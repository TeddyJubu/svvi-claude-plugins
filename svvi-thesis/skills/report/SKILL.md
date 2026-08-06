---
name: report
description: >-
  Generate a research briefing Claude artifact from a filtered slice of the SVVI
  corpus (platform, batch, search query, since/until). Use when the user asks for
  a report, briefing, memo, or summary of selected corpus docs.
argument-hint: "[platform=...] [batch=N] [query=...] [since=YYYY-MM-DD] [until=YYYY-MM-DD] [limit=N]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
compatibility: Requires synced local corpus/ and/or SVVI MCP. Prefer VPS-backed tools when connected.
version: 1.1.0
---

# /report — selected corpus research briefing

Produce a **research briefing** from a **filtered** corpus selection and present it as an **HTML Claude artifact** styled with the Apple design system.

## Design system (required)

1. Read `${CLAUDE_PLUGIN_ROOT}/references/DESIGN-apple.md`.
2. Follow `${CLAUDE_PLUGIN_ROOT}/skills/design-system/SKILL.md` for **all** visual output.
3. Start from `${CLAUDE_PLUGIN_ROOT}/dashboard/report-template.html` — **keep its CSS/tokens unchanged**.
4. Fill only the `__REPORT_*__` placeholders (or equivalent content slots). Do **not** introduce a second accent color, decorative gradients, card shadows, or non-system fonts.

Non-negotiables from the design system:

- Action Blue `#0066cc` is the only interactive color (use `#2997ff` only on dark tiles).
- Surfaces: white / parchment `#f5f5f7` / near-black `#272729`, alternating as section tiles.
- SF Pro / system-ui / Inter substitute; body 17px / 400 / 1.47; display headlines weight 600.
- No UI chrome shadows; utility source cards use 18px radius + hairline only.

## Arguments

Parse `$ARGUMENTS` as optional `key=value` tokens (space-separated):

| Key | Meaning | Example |
| --- | --- | --- |
| `platform` | `blog` \| `youtube` \| `twitter` \| `apple` \| `unknown` | `platform=blog` |
| `batch` | integer batch id | `batch=4` |
| `query` | case-insensitive substring across title/body | `query=regulation` |
| `since` / `until` | content date `YYYY-MM-DD` inclusive | `since=2026-08-01` |
| `limit` | max docs (default 15, hard max 40) | `limit=12` |

If `$ARGUMENTS` is empty, ask the user which filters to apply (do not dump the whole corpus).

## Selection (VPS is source of truth)

1. If local `${CLAUDE_PLUGIN_ROOT}/corpus` looks empty/stale, sync first (`sync-corpus` skill).
2. Build the selection (prefer **MCP** when connected):

**Preferred — MCP**

- `corpus_select` and/or `corpus_search` with the same filters
- `corpus_get` for each chosen filename (respect `limit`)

**Fallback — local mirror**

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/select-corpus.py" \
  --platform "$PLATFORM" \
  --batch "$BATCH" \
  --query "$QUERY" \
  --since "$SINCE" \
  --until "$UNTIL" \
  --limit "$LIMIT" \
  --excerpt-chars 1500
```

Omit empty flags. If `count` is 0, stop and tell the user to widen filters.

## Fill the HTML template

Copy `dashboard/report-template.html` → `reports/briefing-YYYYMMDD-HHMM.html` and replace:

| Placeholder | Content |
| --- | --- |
| `__REPORT_TITLE__` | Short theme title (also used in `<title>`) |
| `__REPORT_LEDE__` | One sentence under the hero |
| `__REPORT_FILTERS__` | Compact filter + doc-count line for the sub-nav |
| `__REPORT_SUMMARY__` | 3–6 sentence executive summary (plain text/HTML paragraphs) |
| `__REPORT_TAKEAWAYS__` | `<li>…</li>` items only |
| `__REPORT_SOURCES__` | Repeated `.source` blocks (see template) with title, meta, quotes |
| `__REPORT_GAPS__` | Short caveats paragraph(s) |
| `__REPORT_FOOTER__` | Generated timestamp + “VPS corpus · N sources” |

**Hard rules**

- Only use selected documents. Do not invent quotes or sources outside the set.
- Prefer short verbatim quotes inside `<blockquote>`; mark transcribed speech *(transcribed)*.
- Keep the briefing scannable.

Also write a plain-text twin at `reports/briefing-YYYYMMDD-HHMM.md` if useful for editing — but **the artifact presented to the user must be the HTML**.

## Deliver as artifact

1. Save the HTML file under `reports/`.
2. **Present the HTML as a Claude artifact** in this chat (do not only link the path).
3. Reply with: filter summary, document count, and the `reports/….html` path.
