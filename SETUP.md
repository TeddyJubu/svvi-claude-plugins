# SVVI setup — Claude Cowork (Desktop)

Your other tools (Notion, Attio, Drive, …) show up under **Customize → Connectors**. SVVI uses the same path.

## Get MCP tools (required — ~1 minute)

1. Ask an admin for the team **SVVI MCP token**.
2. Open **Cowork** → sidebar **Customize** → **Connectors**.
3. Click **+** → **Add custom connector** (wording may vary).
4. Fill in:
   - **Name:** `SVVI`
   - **URL:** paste this, with your token substituted:

```text
https://srv1825737.hstgr.cloud/mcp?token=PASTE_YOUR_TOKEN_HERE
```

5. Save / Connect until **SVVI** appears in the connectors list (alongside Notion, etc.).
6. Start a **new** Cowork chat and ask:

```text
Call corpus_stats on the SVVI MCP
```

You should see a document count.

- Health (no auth): https://srv1825737.hstgr.cloud/mcp-health  
- Viewer: https://srv1825737.hstgr.cloud/

---

## Local corpus mirror (plugin zip)

Install the plugin if you want **local `.md` files** (offline + open/cite) that stay in sync with the server:

1. Download:  
   **https://github.com/TeddyJubu/svvi-claude-plugins/releases/latest/download/svvi-thesis.zip**
2. **Customize** → **Plugins** → **Upload plugin** → choose the zip.
3. Paste the **same MCP token** when prompted for MCP, and once write it to the plugin `.svvi/token` file (ask Claude to run **sync-corpus** — it saves the token without putting it in a shell string).
4. Start a **new** session — SessionStart etag-checks the VPS, syncs markdown if needed, rebuilds the **ops dashboard** when data changed, and Claude should **present `svvi-ops.html` as an HTML artifact**. After any **fetch**, force-sync + rebuild dashboard so local matches the VPS (source of truth).
5. Manual refresh:

```bash
SVVI_SYNC_FORCE=1 bash "${CLAUDE_PLUGIN_ROOT}/scripts/sync-corpus.sh"
SVVI_DASHBOARD_FORCE=1 bash "${CLAUDE_PLUGIN_ROOT}/scripts/build-dashboard.sh"
```

Dashboard and `/report` HTML artifacts follow `plugins/svvi-thesis/references/DESIGN-apple.md` (Action Blue, parchment/tile rhythm, SF Pro).

Or ask: `Show the SVVI dashboard` (`/svvi-thesis:dashboard`).

### Research briefing from a corpus slice

`/svvi-thesis:report platform=blog query=regulation limit=12`

Filters: `platform`, `batch`, `query`, `since`, `until`, `limit`. Writes `reports/briefing-….md` and presents it as a Claude artifact. Uses MCP when connected; otherwise the local synced `corpus/`.

**Retention:** local `corpus/*.md` unused for about **90 days** (filesystem atime) are deleted on each sync. Opening/reading a file refreshes atime. If your disk is mounted `noatime`, run `touch -a` on files you cite.

Marketplace URL (public): `https://github.com/TeddyJubu/svvi-claude-plugins`  
Do **not** use `TeddyJubu/SVVI-fork` (private).

---

## Claude Code (terminal / IDE)

Bearer header (preferred over putting the token in the URL):

```json
{
  "mcpServers": {
    "svvi": {
      "type": "http",
      "url": "https://srv1825737.hstgr.cloud/mcp",
      "headers": {
        "Authorization": "Bearer PASTE_YOUR_TOKEN_HERE"
      }
    }
  }
}
```

Or install the plugin:

```text
/plugin marketplace add TeddyJubu/svvi-claude-plugins
/plugin install svvi-thesis@svvi-plugins
```

---

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Claude says “no SVVI MCP” / only Notion, Attio, … | **Connectors** step missing — add the custom connector URL above, then **new** chat |
| Connector fails to connect / `401` | Token wrong or missing from the URL (`?token=…`) |
| Token in URL feels sketchy | Prefer Claude Code / plugin with `Authorization: Bearer …` header |
| Local `corpus/` empty | Plugin + token required; force sync; check `svvi-sync:` lines on SessionStart |
| Skills missing | Upload the optional zip; start a new session |
| Private-repo marketplace errors | Use Connectors URL or the public zip / `svvi-claude-plugins` |
