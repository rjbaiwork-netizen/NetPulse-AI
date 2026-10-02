# NetPulse-AI Frontend Cockpit

## Implemented
- `/dashboard`: dark responsive NOC cockpit with device inventory summaries, alarm feed, and 15-second refresh.
- `/map`: browser-loaded Google Maps JS canvas with OLT, POP and ONU marker states: healthy, degraded, critical/LOS.
- `/ai-noc`: explicit natural-language command surface wired to existing FastAPI operations.
- `src/services/api.ts`: typed fetch client for device, MikroTik and OLT operations with structured errors.
- `src/services/maps.ts`: Google Maps loader with environment-based API key.
- Tailwind, PostCSS, ESLint and Next.js configuration for CI builds.

## Runtime configuration
Set:
- `NEXT_PUBLIC_API_BASE_URL`
- `NEXT_PUBLIC_GOOGLE_MAPS_API_KEY`

The GIS page currently includes representative markers because the backend Device model does not yet expose a dedicated geospatial inventory endpoint. Production marker hydration should consume latitude/longitude from device metadata or a dedicated GIS endpoint.

## Security and operational boundaries
- Credentials are not embedded in frontend code.
- Frontend actions call the existing FastAPI contract only.
- The AI command UI does not fabricate telemetry or claim hardware state when the API is unavailable.
- Voice transport remains provider-neutral until a selected browser speech/AI provider is integrated.

## Backend contract used
- `GET /api/v1/devices`
- `POST /api/v1/mikrotik/{id}/pppoe/kick`
- `POST /api/v1/mikrotik/{id}/pppoe/speed`
- `POST /api/v1/olt/onu/poll`

## Validation
GitHub Actions remains the authoritative build/test validation. Hardware-backed MikroTik/OLT connectivity is not implied by frontend build success.
