# SVVI Claude plugin setup

Install in Claude Code or Cowork (works in cloud sandboxes — this repo is **public**):

```text
/plugin marketplace add TeddyJubu/svvi-claude-plugins
/plugin install svvi-thesis@svvi-plugins
```

When prompted for **SVVI MCP token**, paste the shared team bearer token (ask an SVVI admin). Never commit the token.

Then:

1. Open `/mcp` and confirm `svvi` is connected
2. Ask: “Call `corpus_stats` on the SVVI MCP”
3. Health check (no auth): https://srv1825737.hstgr.cloud/mcp-health
4. Viewer: https://srv1825737.hstgr.cloud/

## CLI

```bash
claude plugin marketplace add TeddyJubu/svvi-claude-plugins
claude plugin install svvi-thesis@svvi-plugins
```

## What you get

| Piece | Detail |
| --- | --- |
| Skills / slash commands | Prompt 1, Prompt 2, pipeline, process-pending-jobs |
| Hosted MCP | `https://srv1825737.hstgr.cloud/mcp` |
| Auth | Bearer token prompted at enable (`userConfig`) |

## Manual MCP fallback

```bash
export SVVI_MCP_TOKEN='paste-token-here'
claude mcp add --transport http \
  --header "Authorization: Bearer ${SVVI_MCP_TOKEN}" \
  svvi https://srv1825737.hstgr.cloud/mcp
```

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| HTTPS auth / clone failed | Use this repo (`TeddyJubu/svvi-claude-plugins`), not the private `SVVI-fork` |
| 401 on MCP | Wrong/expired token — ask admin |
| Plugin failed to load | Update Claude Code; reinstall plugin |

Source of truth for the fetch app remains private: `TeddyJubu/SVVI-fork`. This repo is the install surface only.
