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

NetPulse-AI does not require ngrok. GitHub Pages can host the static Next.js operator UI, while GitHub Actions validates the FastAPI backend and publishes the frontend.

For an all-GitHub development server, open this repository in **GitHub Codespaces** and run:

```bash
pip install -r backend/requirements.txt
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

In a second terminal:

```bash
cd frontend
npm install
NEXT_PUBLIC_API_BASE_URL="https://<CODESPACE-NAME>-8000.app.github.dev" npm run dev -- --hostname 0.0.0.0 --port 3000
```

Then use the Codespaces **Ports** panel to forward ports 8000 and 3000. GitHub can expose a forwarded port publicly for testing. The Codespaces URL is temporary and can change; it is not a 24/7 VPS.

### Important production boundary

GitHub Pages cannot execute FastAPI/Python server code. GitHub-hosted Actions runners are ephemeral, so they are suitable for CI/deployment jobs, not as a permanent backend server. A permanent backend requires a separately hosted VM/VPS or another server platform. This repository therefore keeps backend validation in Actions and avoids pretending that an Actions runner is a production server.

For the Pages workflow, set the repository variable `NETPULSE_API_BASE_URL` to the actual backend URL before deployment.
