#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
API_DIR="$ROOT_DIR/apps/api"
WEB_DIR="$ROOT_DIR/apps/web"

if [[ ! -x "$ROOT_DIR/.venv/bin/python" ]]; then
  echo "Missing venv at $ROOT_DIR/.venv" >&2
  echo "Create it first: python -m venv .venv && source .venv/bin/activate" >&2
  exit 1
fi

export PATH="$ROOT_DIR/.venv/bin:$PATH"

echo "Installing backend (editable)…"
pip install -e "$API_DIR[dev]" >/dev/null

echo "Installing frontend deps…"
npm --prefix "$WEB_DIR" install >/dev/null

# Optional: if the user didn't create .env.local yet, fall back to local API.
export API_BASE_URL="${API_BASE_URL:-http://127.0.0.1:8000}"

echo "Starting API (uvicorn --reload) on http://127.0.0.1:8000 …"
cd "$API_DIR"
uvicorn procuator.api.app:app --host 127.0.0.1 --port 8000 --reload &
API_PID=$!

echo "Starting web (next dev) on http://127.0.0.1:3000 …"
cd "$WEB_DIR"
API_BASE_URL="$API_BASE_URL" npm run dev &
WEB_PID=$!

cleanup() {
  echo "\nStopping…"
  kill "$WEB_PID" 2>/dev/null || true
  kill "$API_PID" 2>/dev/null || true
}
trap cleanup EXIT

wait "$API_PID" "$WEB_PID"
