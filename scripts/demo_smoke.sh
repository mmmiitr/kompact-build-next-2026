#!/usr/bin/env bash
# One-command smoke demo: health + publish-pack with a tiny sample clip.
# Usage (from repo root, with server already running OR this script starts it briefly):
#   ./scripts/demo_smoke.sh
# Env:
#   BASE=http://127.0.0.1:8000   (default)
#   START_SERVER=1              start uvicorn in background if health fails

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
BASE="${BASE:-http://127.0.0.1:8000}"
SAMPLE="${TMPDIR:-/tmp}/kompact-smoke-sample.mp4"
SERVER_PID=""

cleanup() {
  if [[ -n "${SERVER_PID}" ]] && kill -0 "$SERVER_PID" 2>/dev/null; then
    kill "$SERVER_PID" 2>/dev/null || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
  rm -f "$SAMPLE" 2>/dev/null || true
}
trap cleanup EXIT

make_sample() {
  if command -v ffmpeg >/dev/null 2>&1; then
    ffmpeg -y -hide_banner -loglevel error \
      -f lavfi -i color=c=blue:s=320x240:d=2 \
      -f lavfi -i sine=f=440:d=2 \
      -c:v libx264 -pix_fmt yuv420p -c:a aac -shortest \
      "$SAMPLE"
    echo "sample: ffmpeg lavfi → $SAMPLE"
    return 0
  fi

  # Minimal valid-ish tiny file fallback (not a real video; API still accepts bytes)
  # Prefer skipping with a clear note rather than faking a broken container.
  echo "NOTE: ffmpeg not found — cannot generate a real sample clip."
  echo "Install ffmpeg (for lavfi sample) or upload any short .mp4 via the UI."
  echo "Smoke will still hit /health; publish-pack skipped."
  return 1
}

ensure_server() {
  if curl -sf "$BASE/health" >/dev/null 2>&1; then
    echo "server: already up at $BASE"
    return 0
  fi
  if [[ "${START_SERVER:-0}" != "1" ]]; then
    echo "ERROR: no server at $BASE — start with:"
    echo "  uvicorn app.main:app --host 127.0.0.1 --port 8000"
    echo "Or re-run: START_SERVER=1 $0"
    exit 1
  fi
  # Prefer venv if present
  PY="${ROOT}/.venv/bin/python"
  UV="${ROOT}/.venv/bin/uvicorn"
  if [[ ! -x "$UV" ]]; then
    UV="uvicorn"
  fi
  echo "starting: $UV app.main:app --host 127.0.0.1 --port 8000"
  "$UV" app.main:app --host 127.0.0.1 --port 8000 &
  SERVER_PID=$!
  for i in $(seq 1 30); do
    if curl -sf "$BASE/health" >/dev/null 2>&1; then
      echo "server: ready"
      return 0
    fi
    sleep 0.3
  done
  echo "ERROR: server failed to become healthy"
  exit 1
}

echo "=== Kompact Social Content Helper — smoke demo ==="
ensure_server

echo "--- GET /health ---"
curl -sS "$BASE/health" | python3 -m json.tool

if ! make_sample; then
  echo "=== smoke partial OK (health only) ==="
  exit 0
fi

echo "--- POST /api/publish-pack ---"
RESP="$(curl -sS -X POST "$BASE/api/publish-pack" \
  -F "video=@${SAMPLE};type=video/mp4" \
  -F "prompt=2s smoke demo for indie founders on CPU budgets")"

echo "$RESP" | python3 -m json.tool

MODE="$(echo "$RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('mode',''))")"
DUR="$(echo "$RESP" | python3 -c "import sys,json; v=json.load(sys.stdin).get('video',{}); print(v.get('duration_seconds'), v.get('duration_source'), v.get('width'), v.get('height'), v.get('codec'))")"
echo "mode=$MODE  video_meta=$DUR"
echo "=== smoke OK ==="
