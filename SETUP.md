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

## Optional: thesis skills (plugin zip)

Only if you also want `/svvi-thesis` skills and prompts:

1. Download:  
   **https://github.com/TeddyJubu/svvi-claude-plugins/releases/latest/download/svvi-thesis.zip**
2. **Customize** → **Plugins** → **Upload plugin** → choose the zip.
3. Paste the MCP token if asked (connector above already covers tools).
4. New session for skills to load.

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
| Skills missing | Upload the optional zip; start a new session |
| Private-repo marketplace errors | Use Connectors URL or the public zip / `svvi-claude-plugins` |
