# NetPulse-AI Production Backend Deployment

## Architecture

GitHub Pages hosts the static Next.js frontend. FastAPI must run as a persistent service on a separate container host or VM.

Recommended flow:

`GitHub Pages -> HTTPS FastAPI -> PostgreSQL/SQLite -> MikroTik/OLT`

## Persistent Render deployment

The repository includes `render.yaml` for a persistent Docker + PostgreSQL deployment on Render. Render Blueprints can provision the web service and PostgreSQL database from the repository definition. citeturn0search0turn0search3

1. Connect the repository to Render and create a Blueprint from `render.yaml`.
2. Provide `NETPULSE_ADMIN_USERNAME` and a bcrypt `NETPULSE_ADMIN_PASSWORD_HASH` when prompted; do not commit them.
3. Render provisions the PostgreSQL connection through `DATABASE_URL` and generates the encryption/JWT secrets.
4. Wait for `/health` to become healthy and copy the HTTPS `onrender.com` service URL.
5. Set GitHub repository variable `NETPULSE_API_BASE_URL` to that URL and let the Pages workflow rebuild the frontend.

This is the intended persistent backend path. Codespaces/ngrok remains suitable for temporary development only.

## Backend container

Build from `backend/`:

```bash
docker build -t netpulse-ai-backend ./backend
docker run --rm -p 8000:8000 \\
  -e DATABASE_URL='...' \\
  -e NETPULSE_ENCRYPTION_KEY='...' \\
  -e NETPULSE_JWT_SECRET='...' \\
  -e NETPULSE_ADMIN_USERNAME='...' \\
  -e NETPULSE_ADMIN_PASSWORD_HASH='...' \\
  -e NETPULSE_CORS_ORIGINS='https://rjbaiwork-netizen.github.io' \\
  netpulse-ai-backend
```

The image runs `alembic upgrade head` before starting Uvicorn.

## Required production secrets

Set these through the hosting provider's secret/environment mechanism; never commit them:

- `NETPULSE_ENCRYPTION_KEY`
- `NETPULSE_JWT_SECRET`
- `NETPULSE_ADMIN_USERNAME`
- `NETPULSE_ADMIN_PASSWORD_HASH`

For production, use a strong 32-byte encryption key and a long random JWT secret.

## Database

Use PostgreSQL for production. SQLite remains suitable for local development and CI.

Example:

`DATABASE_URL=postgresql+psycopg://USER:PASSWORD@HOST:5432/netpulse`

The PostgreSQL driver must be installed in `backend/requirements.txt` when PostgreSQL is selected.

## Frontend

Set the GitHub repository variable `NETPULSE_API_BASE_URL` to the public HTTPS FastAPI base URL.

The Pages workflow already reads this variable and injects it as `NEXT_PUBLIC_API_BASE_URL`.

Do not use a GitHub Actions runner as the production backend: the runner terminates when the workflow finishes.

## Health check

After deployment, verify:

`GET /health`

The response must be successful before connecting the frontend.

## Live network validation

After the backend is persistent:

1. Login.
2. List devices.
3. Test MikroTik connection.
4. Read active PPPoE sessions.
5. Open a customer profile.
6. Verify Customer -> PPPoE -> MikroTik correlation.
7. Verify OLT monitoring.
8. Verify GIS markers.
9. Verify AI-NOC audit behavior.

## Security

Put the API behind HTTPS and a firewall. Restrict device management access to approved network addresses where possible. Never expose RouterOS/SNMP credentials in frontend code or logs.
