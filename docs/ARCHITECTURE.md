# NetPulse-AI Architecture

A modular Pure NMS & AI NOC foundation.

## Layers
- Frontend Cockpit: Next.js operator interface.
- API: FastAPI HTTP interface.
- Core: configuration, security, observability and shared runtime concerns.
- Services: domain orchestration.
- Plugins: vendor/device adapters, initially MikroTik and OLT.
- Models/Schemas: domain and API contracts.
- AI NOC: event correlation, anomaly detection, incident intelligence and operator assistance.

## Principles
1. Vendor integrations remain behind plugin boundaries.
2. API contracts stay independent from device implementations.
3. Prefer asynchronous, observable workflows.
4. Keep secrets in runtime configuration, never source code.
5. Deploy frontend and backend independently.