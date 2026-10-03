# NetPulse-AI Advanced Project Blueprint v1.1

**Live baseline:** 03 October 2026  
**Main commit:** 27147e3f4eb112fc45053438c99fc11f3df23341  
**Repository:** rjbaiwork-netizen/NetPulse-AI

## Executive Summary
NetPulse-AI is an ISP-focused NMS + Customer Network Management + GIS + AI-NOC platform. The current repository contains a FastAPI backend, Next.js operator cockpit, customer/GIS capabilities, MikroTik RouterOS integration, OLT/SNMP monitoring foundation, authentication/RBAC, audit logging, Alembic migrations and GitHub CI/CD.

## Live Verification
- Latest main: `27147e3f4eb112fc45053438c99fc11f3df23341`
- CI run `37090646760`: **SUCCESS**
- GitHub Pages run `37090646398`: **SUCCESS**
- NetPulse-AI Deploy run `37090646674`: **FAILURE**
- Repository permissions verified: admin, maintain, push, pull, triage.

## Current Blocking Issue
The production Docker validation fails because `backend/Dockerfile` copies root-level `alembic.ini` and `alembic/`, while the deployment workflow builds with `./backend` as the Docker context. The same context inconsistency is reflected in the current Render Blueprint configuration.

### Phase-0 repair
1. Build from repository root with `docker build -f backend/Dockerfile ... .`, or consistently relocate/package Alembic files under the backend context.
2. Align `render.yaml` with the chosen context.
3. Re-run CI and deployment validation against the resulting commit.

## Project Identity
- Type: ISP NMS + Customer Network Management + GIS + AI-NOC orchestration.
- Operators: NOC engineers, technicians and administrators.
- Core correlation: OLT → PON → ONU/ONT → Customer → PPPoE → MikroTik → telemetry → alarm/incident → AI-NOC.

## Purpose & Objectives
- Centralize customer and network inventory.
- Correlate customers with live MikroTik PPPoE sessions.
- Monitor MikroTik and OLT infrastructure.
- Provide GIS visibility and customer location history.
- Enable auditable AI-assisted diagnostics and controlled automation.
- Establish production-grade security, observability, backups and deployment.

## Explicit Non-Scope
Billing, invoice/payment processing, package/bandwidth billing, support-ticketing suites, HR/ERP and building-management modules are outside the intended platform scope.

## Current Architecture
```
Operator
  |
  v
Next.js Operator Cockpit -- Google Maps/GIS
  |
 HTTPS/JSON
  v
FastAPI
  +-- Auth/RBAC
  +-- Customer Management
  +-- Device Management
  +-- MikroTik RouterOS
  +-- OLT/SNMP
  +-- AI-NOC
       +-- PostgreSQL
       +-- MikroTik
       +-- OLT/ONU
       +-- GIS
```

## Current Domain Model
- **devices:** identity, type, host/port, encrypted credential, vendor, enablement and GIS metadata.
- **customers:** customer code, contact/address, PPPoE username, linked device, status and location.
- **customer_locations:** location history with accuracy/source/timestamp.
- **pppoe_profiles:** bandwidth/profile mapping.
- **alarms:** device alarms and severity/status.
- **incidents:** incident lifecycle and summaries.
- **audit_logs:** actor, role, action, target, success and detail.

## Current Capabilities
- FastAPI health/API layer.
- Customer CRUD and protected roles.
- Customer GPS capture/history.
- Customer ↔ PPPoE ↔ MikroTik live-session correlation.
- MikroTik connection, PPPoE secret/session inspection and controlled actions.
- OLT SNMP polling foundation and optical/fault classification.
- Device onboarding with live validation.
- JWT/bcrypt authentication and encrypted device secrets.
- Dashboard, devices, customers, customer profile, map, login and AI-NOC frontend routes.

## GIS
Device/customer coordinates, accuracy, source and timestamps are persisted. Current browser GPS is operator-side capture; it is not continuous customer live tracking. Continuous customer location would require a customer-side authenticated publisher plus consent/privacy controls.

## AI-NOC
Current AI-NOC is a structured intent/command layer, not an unrestricted LLM-to-router bridge. Production evolution should add evidence retrieval, RCA, recommendation generation, approval gates for disruptive actions, execution verification and audit trails.

## Security
Current foundation: admin/technician RBAC, JWT, bcrypt and encrypted device secrets. Future hardening: DB-backed user lifecycle, login throttling/lockout, refresh-token rotation, key rotation, device-network allowlists and SSRF-safe host validation.

## Repository Tree
```
NetPulse-AI/
├── .devcontainer/ (devcontainer.json, start.sh)
├── .github/workflows/ (ci.yml, deploy.yml)
├── README.md
├── alembic.ini
├── alembic/ (env.py, script.py.mako, versions/0001_device_geo_pop.py, 0002_customer_location.py)
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── api/ (ai_noc, auth, customers, dependencies, devices, mikrotik, olt)
│       ├── core/ (auth, database, security)
│       ├── models/ (alarm, audit_log, customer, device, profile)
│       ├── plugins/ (mikrotik/routeros_api, olt/snmp_poller)
│       ├── schemas/ (ai_noc, alarm, customer, device, mikrotik, olt, profile)
│       ├── services/ (mikrotik_service)
│       └── tests/
├── docs/ (API, ARCHITECTURE, AUTH_RBAC_GIS, DEVICE_TELEMETRY_API, FRONTEND_COCKPIT, PRODUCTION_DEPLOYMENT, PRODUCTION_HARDENING)
├── frontend/
│   └── src/app/ (ai-noc, customers, customers/profile, dashboard, devices, login, map)
└── render.yaml
```

## Technology Stack
Python 3.12, FastAPI, Uvicorn, SQLAlchemy 2.x, Alembic, Pydantic 2.x, PostgreSQL/psycopg, SQLite for CI/local, JWT/bcrypt, AES-GCM foundation, native RouterOS API, pysnmp, Next.js/TypeScript/Tailwind, Google Maps, GitHub Actions and GitHub Pages.

## Deployment
Target production architecture: GitHub Pages frontend → persistent HTTPS FastAPI → PostgreSQL → MikroTik/OLT/GIS/AI services. Codespaces and Actions runners are temporary/validation environments, not persistent backend hosting.

## Roadmap
1. **Phase 0:** Docker/Render packaging repair and green production-container validation.
2. **Phase 1:** Persistent backend, PostgreSQL, secrets, HTTPS, staging/production separation.
3. **Phase 2:** Polling scheduler, telemetry, latency/loss, traffic metrics and alarms.
4. **Phase 3:** OLT/PON/ONU/customer topology, vendor profiles, SNMPv3 and traps.
5. **Phase 4:** Customer impact calculation and advanced GIS.
6. **Phase 5:** AI-NOC evidence retrieval, RCA, approvals and verification.
7. **Phase 6:** Queues/workers, metrics, tracing, backup/DR and capacity testing.
8. **Phase 7:** UAT, security review, performance testing, rollback drill and controlled production release.

## Phase-0 Exit Criteria
- Reproducible production Docker build.
- Successful container startup.
- Successful `/health`.
- Successful Alembic migration.
- Green deployment workflow on the same main commit.
- GitHub Pages remains green and points to the intended backend.

## Final Baseline
This v1.1 blueprint reflects the repository state verified on 03 October 2026. The immediate engineering blocker is Docker build-context consistency; persistent production backend deployment should not be treated as verified until that issue and provider-side deployment are successfully validated.
