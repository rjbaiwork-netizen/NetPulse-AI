# Authentication, RBAC and GIS hydration

## Authentication
Short-lived JWT bearer tokens are signed with `NETPULSE_JWT_SECRET`. The bootstrap admin password is supplied as a bcrypt hash through `NETPULSE_ADMIN_PASSWORD_HASH`; plaintext passwords are never stored.

## Roles
- **admin**: full device CRUD and operational actions; device deletion is admin-only.
- **technician**: device read/create/update and MikroTik/OLT operational actions.

The current bootstrap login is environment-backed. A production multi-operator deployment should add a database-backed user table, refresh-token rotation, rate limiting and audit logs.

## GIS
Devices persist `latitude` (-90..90) and `longitude` (-180..180). `GET /api/v1/devices` returns coordinates and the frontend map hydrates markers from that response. Existing databases require an Alembic migration because startup `create_all` does not alter existing tables.

## Frontend security
The cockpit stores the short-lived access token in `sessionStorage`, and protected pages redirect unauthenticated browser sessions to `/login`. Production should use HTTPS, CSP/security headers, rate limiting, audit logging and a hardened session strategy.
