#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel)"
BACKEND_LOG="/tmp/netpulse-backend.log"
FRONTEND_LOG="/tmp/netpulse-frontend.log"

cd "$ROOT"

# GitHub Codespaces provides these values dynamically for each codespace.
DOMAIN="${GITHUB_CODESPACES_PORT_FORWARDING_DOMAIN:-app.github.dev}"
NAME="${CODESPACE_NAME:-}"
if [[ -n "$NAME" ]]; then
  BACKEND_URL="https://${NAME}-8000.${DOMAIN}"
  FRONTEND_URL="https://${NAME}-3000.${DOMAIN}"
else
  BACKEND_URL="http://127.0.0.1:8000"
  FRONTEND_URL="http://127.0.0.1:3000"
fi

# Keep local development origins and add the current Codespaces frontend origin.
export NETPULSE_CORS_ORIGINS="${NETPULSE_CORS_ORIGINS:-https://rjbaiwork-netizen.github.io,http://localhost:3000}"
if [[ -n "$NAME" ]]; then
  export NETPULSE_CORS_ORIGINS="${NETPULSE_CORS_ORIGINS},${FRONTEND_URL}"
fi

# Start FastAPI only if port 8000 is not already serving.
if ! (echo >/dev/tcp/127.0.0.1/8000) >/dev/null 2>&1; then
  (
    cd "$ROOT/backend"
    nohup python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 >"$BACKEND_LOG" 2>&1 &
  )
fi

# Start the Next.js development server only if port 3000 is not already serving.
if ! (echo >/dev/tcp/127.0.0.1/3000) >/dev/null 2>&1; then
  (
    cd "$ROOT/frontend"
    export NEXT_PUBLIC_API_BASE_URL="$BACKEND_URL"
    nohup npm run dev -- --hostname 0.0.0.0 --port 3000 >"$FRONTEND_LOG" 2>&1 &
  )
fi

echo "NetPulse-AI Codespaces services starting..."
echo "FastAPI:  $BACKEND_URL"
echo "Frontend: $FRONTEND_URL"
echo "Health:   $BACKEND_URL/health"
echo "Logs:     $BACKEND_LOG and $FRONTEND_LOG"
echo
echo "If authentication is not configured, set NETPULSE_JWT_SECRET,"
echo "NETPULSE_ENCRYPTION_KEY, NETPULSE_ADMIN_USERNAME and"
echo "NETPULSE_ADMIN_PASSWORD_HASH as Codespaces secrets/env vars."
