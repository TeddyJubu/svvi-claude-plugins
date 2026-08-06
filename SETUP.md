# SVVI setup — Claude Cowork (Desktop)

Cowork does **not** use `/plugin` slash commands. Use the Plugins UI.

## Easiest path: upload the zip (recommended)

1. Download the plugin:  
   **https://github.com/TeddyJubu/svvi-claude-plugins/releases/latest/download/svvi-thesis.zip**
2. Open **Cowork** (not Chat).
3. Sidebar → **Customize** → **Plugins**.
4. Click **Upload plugin** (or **+** → upload) → choose `svvi-thesis.zip`.
5. When asked for **SVVI MCP token**, paste the team token (from your admin / `SVVI_MCP_TOKEN`).
6. Open the installed plugin and confirm **skills** + **connector (`svvi`)** are enabled.
7. In a Cowork chat, ask:  
   `Call corpus_stats on the SVVI MCP`

You should see a document count.

- Health: https://srv1825737.hstgr.cloud/mcp-health  
- Viewer: https://srv1825737.hstgr.cloud/

---

## Alternative: add marketplace by URL

If you prefer browsing plugins:

1. **Customize** → **Plugins** → **+** → **Add marketplace**
2. Paste exactly:  
   `https://github.com/TeddyJubu/svvi-claude-plugins`
3. Install **svvi-thesis**
4. Paste the MCP token when prompted

Do **not** use `TeddyJubu/SVVI-fork` (private — install will fail).

---

## Claude Code (terminal / IDE only)

```text
/plugin marketplace add TeddyJubu/svvi-claude-plugins
/plugin install svvi-thesis@svvi-plugins
```

---

## Troubleshooting

| Problem | Fix |
| --- | --- |
| “Don’t find anything” / marketplace empty | Use **Upload plugin** with the zip above — don’t rely on slash commands in Cowork |
| Auth / clone failed | Use the public zip or `https://github.com/TeddyJubu/svvi-claude-plugins` |
| No MCP tools | Open plugin → enable the **svvi** connector; re-enter token |
| `401` | Wrong token — ask admin |
| Skills missing | Start a **new Cowork** session after install |
