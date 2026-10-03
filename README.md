# NetPulse-AI

**Pure NMS & AI NOC platform foundation**

Production-oriented modular foundation for network monitoring, device/plugin integration, service orchestration and AI-assisted NOC operations.

## Layout
- .github/workflows/ — CI automation
- backend/ — FastAPI infrastructure
- frontend/ — Next.js operator cockpit
- docs/ — architecture and API documentation

## Local development
Backend: cd backend && python -m venv .venv && pip install -r requirements.txt && uvicorn app.main:app --reload

Frontend: cd frontend && npm install && npm run dev

Backend health: http://localhost:8000/health

## Architecture direction
API, Core, Models/Schemas, Services and vendor Plugins are separated so MikroTik/OLT integrations can evolve independently. AI NOC capabilities are added behind these boundaries.

This is the bootstrap foundation; production hardening, authentication, persistence, observability, queues, device protocols and AI workflows are subsequent layers.

## GitHub-only operation

NetPulse-AI is configured for repeatable GitHub Codespaces development. The repository's `.devcontainer/devcontainer.json` automatically installs backend and frontend dependencies, forwards ports **3000** and **8000**, and starts FastAPI plus the Next.js development server when the Codespace starts. GitHub supports `postCreateCommand` for setup after container creation and `postStartCommand` for commands each time the container starts.

After creating or rebuilding the Codespace, the services are started automatically:

- FastAPI: `https://<CODESPACE_NAME>-8000.<GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN>/health`
- Next.js: `https://<CODESPACE_NAME>-3000.<GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN>`

GitHub supplies `CODESPACE_NAME` and `GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN`, so the configuration does not hardcode a Codespaces hostname.

### First-time setup

1. Open the repository in GitHub Codespaces.
2. If the Codespace already existed before this configuration was committed, run **Codespaces: Rebuild Container** so the new lifecycle configuration is applied.
3. Wait for the post-create installation to finish.
4. Open **Ports** and confirm ports **3000** and **8000** are forwarded.
5. For GitHub Pages or any external browser client to reach FastAPI, change port **8000** visibility to **Public**. Forwarded ports are private by default.
6. Use the displayed 8000 URL as the backend URL. The Codespaces startup script also derives the same URL automatically for the Next.js runtime configuration.

### Authentication secrets

Codespaces automation intentionally does **not** commit credentials or cryptographic secrets. Configure these as Codespaces secrets/environment variables when authentication and device onboarding are needed:

```text
NETPULSE_ENCRYPTION_KEY
NETPULSE_JWT_SECRET
NETPULSE_ADMIN_USERNAME
NETPULSE_ADMIN_PASSWORD_HASH
NETPULSE_CORS_ORIGINS   # optional; the startup script adds the current Codespaces frontend origin
```

Without the authentication bootstrap values, the backend health endpoint can still be tested, but login/device credential operations should not be treated as configured.

### Logs and manual restart

The startup script writes logs to:

```text
/tmp/netpulse-backend.log
/tmp/netpulse-frontend.log
```

If a service is stopped, rerun:

```bash
bash .devcontainer/start.sh
```

NetPulse-AI does not require ngrok. GitHub Pages can host the static Next.js operator UI, while Codespaces provides the temporary live FastAPI/frontend development environment.

### Important production boundary

GitHub Pages cannot execute FastAPI/Python server code. GitHub-hosted Actions runners are ephemeral, so they are suitable for CI/deployment jobs, not as a permanent backend server. A permanent backend requires a separately hosted VM/VPS or another server platform. A Codespace is likewise a development/live-testing environment rather than a 24/7 production server.

