---
name: dashboard
description: >-
  Present the SVVI ops dashboard as an interactive HTML Claude artifact with
  corpus charts synced from the VPS. Use on install, SessionStart notices,
  when the user asks for the SVVI dashboard/overview/charts, or after fetch sync.
compatibility: Requires svvi-thesis plugin, network to VPS, and .svvi/token or SVVI_MCP_TOKEN.
version: 1.0.0
---

# SVVI ops dashboard (Claude artifact)

VPS is the source of truth. The dashboard HTML is generated from
`https://srv1825737.hstgr.cloud/corpus/dashboard.json` using the Apple design
system in `${CLAUDE_PLUGIN_ROOT}/references/DESIGN-apple.md` (tokens baked into
`${CLAUDE_PLUGIN_ROOT}/dashboard/template.html`).

## Steps

1. Ensure token exists at `${CLAUDE_PLUGIN_ROOT}/.svvi/token` (or `SVVI_MCP_TOKEN`).
2. Rebuild from VPS:

```bash
SVVI_DASHBOARD_FORCE=1 bash "${CLAUDE_PLUGIN_ROOT}/scripts/build-dashboard.sh"
```

3. Read `${CLAUDE_PLUGIN_ROOT}/dashboard/svvi-ops.html` (or `svvi-ops-dashboard.html` in the working directory).
4. **Present it immediately as an interactive HTML artifact** in this Cowork chat (do not only link the path).
5. Briefly state totals (documents / top platform / whether schedules exist) from the embedded data.
6. Do **not** restyle the dashboard ad hoc — change `dashboard/template.html` / `DESIGN-apple.md` instead.
7. All visuals (including any extra charts or slides) must follow `${CLAUDE_PLUGIN_ROOT}/skills/design-system/SKILL.md`.

If the SessionStart hook already printed `SVVI_DASHBOARD_ARTIFACT=...`, skip rebuild unless the user asks to refresh or a fetch just completed.
