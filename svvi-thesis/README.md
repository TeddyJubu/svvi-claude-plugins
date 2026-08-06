# SVVI Thesis Plugin

Claude Code / Cowork plugin for the SVVI investment-thesis workflow, plus the **hosted corpus MCP**.

1. **Prompt 1** — extract every forward-looking AI statement from a Markdown corpus
2. **Prompt 2** — synthesize consensus points, high-conviction signals, and thesis-slide bullets
3. **Full pipeline** — Prompt 1 → Prompt 2
4. **Pending jobs** — claim Prompt 1/2 jobs enqueued by `svvi-scheduler`
5. **Hosted MCP** — `corpus_*`, `fetch_run`, schedules/jobs against `https://srv1825737.hstgr.cloud/mcp`

## Install (team — recommended)

See the short guide: [../SETUP.md](../SETUP.md)

```text
/plugin marketplace add TeddyJubu/svvi-claude-plugins
/plugin install svvi-thesis@svvi-plugins
```

When prompted for **SVVI MCP token**, paste the shared team token (ask an admin). Never commit it.

Or:

```bash
# (optional) see SETUP.md
```

## Install (local plugin dir)

```bash
claude --plugin-dir /absolute/path/to/SVVI-fork/plugins/svvi-thesis
```

You still need MCP auth — use the token prompt if present, or the fallback JSON in [SETUP.md](../SETUP.md).

## Slash commands

| Command | What it does |
| --- | --- |
| `/svvi-thesis:prompt-1 [corpus-dir]` | Run Prompt 1 only |
| `/svvi-thesis:prompt-2 [input-report]` | Run Prompt 2 only |
| `/svvi-thesis:run-thesis-pipeline [corpus-dir]` | Run Prompt 1 → Prompt 2 |
| `/svvi-thesis:process-pending-jobs` | Claim + run pending scheduled Prompt jobs |

Bare names (`/prompt-1`, …) may work depending on the client.

## Expected project layout (skills writing local files)

```text
your-project/
├── output/                          # Markdown corpus (optional if using MCP only)
├── .state/schedules/                # jobs from svvi-scheduler / MCP
├── prompt 1/
│   └── forward-looking-statements.md
└── prompt 2/
    └── thesis-synthesis.md
```

If you only use remote MCP tools (search/fetch/stats), you do not need a local `output/` tree.

## Scheduled jobs flow

1. Create a schedule in the Viewer **Schedules** UI or via MCP `schedule_create`.
2. Scheduler / **Run now** executes fetches and enqueues Prompt jobs.
3. Open Claude with this plugin — SessionStart notices pending jobs.
4. Run `/svvi-thesis:process-pending-jobs`.

## Auto skills

- `forward-looking-thesis-extraction` (Prompt 1)
- `investment-thesis-synthesis` (Prompt 2)
- `thesis-pipeline` (both)
- `process-pending-jobs` (scheduled queue)

## Requirements

- Claude Code or Cowork with plugin support
- Team MCP bearer token (prompted at enable; also called `SVVI_MCP_TOKEN` on the server)
- Python 3 only if running the Prompt 1 manifest helper locally

## Plugin layout

```text
svvi-thesis/
├── .claude-plugin/plugin.json   # manifest + userConfig (MCP token)
├── .mcp.json                    # hosted SVVI MCP
├── hooks/hooks.json
├── scripts/pending-jobs-notice.sh
├── references/
└── skills/
```

## Notes

- Skills refuse to invent quotes or outside knowledge.
- Deliverables are Markdown files — chat alone is not the source of truth.
- The plugin does not modify fetch/app code in host projects.
