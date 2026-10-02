"""Business operations for MikroTik PPPoE/NMS management."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Mapping

from app.plugins.mikrotik.routeros_api import (
    RouterOSClient,
    RouterOSConfig,
    RouterOSCommandError,
    RouterOSConnectionError,
)

logger = logging.getLogger(__name__)
_SAFE_NAME = re.compile(r"^[A-Za-z0-9._:@/+\-]{1,128}$")


class MikroTikServiceError(Exception):
    """Base service-layer exception."""


class MikroTikValidationError(MikroTikServiceError):
    """Raised when an operation contains invalid input."""


@dataclass(frozen=True)
class PPPoESecret:
    name: str
    password: str
    profile: str = "default"
    service: str = "pppoe"
    disabled: bool = False
    comment: str | None = None


class MikroTikService:
    """High-level PPPoE and subscriber-control operations.

    A client is created per operation by default so sockets are not shared
    between concurrent FastAPI requests. For larger deployments, a bounded
    connection pool can be introduced above this service layer.
    """

    def __init__(self, config: RouterOSConfig | None = None):
        self.config = config or RouterOSConfig.from_env()

    def _client(self) -> RouterOSClient:
        return RouterOSClient(self.config)

    @staticmethod
    def _validate_name(value: str, field: str) -> str:
        if not isinstance(value, str) or not _SAFE_NAME.fullmatch(value):
            raise MikroTikValidationError(f"Invalid {field}")
        return value

    @staticmethod
    def _validate_limit(value: int, field: str) -> int:
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise MikroTikValidationError(f"{field} must be a positive integer")
        return value

    def add_pppoe_secret(self, secret: PPPoESecret) -> list[dict[str, str | list[str]]]:
        """Create a PPPoE secret without logging its password."""
        self._validate_name(secret.name, "PPPoE username")
        self._validate_name(secret.profile, "PPP profile")
        self._validate_name(secret.service, "service")
        if not secret.password or len(secret.password) > 256:
            raise MikroTikValidationError("PPPoE password must be 1-256 characters")
        attrs = {
            "name": secret.name,
            "password": secret.password,
            "profile": secret.profile,
            "service": secret.service,
            "disabled": "yes" if secret.disabled else "no",
        }
        if secret.comment is not None:
            attrs["comment"] = secret.comment[:255]
        with self._client() as client:
            return client.execute("/ppp/secret/add", attrs)

    def set_speed_profile(self, username: str, download_bps: int, upload_bps: int) -> list[dict[str, str | list[str]]]:
        """Change a PPPoE user's active simple queue/profile speed.

        The operation targets the queue by its comment convention
        'netpulse:<username>'. Deployments may replace this lookup with their
        own subscriber-to-queue mapping.
        """
        self._validate_name(username, "PPPoE username")
        down = self._validate_limit(download_bps, "download_bps")
        up = self._validate_limit(upload_bps, "upload_bps")
        queue_id = self._find_queue_id(username)
        with self._client() as client:
            return client.execute(
                "/queue/simple/set",
                {".id": queue_id, "max-limit": f"{up}/{down}"},
            )

    def kick_active_session(self, username: str) -> int:
        """Immediately disconnect every active PPP session for a username."""
        self._validate_name(username, "PPPoE username")
        with self._client() as client:
            replies = client.execute("/ppp/active/print", {"?name": username})
            removed = 0
            for row in replies:
                session_id = row.get(".id")
                if isinstance(session_id, str) and session_id.startswith("*"):
                    client.execute("/ppp/active/remove", {".id": session_id})
                    removed += 1
            return removed

    def _find_queue_id(self, username: str) -> str:
        with self._client() as client:
            replies = client.execute(
                "/queue/simple/print",
                {("?comment"): f"netpulse:{username}"},
            )
        for row in replies:
            queue_id = row.get(".id")
            if isinstance(queue_id, str) and queue_id.startswith("*"):
                return queue_id
        raise MikroTikServiceError(f"No NetPulse queue found for {username}")

    def update_secret_profile(self, username: str, profile: str) -> list[dict[str, str | list[str]]]:
        """Change the RouterOS PPP profile assigned to an existing secret."""
        self._validate_name(username, "PPPoE username")
        self._validate_name(profile, "PPP profile")
        with self._client() as client:
            replies = client.execute("/ppp/secret/print", {"?name": username})
            secret_id = next(
                (str(row[".id"]) for row in replies if isinstance(row.get(".id"), str) and str(row[".id"]).startswith("*")),
                None,
            )
            if not secret_id:
                raise MikroTikServiceError(f"PPPoE secret not found: {username}")
            return client.execute("/ppp/secret/set", {".id": secret_id, "profile": profile})

    def disable_secret(self, username: str) -> list[dict[str, str | list[str]]]:
        """Disable a PPPoE secret and terminate its current session."""
        self._validate_name(username, "PPPoE username")
        with self._client() as client:
            replies = client.execute("/ppp/secret/print", {"?name": username})
            secret_id = next(
                (str(row[".id"]) for row in replies if isinstance(row.get(".id"), str) and str(row[".id"]).startswith("*")),
                None,
            )
            if not secret_id:
                raise MikroTikServiceError(f"PPPoE secret not found: {username}")
            result = client.execute("/ppp/secret/set", {".id": secret_id, "disabled": "yes"})
            # Keep the same TCP connection for the follow-up kick.
            active = client.execute("/ppp/active/print", {"?name": username})
            for row in active:
                session_id = row.get(".id")
                if isinstance(session_id, str) and session_id.startswith("*"):
                    client.execute("/ppp/active/remove", {".id": session_id})
            return result


__all__ = [
    "MikroTikService",
    "MikroTikServiceError",
    "MikroTikValidationError",
    "PPPoESecret",
]
