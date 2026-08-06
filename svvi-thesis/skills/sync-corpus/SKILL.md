---
name: sync-corpus
description: >-
  Download/refresh the hosted SVVI Markdown corpus into the plugin local
  corpus/ folder and prune .md files not accessed for 90+ days. Use on install,
  when local files look stale, or when the user asks to sync/update the corpus.
compatibility: Requires network access to srv1825737.hstgr.cloud and the SVVI MCP token.
version: 1.0.0
---

# Sync local SVVI corpus

1. Ensure the MCP token is available:
   - Plugin `userConfig.mcp_token`, or
   - Env `SVVI_MCP_TOKEN`, or
   - Write the token once to `${CLAUDE_PLUGIN_ROOT}/.svvi/token`
2. Force a sync:

```bash
SVVI_SYNC_FORCE=1 SVVI_MCP_TOKEN='…' bash "${CLAUDE_PLUGIN_ROOT}/scripts/sync-corpus.sh"
```

3. Tell the user:
   - Local corpus path: `${CLAUDE_PLUGIN_ROOT}/corpus/`
   - Auto-prune: local `*.md` with filesystem **atime** older than **90 days** are deleted
   - Opening/reading a file refreshes atime (prefer `touch -a` after citing if the mount uses `noatime`)
4. Prefer this local folder for Prompt 1 (`--output-dir` / corpus-dir) when it contains `.md` files; keep using the SVVI MCP for search/stats when live index is needed.

Do not commit `corpus/` or `.svvi/token`.
