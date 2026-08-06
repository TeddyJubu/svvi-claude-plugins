# SVVI setup (Claude Code / Cowork)

## 1. Install the plugin

In Claude Code or Cowork, run:

```text
/plugin marketplace add TeddyJubu/svvi-claude-plugins
/plugin install svvi-thesis@svvi-plugins
```

## 2. Paste the token

When prompted for **SVVI MCP token**, paste the team token.

Get the token from an SVVI admin (or from the server: `SVVI_MCP_TOKEN` in `/opt/SVVI-fork/.env`). Never commit it.

## 3. Check it works

Ask Claude:

```text
Call corpus_stats on the SVVI MCP
```

You should see a document count. Optional links:

- Health: https://srv1825737.hstgr.cloud/mcp-health
- Viewer: https://srv1825737.hstgr.cloud/

## Commands after install

| Goal | Command |
| --- | --- |
| Prompt 1 | `/svvi-thesis:prompt-1` |
| Prompt 2 | `/svvi-thesis:prompt-2` |
| Full pipeline | `/svvi-thesis:run-thesis-pipeline` |
| Pending jobs | `/svvi-thesis:process-pending-jobs` |

## If install fails

- Use **`TeddyJubu/svvi-claude-plugins`** (public). Do **not** use private `SVVI-fork`.
- Restart the Claude session after install so skills load.
- `401` on MCP → wrong token; ask admin for a fresh one.
