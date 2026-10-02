# NetPulse-AI Production Hardening

## Authentication and RBAC
- JWT access tokens use HS256 and bcrypt password verification.
- Bootstrap administrator credentials come from environment variables; no default password is committed.
- admin and technician roles are enforced on device, MikroTik, OLT and AI-NOC APIs.
- Device deletion remains admin-only.
- Browser tokens are kept in sessionStorage, not persistent localStorage; production deployments should additionally enforce HTTPS, CSP and a hardened session strategy.

## GIS schema
Devices now expose latitude, longitude and pop_name.
Run `alembic upgrade head` against the deployment database before a release that depends on the new schema. Existing databases created before Alembic adoption should be inspected and stamped at the appropriate baseline after verification.

## AI-NOC
The command layer is intentionally structured rather than an unrestricted LLM-to-router bridge:
- show devices
- check signal <device-id>
- kick session <device-id> <username>

Every command produces an audit record containing actor, role, action, target, success and a bounded detail field. Network credentials and passwords are not written to audit details.

## Operational hardening still recommended
- Move from environment-only bootstrap admin to a database-backed user lifecycle.
- Prefer RS256/EdDSA signing with key rotation for multi-instance production.
- Add refresh-token rotation, login throttling/account lockout and security event monitoring.
- Add vendor-specific OID profiles and SNMPv3/trap ingestion.