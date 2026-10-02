"""Minimal, dependency-free RouterOS API client for MikroTik devices.

Supports RouterOS API over TCP 8728 and API-SSL over TCP 8729.  Credentials are
never logged and are accepted only through constructor arguments/environment.
The client intentionally exposes structured command execution rather than
shell-like command strings.
"""

from __future__ import annotations

import hashlib
import logging
import os
import socket
import ssl
import struct
from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

logger = logging.getLogger(__name__)


class RouterOSError(Exception):
    """Base exception for RouterOS client errors."""


class RouterOSConnectionError(RouterOSError):
    """Raised when the TCP/TLS connection cannot be established."""


class RouterOSAuthenticationError(RouterOSError):
    """Raised when RouterOS rejects authentication."""


class RouterOSCommandError(RouterOSError):
    """Raised when RouterOS returns a !trap or !fatal response."""


class RouterOSTimeoutError(RouterOSConnectionError):
    """Raised when a RouterOS operation times out."""


@dataclass(frozen=True)
class RouterOSConfig:
    host: str
    username: str
    password: str
    port: int = 8729
    tls: bool = True
    timeout: float = 10.0
    verify_tls: bool = True

    @classmethod
    def from_env(cls, prefix: str = "MIKROTIK_") -> "RouterOSConfig":
        host = os.getenv(f"{prefix}HOST")
        username = os.getenv(f"{prefix}USERNAME")
        password = os.getenv(f"{prefix}PASSWORD")
        if not host or not username or password is None:
            raise ValueError(
                f"{prefix}HOST, {prefix}USERNAME and {prefix}PASSWORD are required"
            )
        port = int(os.getenv(f"{prefix}PORT", "8729"))
        tls = os.getenv(f"{prefix}TLS", "true").strip().lower() in {"1", "true", "yes", "on"}
        verify_tls = os.getenv(f"{prefix}VERIFY_TLS", "true").strip().lower() in {
            "1", "true", "yes", "on"
        }
        return cls(
            host=host,
            username=username,
            password=password,
            port=port,
            tls=tls,
            timeout=float(os.getenv(f"{prefix}TIMEOUT", "10")),
            verify_tls=verify_tls,
        )


def _encode_length(length: int) -> bytes:
    if length < 0:
        raise ValueError("RouterOS word length cannot be negative")
    if length < 0x80:
        return bytes([length])
    if length < 0x4000:
        return bytes([(length >> 8) | 0x80, length & 0xFF])
    if length < 0x200000:
        return bytes([(length >> 16) | 0xC0, (length >> 8) & 0xFF, length & 0xFF])
    if length < 0x10000000:
        return bytes(
            [(length >> 24) | 0xE0, (length >> 16) & 0xFF, (length >> 8) & 0xFF, length & 0xFF]
        )
    if length < 0x100000000:
        return b"\xF0" + struct.pack(">I", length)
    raise ValueError("RouterOS word is too large")


def _decode_length(sock: socket.socket) -> int:
    first = sock.recv(1)
    if not first:
        raise RouterOSConnectionError("RouterOS closed the connection")
    value = first[0]
    if value < 0x80:
        return value
    if value < 0xC0:
        return ((value & 0x3F) << 8) | _recv_exact(sock, 1)[0]
    if value < 0xE0:
        return ((value & 0x1F) << 16) | struct.unpack(">H", _recv_exact(sock, 2))[0]
    if value < 0xF0:
        return ((value & 0x0F) << 24) | int.from_bytes(_recv_exact(sock, 3), "big")
    if value == 0xF0:
        return struct.unpack(">I", _recv_exact(sock, 4))[0]
    raise RouterOSConnectionError(f"Invalid RouterOS length prefix: 0x{value:02x}")


def _recv_exact(sock: socket.socket, size: int) -> bytes:
    data = bytearray()
    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise RouterOSConnectionError("RouterOS closed the connection")
        data.extend(chunk)
    return bytes(data)


def _word(value: str) -> bytes:
    raw = value.encode("utf-8")
    return _encode_length(len(raw)) + raw


def _sentence(words: Iterable[str]) -> bytes:
    return b"".join(_word(word) for word in words) + _word("")


def _decode_sentence(sock: socket.socket) -> list[str]:
    words: list[str] = []
    while True:
        length = _decode_length(sock)
        if length == 0:
            return words
        words.append(_recv_exact(sock, length).decode("utf-8", errors="replace"))


def _parse_sentence(words: Sequence[str]) -> dict[str, str | list[str]]:
    result: dict[str, str | list[str]] = {"!type": words[0] if words else ""}
    for word in words[1:]:
        if not word.startswith("="):
            continue
        key, _, value = word[1:].partition("=")
        if key in result:
            old = result[key]
            if isinstance(old, list):
                old.append(value)
            else:
                result[key] = [old, value]
        else:
            result[key] = value
    return result


class RouterOSClient:
    """Synchronous RouterOS API client safe to use from FastAPI thread pools."""

    def __init__(self, config: RouterOSConfig):
        self.config = config
        self._sock: socket.socket | None = None

    def __enter__(self) -> "RouterOSClient":
        self.connect()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    def connect(self) -> None:
        if self._sock is not None:
            return
        try:
            raw = socket.create_connection((self.config.host, self.config.port), self.config.timeout)
            raw.settimeout(self.config.timeout)
            if self.config.tls:
                context = ssl.create_default_context()
                if not self.config.verify_tls:
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                self._sock = context.wrap_socket(raw, server_hostname=self.config.host)
            else:
                self._sock = raw
            self._login()
        except (socket.timeout, TimeoutError) as exc:
            self.close()
            raise RouterOSTimeoutError("Timed out connecting to MikroTik") from exc
        except RouterOSError:
            self.close()
            raise
        except (OSError, ssl.SSLError) as exc:
            self.close()
            raise RouterOSConnectionError(f"Unable to connect to {self.config.host}:{self.config.port}") from exc

    def close(self) -> None:
        sock, self._sock = self._sock, None
        if sock is not None:
            try:
                sock.close()
            except OSError:
                logger.debug("Error while closing RouterOS socket", exc_info=True)

    def execute(
        self,
        command: str,
        attributes: Mapping[str, str] | None = None,
        *,
        extra_words: Iterable[str] = (),
    ) -> list[dict[str, str | list[str]]]:
        """Execute a RouterOS API command using structured attributes."""
        if not command.startswith("/") or any(ch in command for ch in "\r\n\x00"):
            raise ValueError("command must be a single RouterOS path beginning with '/'")
        if attributes:
            for key, value in attributes.items():
                if not key or any(ch in key for ch in "=\r\n\x00"):
                    raise ValueError("invalid RouterOS attribute name")
                if any(ch in str(value) for ch in "\r\n\x00"):
                    raise ValueError("invalid RouterOS attribute value")
        self.connect()
        assert self._sock is not None
        words = [command, *[f"={k}={v}" for k, v in (attributes or {}).items()], *extra_words]
        try:
            self._sock.sendall(_sentence(words))
            replies: list[dict[str, str | list[str]]] = []
            while True:
                sentence = _parse_sentence(_decode_sentence(self._sock))
                reply_type = str(sentence.get("!type", ""))
                replies.append(sentence)
                if reply_type in {"!trap", "!fatal"}:
                    message = str(sentence.get("message", "RouterOS command failed"))
                    raise RouterOSCommandError(message)
                if reply_type == "!done":
                    return replies
        except socket.timeout as exc:
            self.close()
            raise RouterOSTimeoutError("Timed out waiting for MikroTik response") from exc
        except (OSError, UnicodeError) as exc:
            self.close()
            raise RouterOSConnectionError("RouterOS connection failed during command execution") from exc

    def _login(self) -> None:
        assert self._sock is not None
        # RouterOS v7 accepts username/password directly. Older RouterOS
        # versions return a challenge and require the legacy MD5 response.
        self._sock.sendall(_sentence(["/login", f"=name={self.config.username}", f"=password={self.config.password}"]))
        reply = _parse_sentence(_decode_sentence(self._sock))
        if reply.get("!type") == "!done":
            return
        if reply.get("!type") in {"!trap", "!fatal"}:
            message = str(reply.get("message", "Authentication failed"))
            if "unknown command" not in message.lower() and "argument" not in message.lower():
                raise RouterOSAuthenticationError(message)
        self._sock.sendall(_sentence(["/login"]))
        challenge = _parse_sentence(_decode_sentence(self._sock))
        if challenge.get("!type") != "!done" or not isinstance(challenge.get("ret"), str):
            raise RouterOSAuthenticationError("MikroTik authentication handshake failed")
        digest = hashlib.md5(b"\x00" + self.config.password.encode() + bytes.fromhex(challenge["ret"])).hexdigest()
        self._sock.sendall(
            _sentence(
                [
                    "/login",
                    f"=name={self.config.username}",
                    f"=response=00{digest}",
                ]
            )
        )
        final = _parse_sentence(_decode_sentence(self._sock))
        if final.get("!type") != "!done":
            raise RouterOSAuthenticationError(str(final.get("message", "Authentication failed")))


__all__ = [
    "RouterOSClient",
    "RouterOSConfig",
    "RouterOSError",
    "RouterOSConnectionError",
    "RouterOSAuthenticationError",
    "RouterOSCommandError",
    "RouterOSTimeoutError",
]
