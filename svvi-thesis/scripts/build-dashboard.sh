#!/usr/bin/env bash
# Rebuild ops dashboard HTML from VPS when corpus etag changes (or FORCE=1).
set -euo pipefail

ROOT="${CLAUDE_PLUGIN_ROOT:-}"
if [[ -z "$ROOT" ]]; then
  ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fi
export CLAUDE_PLUGIN_ROOT="$ROOT"

STATE_DIR="$ROOT/.svvi"
FORCE="${SVVI_DASHBOARD_FORCE:-${SVVI_SYNC_FORCE:-0}}"
mkdir -p "$STATE_DIR"

prev=""
if [[ -f "$STATE_DIR/dashboard.json" ]]; then
  prev="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("corpus_etag",""))' "$STATE_DIR/dashboard.json" 2>/dev/null || true)"
fi
curr=""
if [[ -f "$STATE_DIR/last-sync.json" ]]; then
  curr="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("etag",""))' "$STATE_DIR/last-sync.json" 2>/dev/null || true)"
fi

if [[ "$FORCE" != "1" && -n "$prev" && -n "$curr" && "$prev" == "$curr" && -f "$ROOT/dashboard/svvi-ops.html" ]]; then
  echo "svvi-dashboard: etag unchanged, keep existing artifact"
  echo "SVVI_DASHBOARD_ARTIFACT=$ROOT/dashboard/svvi-ops.html"
  echo "ACTION: Present the existing SVVI ops dashboard HTML artifact at $ROOT/dashboard/svvi-ops.html (VPS-synced)."
  exit 0
fi

exec python3 "$ROOT/scripts/render-dashboard.py"
