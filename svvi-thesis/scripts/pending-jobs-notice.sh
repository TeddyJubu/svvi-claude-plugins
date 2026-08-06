#!/usr/bin/env bash
# Print a one-line notice when pending schedule agent jobs exist.
set -euo pipefail

state_dir="${SVVI_STATE_DIR:-.state}"
jobs_dir="${state_dir}/schedules/jobs"

if [[ ! -d "$jobs_dir" ]]; then
  exit 0
fi

count=0
shopt -s nullglob
for f in "$jobs_dir"/job_*.json; do
  if grep -q '"status"[[:space:]]*:[[:space:]]*"pending"' "$f" 2>/dev/null; then
    count=$((count + 1))
  fi
done

if [[ "$count" -gt 0 ]]; then
  echo "${count} pending thesis jobs — run /svvi-thesis:process-pending-jobs"
fi
