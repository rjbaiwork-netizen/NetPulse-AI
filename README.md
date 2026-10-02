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