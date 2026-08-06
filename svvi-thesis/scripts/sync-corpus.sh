#!/usr/bin/env bash
# Sync hosted SVVI corpus markdown into the plugin, then prune stale locals by atime.
# Auth: SVVI_MCP_TOKEN, ${user_config.mcp_token} (via hooks), or $CLAUDE_PLUGIN_ROOT/.svvi/token
set -euo pipefail

ROOT="${CLAUDE_PLUGIN_ROOT:-}"
if [[ -z "$ROOT" ]]; then
  ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fi

CORPUS_DIR="${SVVI_LOCAL_CORPUS_DIR:-$ROOT/corpus}"
STATE_DIR="$ROOT/.svvi"
BASE_URL="${SVVI_BASE_URL:-https://srv1825737.hstgr.cloud}"
MANIFEST_URL="${SVVI_CORPUS_MANIFEST_URL:-$BASE_URL/corpus/manifest.json}"
TARBALL_URL="${SVVI_CORPUS_TARBALL_URL:-$BASE_URL/corpus.tar.gz}"
MIN_INTERVAL_SEC="${SVVI_SYNC_MIN_INTERVAL_SEC:-0}"
PRUNE_DAYS="${SVVI_CORPUS_PRUNE_DAYS:-90}"
FORCE="${SVVI_SYNC_FORCE:-0}"

mkdir -p "$CORPUS_DIR" "$STATE_DIR"

TOKEN="${SVVI_MCP_TOKEN:-}"
if [[ -z "$TOKEN" && -n "${1:-}" ]]; then
  TOKEN="$1"
fi
if [[ -z "$TOKEN" && -f "$STATE_DIR/token" ]]; then
  TOKEN="$(tr -d '[:space:]' <"$STATE_DIR/token")"
fi
if [[ -z "$TOKEN" ]]; then
  echo "svvi-sync: no token (set SVVI_MCP_TOKEN or $STATE_DIR/token)" >&2
  exit 0
fi

# Persist token for later sessions / prune-only runs (plugin-local, gitignored).
umask 077
printf '%s\n' "$TOKEN" >"$STATE_DIR/token"

now="$(date +%s)"
last_file="$STATE_DIR/last-sync.json"
# Optional cooldown (default 0): VPS is source of truth — always etag-check unless set.
if [[ "$FORCE" != "1" && "$MIN_INTERVAL_SEC" =~ ^[0-9]+$ ]] && (( MIN_INTERVAL_SEC > 0 )) && [[ -f "$last_file" ]]; then
  last_ts="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("synced_at",0))' "$last_file" 2>/dev/null || echo 0)"
  if [[ "$last_ts" =~ ^[0-9]+$ ]] && (( now - last_ts < MIN_INTERVAL_SEC )); then
    echo "svvi-sync: skipped (synced $((now - last_ts))s ago; set SVVI_SYNC_MIN_INTERVAL_SEC=0 to always etag-check)"
    exit 0
  fi
fi

auth_args=(-H "Authorization: Bearer ${TOKEN}")
# Also allow ?token= fallbacks if Bearer is stripped by an intermediary
manifest_q="${MANIFEST_URL}"
tarball_q="${TARBALL_URL}"
if [[ "$MANIFEST_URL" != *"?"* ]]; then
  manifest_q="${MANIFEST_URL}?token=${TOKEN}"
fi
if [[ "$TARBALL_URL" != *"?"* ]]; then
  tarball_q="${TARBALL_URL}?token=${TOKEN}"
fi

hdrs="$(mktemp)"
manifest_tmp="$(mktemp)"
trap 'rm -f "$hdrs" "$manifest_tmp" "${tarball_tmp:-}"' EXIT

code="$(
  curl -sS -L \
    -D "$hdrs" \
    -o "$manifest_tmp" \
    -w '%{http_code}' \
    "${auth_args[@]}" \
    "$MANIFEST_URL" || true
)"
if [[ "$code" != "200" && "$code" != "304" ]]; then
  code="$(
    curl -sS -L \
      -D "$hdrs" \
      -o "$manifest_tmp" \
      -w '%{http_code}' \
      "$manifest_q" || true
  )"
fi
if [[ "$code" != "200" && "$code" != "304" ]]; then
  echo "svvi-sync: manifest HTTP $code" >&2
  exit 1
fi

etag="$(awk 'BEGIN{IGNORECASE=1} /^ETag:/{sub(/\r$/,""); sub(/^ETag:[[:space:]]*/,""); print; exit}' "$hdrs")"
etag="${etag#\"}"; etag="${etag%\"}"
prev_etag=""
if [[ -f "$last_file" ]]; then
  prev_etag="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("etag","").strip("\""))' "$last_file" 2>/dev/null || true)"
fi

downloaded=0
if [[ "$FORCE" == "1" || "$code" == "200" && "$etag" != "$prev_etag" ]]; then
  tarball_tmp="$(mktemp)"
  curl_extra=()
  if [[ "$FORCE" != "1" && -n "$prev_etag" ]]; then
    curl_extra+=(-H "If-None-Match: \"${prev_etag}\"")
  fi
  tcode="$(
    curl -sS -L \
      -o "$tarball_tmp" \
      -w '%{http_code}' \
      "${auth_args[@]}" \
      "${curl_extra[@]}" \
      "$TARBALL_URL" || true
  )"
  if [[ "$tcode" == "304" ]]; then
    echo "svvi-sync: tarball unchanged (304)"
  elif [[ "$tcode" != "200" ]]; then
    tcode="$(
      curl -sS -L \
        -o "$tarball_tmp" \
        -w '%{http_code}' \
        "$tarball_q" || true
    )"
  fi
  if [[ "$tcode" == "200" ]]; then
    extract_tmp="$(mktemp -d)"
    trap 'rm -f "$hdrs" "$manifest_tmp" "${tarball_tmp:-}"; rm -rf "${extract_tmp:-}"' EXIT
    tar -xzf "$tarball_tmp" -C "$extract_tmp"
    # Merge: only replace when content differs so unchanged local atime is preserved.
    shopt -s nullglob
    for src in "$extract_tmp"/*.md; do
      base="$(basename "$src")"
      dest="$CORPUS_DIR/$base"
      if [[ -f "$dest" ]] && cmp -s "$src" "$dest"; then
        continue
      fi
      cp -f "$src" "$dest"
    done
    downloaded=1
    count="$(find "$extract_tmp" -maxdepth 1 -type f -name '*.md' | wc -l | tr -d ' ')"
    echo "svvi-sync: merged ${count} remote markdown files into $CORPUS_DIR"
  elif [[ "$tcode" != "304" ]]; then
    echo "svvi-sync: tarball HTTP $tcode" >&2
    exit 1
  fi
else
  echo "svvi-sync: etag unchanged, skip download"
fi

# Auto-delete local markdown not accessed for ~PRUNE_DAYS (POSIX find atime).
# find -atime +N means strictly more than N*24h ago; use N=PRUNE_DAYS-1 so
# "90 days unused" deletes once age reaches 90 days rather than 91+.
pruned=0
if [[ "$PRUNE_DAYS" =~ ^[0-9]+$ ]] && (( PRUNE_DAYS > 0 )); then
  atime_plus=$((PRUNE_DAYS - 1))
  while IFS= read -r -d '' stale; do
    rm -f "$stale"
    pruned=$((pruned + 1))
  done < <(find "$CORPUS_DIR" -maxdepth 1 -type f -name '*.md' -atime "+${atime_plus}" -print0 2>/dev/null || true)
fi

remote_etag="$etag"
if [[ -z "$remote_etag" && -f "$manifest_tmp" ]]; then
  remote_etag="$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1])).get("etag","").strip("\""))' "$manifest_tmp" 2>/dev/null || true)"
fi

python3 - "$last_file" "$remote_etag" "$now" "$downloaded" "$pruned" "$CORPUS_DIR" <<'PY'
import json, sys, pathlib
path, etag, now, downloaded, pruned, corpus = sys.argv[1:7]
local = len(list(pathlib.Path(corpus).glob("*.md")))
pathlib.Path(path).write_text(json.dumps({
    "synced_at": int(now),
    "etag": etag,
    "downloaded": downloaded == "1",
    "pruned": int(pruned),
    "local_md_count": local,
    "corpus_dir": corpus,
}, indent=2) + "\n")
print(f"svvi-sync: done local_md={local} pruned={pruned}")
PY
