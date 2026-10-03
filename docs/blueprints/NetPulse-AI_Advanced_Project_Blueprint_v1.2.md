# NetPulse-AI — Advanced Project Blueprint v1.2

**Live verification date:** 03 October 2026  
**Repository:** `rjbaiwork-netizen/NetPulse-AI`  
**Default branch:** `main`  
**Latest verified documentation commit:** `e1a2663ffa30ddd509302984d4ebea1fd7e36f7b`

> This blueprint is a live engineering baseline. It separates what is implemented today from what is planned. It does not treat the persistent production backend as live until provider-side deployment is independently verified.

---

## 1. Document Control

| Item | Value |
|---|---|
| Project | NetPulse-AI |
| Project class | ISP NMS + Customer Network Management + GIS + AI-NOC |
| Primary repository | GitHub — rjbaiwork-netizen/NetPulse-AI |
| Baseline | 03 October 2026 |
| Blueprint | v1.2 |
| Current branch | main |
| Current repo visibility | Public |
| Verified GitHub permissions | admin, maintain, push, pull, triage |
| Frontend target | GitHub Pages |
| Backend target | Persistent HTTPS service such as Render/Railway/VPS |
| Primary database | PostgreSQL |
| Development/CI database | SQLite |
| Current production blocker | Docker build-context/package consistency |

## 2. Executive Summary

NetPulse-AI is an ISP-focused Network Management System (NMS), Customer Network Management platform, GIS operations cockpit and AI-NOC orchestration layer.

The platform is designed to give an ISP/NOC one operational view of:

- network devices and infrastructure inventory;
- customer records and network relationships;
- MikroTik RouterOS and PPPoE state;
- OLT/access-network telemetry;
- customer and infrastructure GIS coordinates;
- alarms, incidents and audit history;
- controlled AI-assisted diagnostics and automation.

The intended operational relationship is:

`OLT → PON → ONU/ONT → Customer → PPPoE → MikroTik → Telemetry → Alarm/Incident → AI-NOC`

The current repository already contains the foundation for customer management, GIS, MikroTik integration, OLT/SNMP monitoring, authentication/RBAC, audit logging, migrations, frontend cockpit and CI/CD. The immediate engineering gap is deployment packaging consistency: the production Dockerfile expects root-level Alembic files while the current CI/Render Docker context is `backend/`.

## 3. Project Type — What Kind of Project Is This?

NetPulse-AI is a **network operations and customer-network intelligence platform for Internet Service Providers (ISPs)**.

It is not intended to be:

- an accounting/billing system;
- an invoice/payment platform;
- a package/bandwidth sales/billing suite;
- a generic help-desk/ticketing product;
- an HR/ERP system;
- a building-management system.

Its primary purpose is technical operations: inventory, monitoring, correlation, GIS, diagnostics, incident visibility and controlled network automation.

## 4. Why This Project Is Being Built

Traditional ISP operations often split information between router interfaces, OLT consoles, spreadsheets, customer records, maps and separate monitoring tools. That makes it difficult to answer operational questions such as:

1. Which customer is affected by a network fault?
2. Which PPPoE session belongs to which customer?
3. Which MikroTik/OLT/PON/ONU path is involved?
4. Where is the affected customer or device geographically?
5. What telemetry and alarms explain the incident?
6. Which action is safe to automate?
7. Who performed the action and what was the result?

NetPulse-AI is designed to create a unified operational data and action layer around those questions.

## 5. Vision

Create a secure, auditable and extensible ISP NOC platform where infrastructure, customer relationships, GIS, telemetry, alarms and AI-assisted operations are connected through a common data model and controlled APIs.

## 6. Mission

Build the platform incrementally from a reliable production foundation:

**Inventory → Connectivity → Telemetry → Correlation → GIS → Incidents → AI-NOC → Controlled Automation → SRE/Scale**

## 7. Objectives

### 7.1 Primary objectives

- Centralize network and customer inventory.
- Maintain customer-to-network relationships.
- Correlate PPPoE users with live MikroTik sessions.
- Monitor MikroTik and OLT infrastructure.
- Persist customer/device GIS data and location history.
- Provide operator dashboards and map-based visibility.
- Build an auditable alarm and incident foundation.
- Provide AI-assisted diagnostics without unrestricted device control.
- Apply RBAC, encryption, audit logging and secure secret handling.
- Establish repeatable CI/CD and production deployment.

### 7.2 Engineering objectives

- API-first backend architecture.
- Modular network plugins.
- Database migrations through Alembic.
- Testable services and adapters.
- Static frontend deployment compatibility.
- Persistent backend hosting.
- PostgreSQL for production.
- Observability, backup and disaster-recovery readiness.

## 8. Scope

### In scope

1. Customer database and customer management.
2. Network device inventory.
3. MikroTik RouterOS integration.
4. PPPoE secret/session correlation.
5. OLT/SNMP monitoring foundation.
6. GIS/map operations.
7. Customer location history.
8. Alarms and incidents.
9. Audit logging.
10. Authentication and RBAC.
11. AI-NOC diagnostics and controlled automation.
12. CI/CD and production deployment.
13. Security hardening and observability.

### Explicitly out of scope

- Billing.
- Invoice generation.
- Payment processing.
- Package/bandwidth billing.
- Support-ticketing suites.
- HR/ERP.
- Building management.

## 9. Functional Feature Blueprint

### 9.1 Dashboard

- Device totals and status.
- Customer totals and status.
- Alarm/incident indicators.
- Network operational overview.
- Future: live KPI panels and trend graphs.

### 9.2 Customer Management

- Customer code.
- Name.
- Phone/email.
- Address.
- PPPoE username.
- Linked network device.
- Status.
- Latitude/longitude.
- Location accuracy/source/time.
- Notes.
- Location history.
- Network-status lookup.

### 9.3 Device Management

- Device identity.
- Device type.
- Host/port.
- Vendor.
- Enabled/disabled state.
- GIS metadata.
- Encrypted credentials.
- Live onboarding validation.

### 9.4 MikroTik

- Native RouterOS API foundation.
- Connection testing.
- PPPoE secret listing.
- Active session listing.
- Customer-to-PPPoE correlation.
- Controlled session kick.
- Speed/profile operations foundation.
- Future: richer telemetry and policy workflows.

### 9.5 OLT / Access Network

- SNMP polling foundation.
- System information.
- Interface/optical telemetry foundation.
- Fault classification.
- Future: vendor profiles, PON/ONU inventory, traps and SNMPv3.

### 9.6 GIS

- Device coordinates.
- Customer coordinates.
- Location accuracy.
- Location source.
- Location timestamps.
- Google Maps visualization.
- Marker-based infrastructure/customer view.
- Customer location history.
- Future: PON/fiber topology layers and coverage visualization.

### 9.7 AI-NOC

Current:

- Structured intent parser.
- Device listing.
- Signal/health query foundation.
- Controlled session-kick command.
- Audit logging.

Target:

- Evidence retrieval.
- Alarm correlation.
- Root-cause analysis assistance.
- Customer-impact calculation.
- Suggested remediation.
- Human approval gates for disruptive actions.
- Execution.
- Post-action verification.
- Full audit trail.

### 9.8 Security

Current foundation:

- JWT authentication.
- bcrypt password hashing.
- Admin/technician RBAC.
- AES-GCM credential-encryption foundation.
- Audit logging.
- No credential logging.

Target hardening:

- Database-backed user lifecycle.
- Login throttling and lockout.
- Refresh-token rotation.
- Key rotation.
- Device network allowlists.
- SSRF-safe host validation.
- Security-event monitoring.
- Secret-management integration.

## 10. Technology Stack

### Backend

- Python 3.12
- FastAPI
- Uvicorn
- SQLAlchemy 2.x
- Pydantic 2.x
- Alembic
- PostgreSQL
- psycopg
- SQLite for local/CI validation

### Network integrations

- Native MikroTik RouterOS API
- TCP 8728 / TLS 8729 foundation
- pysnmp
- SNMP-based OLT polling
- Future SNMPv3 and traps
- Future vendor-specific OLT adapters

### Frontend

- Next.js
- TypeScript
- Tailwind CSS
- Static export for GitHub Pages
- Google Maps JavaScript integration

### Security

- JWT
- bcrypt
- cryptography/AES-GCM foundation
- HTTPS
- CORS
- RBAC
- audit logs

### DevOps

- GitHub
- GitHub Actions
- GitHub Pages
- Docker
- Render Blueprint foundation
- PostgreSQL
- Codespaces for development
- ngrok only as temporary development tunneling when required

### AI/NOC direction

- Structured command layer first.
- Evidence retrieval and deterministic tools.
- LLM-assisted reasoning only around approved evidence/tools.
- Approval/verification/audit gates before disruptive automation.

## 11. Architecture

```
                         ┌───────────────────────────┐
                         │       NOC Operator        │
                         │ Admin / Technician        │
                         └─────────────┬─────────────┘
                                       │ HTTPS
                                       ▼
                         ┌───────────────────────────┐
                         │ Next.js Operator Cockpit  │
                         │ Dashboard / Map / Customer│
                         │ Devices / AI-NOC / Login  │
                         └─────────────┬─────────────┘
                                       │ JSON API
                                       ▼
                         ┌───────────────────────────┐
                         │       FastAPI Backend      │
                         ├───────────────────────────┤
                         │ Auth/RBAC                  │
                         │ Customer Management        │
                         │ Device Management          │
                         │ MikroTik API               │
                         │ OLT/SNMP                   │
                         │ GIS                         │
                         │ Alarm/Incident              │
                         │ AI-NOC                      │
                         │ Audit                       │
                         └───────┬─────────┬─────────┘
                                 │         │
                    ┌────────────┘         └──────────────┐
                    ▼                                     ▼
           ┌──────────────────┐                  ┌─────────────────┐
           │ PostgreSQL       │                  │ Network Layer   │
           │ Inventory        │                  │ MikroTik / OLT  │
           │ Customers        │                  │ ONU/ONT / SNMP  │
           │ Locations        │                  └─────────────────┘
           │ Alarms/Incidents │
           │ Audit            │
           └──────────────────┘
                    │
                    ▼
           ┌──────────────────┐
           │ GIS / Maps       │
           │ Customer impact  │
           └──────────────────┘
```

## 12. Repository Structure — Current Verified Tree

```
NetPulse-AI/
├── .devcontainer/
│   ├── devcontainer.json
│   └── start.sh
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── .env.example
├── .gitignore
├── README.md
├── alembic.ini
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 0001_device_geo_pop.py
│       └── 0002_customer_location.py
├── backend/
│   ├── .dockerignore
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── api/
│       │   ├── __init__.py
│       │   ├── ai_noc.py
│       │   ├── auth.py
│       │   ├── customers.py
│       │   ├── dependencies.py
│       │   ├── devices.py
│       │   ├── mikrotik.py
│       │   └── olt.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── database.py
│       │   └── security.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── alarm.py
│       │   ├── audit_log.py
│       │   ├── customer.py
│       │   ├── device.py
│       │   └── profile.py
│       ├── plugins/
│       │   ├── __init__.py
│       │   ├── mikrotik/
│       │   │   ├── __init__.py
│       │   │   └── routeros_api.py
│       │   └── olt/
│       │       ├── __init__.py
│       │       └── snmp_poller.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── ai_noc.py
│       │   ├── alarm.py
│       │   ├── customer.py
│       │   ├── device.py
│       │   ├── mikrotik.py
│       │   ├── olt.py
│       │   └── profile.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── mikrotik_service.py
│       └── tests/
│           ├── test_api.py
│           ├── test_auth_and_ai_noc.py
│           ├── test_customers.py
│           ├── test_health.py
│           └── test_routeros_api.py
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── AUTH_RBAC_GIS.md
│   ├── DEVICE_TELEMETRY_API.md
│   ├── FRONTEND_COCKPIT.md
│   ├── PRODUCTION_DEPLOYMENT.md
│   ├── PRODUCTION_HARDENING.md
│   └── blueprints/
│       ├── README.md
│       └── NetPulse-AI_Advanced_Project_Blueprint_v1.1.md
├── frontend/
│   ├── .env.example
│   ├── .eslintrc.json
│   ├── next-env.d.ts
│   ├── next.config.mjs
│   ├── next.config.ts
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── src/
│       ├── app/
│       │   ├── ai-noc/page.tsx
│       │   ├── customers/page.tsx
│       │   ├── customers/profile/page.tsx
│       │   ├── dashboard/page.tsx
│       │   ├── devices/page.tsx
│       │   ├── login/page.tsx
│       │   ├── map/page.tsx
│       │   ├── globals.css
│       │   ├── layout.tsx
│       │   └── page.tsx
│       ├── components/.gitkeep
│       ├── hooks/.gitkeep
│       ├── services/
│       │   ├── .gitkeep
│       │   ├── api.ts
│       │   ├── auth.ts
│       │   └── maps.ts
│       └── types/
│           ├── api.ts
│           └── google.d.ts
└── render.yaml
```

## 13. Database Blueprint — Current Logical Structure

The database is migration-driven. The current schema foundation is centered on these logical entities:

```
PostgreSQL
└── NetPulse-AI
    ├── devices
    │   ├── id
    │   ├── name
    │   ├── type
    │   ├── host / port
    │   ├── username
    │   ├── encrypted_password
    │   ├── tls / enabled
    │   ├── vendor
    │   ├── latitude / longitude
    │   └── pop_name / metadata / timestamps
    │
    ├── customers
    │   ├── id
    │   ├── customer_code
    │   ├── name / phone / email / address
    │   ├── pppoe_username
    │   ├── device_id → devices.id
    │   ├── status
    │   ├── latitude / longitude
    │   ├── location_accuracy_m
    │   ├── location_source
    │   └── timestamps / notes
    │
    ├── customer_locations
    │   ├── id
    │   ├── customer_id → customers.id
    │   ├── latitude / longitude
    │   ├── accuracy_m / source
    │   └── captured_at
    │
    ├── pppoe_profiles
    │   └── profile/bandwidth mapping foundation
    │
    ├── alarms
    │   └── network alarm foundation
    │
    ├── incidents
    │   └── incident lifecycle foundation
    │
    └── audit_logs
        └── actor / role / action / target / result / detail / timestamp
```

### Database relationship view

```
devices 1 ───────< customers
customers 1 ─────< customer_locations
customers ──────── PPPoE identity ─────── MikroTik active session
devices ──────────< alarms
alarms ───────────< incidents
users/actors ─────< audit_logs
```

### Future topology entities

The roadmap should extend the model with explicit access topology such as:

```
OLT
└── PON
    └── ONU/ONT
        └── Fiber/Service Link
            └── Customer
                └── PPPoE
                    └── MikroTik Session
```

These are planned extensions, not claims about current database tables.

## 14. API and Backend Domain Map

```
FastAPI
├── /health
├── /api/v1/auth
│   ├── /login
│   └── /me
├── /api/v1/customers
│   ├── CRUD
│   ├── /{id}/location
│   ├── /{id}/locations
│   └── /{id}/network-status
├── /api/v1/devices
├── /api/v1/mikrotik
│   ├── connection
│   ├── PPPoE secrets
│   ├── active sessions
│   └── controlled actions
├── /api/v1/olt
│   ├── monitor
│   └── ONU polling foundation
└── /api/v1/ai-noc
    └── structured intent/command foundation
```

## 15. GIS and Location Design

The GIS layer has two separate concepts:

1. **Infrastructure location** — device/POP/OLT coordinates.
2. **Customer location** — customer coordinate plus accuracy, source and timestamp.

The current browser GPS function is an operator-side capture mechanism. It should not be described as continuous customer tracking.

A future customer-side location publisher would require:

- explicit user consent;
- authenticated publishing;
- privacy policy;
- accuracy and timestamp controls;
- revocation;
- retention rules;
- anti-spoofing/rate limiting where appropriate.

## 16. AI-NOC Design Principles

AI-NOC must be designed as a controlled operations system rather than an unrestricted chatbot.

Recommended control chain:

```
User Intent
   ↓
Intent Parser
   ↓
Authorization / Policy Check
   ↓
Evidence Retrieval
   ↓
Diagnosis / Recommendation
   ↓
Human Approval (when required)
   ↓
Tool Execution
   ↓
Post-Action Verification
   ↓
Audit Log
   ↓
Incident / Customer Impact Update
```

High-risk actions should require explicit authorization and verification.

## 17. Security Architecture

### Identity

- JWT-based access.
- Admin/technician roles.
- Short-lived access token foundation.

### Secrets

- Encrypted device credentials.
- Secrets supplied through environment/secret management.
- No plaintext credential logging.

### Authorization

- Protected endpoints.
- Role checks.
- Admin-only destructive operations where appropriate.

### Network security

Production should add:

- HTTPS-only operation.
- Network allowlists.
- Safe outbound target validation.
- SSRF protections.
- Device reachability policies.
- Timeouts and connection limits.

### Audit

Record:

- actor;
- role;
- action;
- target;
- success/failure;
- relevant result metadata;
- timestamp.

## 18. CI/CD and Deployment Blueprint

### Current target

```
GitHub
  ├── GitHub Actions
  │    ├── backend compile/test/migration/container validation
  │    └── frontend build/static export
  │
  ├── GitHub Pages
  │    └── Next.js static frontend
  │
  └── Render/Railway/VPS
       ├── FastAPI
       └── PostgreSQL
```

### Current verification state

- Repository is public.
- GitHub permissions: admin/maintain/push/pull/triage verified.
- Latest documentation commits exist on main.
- Earlier verified CI and Pages runs were successful on the previous baseline.
- The production deployment workflow had a failed run because of Docker build-context mismatch.
- Provider-side persistent backend deployment is not considered verified by this blueprint.

### Current Docker packaging issue

The Dockerfile contains:

```
COPY alembic.ini ./alembic.ini
COPY alembic ./alembic
```

but CI currently builds:

```
docker build -t netpulse-ai-backend:ci ./backend
```

That makes root-level Alembic files unavailable to the Docker build context.

The Render Blueprint also currently uses `rootDir: backend` with `dockerContext: .`, while the Dockerfile expects root-level files.

### Phase-0 resolution

Use one consistent packaging model. Preferred:

```
docker build -f backend/Dockerfile -t netpulse-ai-backend:ci .
```

and align Render's Docker context to the repository root, or alternatively move all required Alembic files into the backend package and update configuration. The selected solution must be tested by CI and provider build validation.

## 19. Testing Strategy

### Unit tests

- RouterOS protocol.
- Authentication.
- Customer operations.
- API behavior.
- Health.
- GIS/location persistence.

### Integration tests

- Database migrations.
- Customer ↔ device relations.
- Customer ↔ PPPoE ↔ MikroTik correlation.
- OLT polling adapters.
- AI-NOC authorization and audit.

### Deployment tests

- Docker build.
- Container startup.
- Alembic upgrade.
- /health.
- Static export.
- GitHub Pages reachability.
- Production provider health check.

### Security tests

- Authentication failures.
- Authorization boundaries.
- SSRF controls.
- Secret leakage checks.
- CORS.
- Token expiry.
- Rate limiting.
- Audit completeness.

## 20. Non-Functional Requirements

### Availability

Backend should be hosted on persistent infrastructure rather than ephemeral CI/Codespaces.

### Performance

- Async I/O for network integrations.
- Connection timeouts.
- Background polling workers.
- Pagination.
- Indexed search fields.
- Caching where justified.

### Reliability

- Idempotent provisioning operations.
- Retry policies with bounds.
- Circuit breakers for unstable devices.
- Health/readiness endpoints.
- Backup and restore tests.

### Observability

Target:

- structured logs;
- metrics;
- traces;
- device poll latency;
- API latency;
- error rates;
- alarm rates;
- worker queue health.

## 21. Production Readiness Gaps

Priority gaps:

1. Fix Docker build context.
2. Verify persistent backend provider deployment.
3. Configure production PostgreSQL.
4. Configure secure production secrets.
5. Complete CORS and domain configuration.
6. Add DB-backed user lifecycle.
7. Add rate limiting/lockout.
8. Harden device host validation/SSRF.
9. Add scheduled telemetry polling.
10. Add SNMPv3/traps.
11. Build OLT/PON/ONU/customer topology.
12. Add observability and backup/DR.
13. Conduct security and performance testing.
14. Perform UAT and rollback drills.

## 22. Development Requirements

To build and operate the project, the team needs:

### Software

- Git/GitHub.
- Python 3.12.
- Node.js 20+.
- npm.
- Docker.
- PostgreSQL.
- Optional Codespaces.
- Optional ngrok for temporary development tunnels.

### Network access

- Reachable MikroTik RouterOS API endpoint.
- Reachable OLT SNMP endpoint.
- Correct credentials and least-privilege accounts.
- Firewall rules allowing only required management traffic.

### Cloud/hosting

- GitHub repository.
- Static frontend hosting.
- Persistent backend hosting.
- PostgreSQL.
- Secret management.
- DNS/HTTPS for production.

### Operations

- NOC operator roles.
- Device inventory.
- Customer inventory.
- IP/POP topology information.
- GIS coordinates where applicable.
- Incident and alarm definitions.

## 23. Implementation Method

The project should be developed in controlled increments:

1. **Foundation** — repository, runtime, database, migrations, health.
2. **Identity** — authentication, RBAC, secrets.
3. **Inventory** — devices and customers.
4. **Network adapters** — MikroTik and OLT.
5. **Correlation** — customer/PPPoE/session/device.
6. **GIS** — map and location history.
7. **Telemetry** — scheduled polling and metrics.
8. **Alarm/incident** — event lifecycle.
9. **AI-NOC** — evidence-driven reasoning.
10. **Automation** — approvals, execution, verification.
11. **SRE** — observability, backup, DR, capacity.
12. **Production** — UAT, security review and controlled release.

Each phase must preserve backward compatibility and have a testable exit criterion.

## 24. Professional Operating Model

### Change management

- Every production change through Git.
- Reviewable commits/PRs where practical.
- No manual undocumented production edits.

### Secrets

- Never commit secrets.
- Never put device passwords in logs.
- Rotate production secrets.

### Network actions

- Read-only diagnostics by default.
- Disruptive actions require authorization.
- Every action is auditable.
- Verify results after execution.

### Data

- Use migrations for schema changes.
- Back up production database.
- Test restore procedures.

## 25. Roadmap

### Phase 0 — Packaging and Deployment Foundation
- Fix Docker context.
- Align Render configuration.
- Re-run CI.
- Verify container health.
- Confirm migrations.

**Exit:** reproducible green production image.

### Phase 1 — Production Core
- Persistent FastAPI service.
- PostgreSQL.
- HTTPS.
- Secrets.
- staging/production separation.
- domain configuration.

**Exit:** authenticated production API.

### Phase 2 — NMS Telemetry
- Polling scheduler.
- CPU/memory/interface metrics.
- latency/loss.
- traffic metrics.
- thresholds.
- alarms.

**Exit:** continuously monitored device inventory.

### Phase 3 — Access Network Correlation
- OLT vendor adapters.
- PON/ONU inventory.
- SNMPv3.
- traps.
- optical levels.
- fiber/LOS events.

**Exit:** OLT → ONU → customer relationship.

### Phase 4 — Customer Intelligence + GIS
- Customer impact calculation.
- outage grouping.
- advanced map layers.
- POP/service-area topology.

**Exit:** network event → affected customer visibility.

### Phase 5 — AI-NOC
- evidence retrieval.
- RCA assistance.
- recommendations.
- approval workflows.
- execution verification.
- incident summaries.

**Exit:** auditable AI-assisted NOC workflows.

### Phase 6 — SRE and Scale
- queues/workers.
- metrics/tracing.
- caching.
- HA planning.
- backup/DR.
- capacity tests.

**Exit:** operationally scalable platform.

### Phase 7 — Production Cutover
- UAT.
- security review.
- performance test.
- backup restore drill.
- rollback drill.
- controlled release.

**Exit:** formal production acceptance.

## 26. Phase-0 Exit Checklist

- [ ] Docker build works from a clean checkout.
- [ ] Alembic files are available inside the Docker context.
- [ ] Production image starts.
- [ ] `/health` returns success.
- [ ] Alembic migration succeeds.
- [ ] CI is green.
- [ ] Deployment workflow is green.
- [ ] GitHub Pages is reachable.
- [ ] Frontend backend URL is configured intentionally.
- [ ] Provider-side backend is independently verified.

## 27. Risks and Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Docker context mismatch | Deployment failure | Single source-of-truth build context |
| Unrestricted device targets | SSRF/network abuse | Allowlist and safe target validation |
| Device credential leakage | Critical security issue | Encryption + secret manager + log redaction |
| Network API instability | NOC errors | Timeouts, retries, circuit breakers |
| Incorrect automation | Service disruption | Approval + verification + audit |
| Stale telemetry | Wrong diagnosis | Timestamped metrics and freshness checks |
| Database loss | Operational loss | Backup + restore drills |
| GIS privacy issues | Privacy risk | Consent, access control, retention |
| AI hallucination | Wrong action | Tool-grounded evidence and deterministic controls |

## 28. Definition of Done

A feature is complete only when:

1. Code exists in the repository.
2. Database changes have migrations where required.
3. API contract is documented.
4. Tests exist.
5. Security implications are reviewed.
6. Frontend integration is complete where applicable.
7. CI passes.
8. Deployment is validated.
9. Logs/audit behavior is defined.
10. Rollback or failure behavior is understood.

## 29. Final Baseline Statement

As of 03 October 2026, NetPulse-AI has a substantial functional foundation covering customer management, GIS, MikroTik integration, OLT/SNMP foundation, authentication/RBAC, audit logging, frontend cockpit and CI/CD.

The main verified engineering blocker is the Docker build-context mismatch between the repository-root Alembic files and the current backend-only Docker build context. The persistent production backend must remain marked **not independently verified** until a provider deployment succeeds and its health endpoint is checked.

This blueprint is the engineering reference for the next implementation cycle and should be updated whenever the architecture, database, deployment model or production readiness state materially changes.
