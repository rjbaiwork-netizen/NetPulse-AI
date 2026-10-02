# Device Management & Telemetry Core

Credentials are encrypted at rest with AES-256-GCM using NETPULSE_ENCRYPTION_KEY. Never commit that key; provide it through a deployment secret manager.

## MikroTik
POST /api/v1/mikrotik/{device_id}/pppoe/secrets — create PPPoE secret.
POST /api/v1/mikrotik/{device_id}/pppoe/speed — change queue speed.
POST /api/v1/mikrotik/{device_id}/pppoe/kick — immediately terminate active sessions.

The RouterOS client defaults to API-SSL on 8729. Plain 8728 should only be used on trusted networks.

## OLT / SNMP
POST /api/v1/olt/interface/status — standard IF-MIB ifOperStatus.
POST /api/v1/olt/onu/poll — optical signal, attenuation, operational status, LOS and Dying Gasp using configured vendor OIDs.

Dying Gasp is classified separately when the configured OID reports an active indication. LOS/down without Dying Gasp is classified as FIBER_CUT_OR_LOS; declaring a physical fiber cut should additionally correlate multiple affected ONUs/interfaces and alarms.

SQLite is the development default. Production should use PostgreSQL and Alembic migrations before deployment.
