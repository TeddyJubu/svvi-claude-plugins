---
name: sync-corpus
description: >-
  Download/refresh the hosted SVVI Markdown corpus into the plugin local
  corpus/ folder and prune .md files not accessed for 90+ days. Use on install,
  after every fetch_run/schedule_run that writes docs, when local files look
  stale, or when the user asks to sync/update the corpus. VPS is source of truth.
compatibility: Requires network access to srv1825737.hstgr.cloud and the SVVI MCP token.
version: 1.1.0
---

# Sync local SVVI corpus (VPS is source of truth)

Local `corpus/` is a **mirror**. Never invent or keep stale content when the host has moved on.

## When to run

- SessionStart hook (etag check; downloads only if VPS changed)
- **Immediately after** any successful MCP `fetch_run` or `schedule_run` that may have written docs (read `local_sync_hint` / `corpus_etag` in the tool JSON)
- When Prompt 1 needs fresh local files
- When the user asks to sync/update the corpus

## How

1. Ensure the MCP token is available (`userConfig.mcp_token`, `SVVI_MCP_TOKEN`, or `${CLAUDE_PLUGIN_ROOT}/.svvi/token`).
2. Force pull from VPS:

```bash
SVVI_SYNC_FORCE=1 bash "${CLAUDE_PLUGIN_ROOT}/scripts/sync-corpus.sh"
```

3. Tell the user:
   - Local path: `${CLAUDE_PLUGIN_ROOT}/corpus/`
   - Auto-prune: local `*.md` with filesystem **atime** older than **90 days** are deleted
   - Opening/reading a file refreshes atime (`touch -a` if the mount uses `noatime`)
4. Prefer synced `corpus/` for Prompt 1; use MCP for live search/stats.

Do not commit `corpus/` or `.svvi/token`.
