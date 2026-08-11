#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

export NEXT_PUBLIC_API_URL="${NEXT_PUBLIC_API_URL:-http://127.0.0.1:8000}"

cleanup() {
  kill "${BACKEND_PID:-}" "${UI_PID:-}" 2>/dev/null || true
}

trap cleanup EXIT INT TERM

echo "Starting PostgreSQL..."
docker compose up -d

echo "Starting backend..."
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "& {
  Set-Location '$ROOT_DIR\\backend'
  . .\.venv\Scripts\Activate.ps1
  python run.py
}" &
BACKEND_PID=$!

sleep 5

echo "Starting UI..."
(
  cd "$ROOT_DIR/ui"
  npm run dev
) &
UI_PID=$!

echo "Backend: http://127.0.0.1:8000"
echo "UI:      http://localhost:3000"

wait
