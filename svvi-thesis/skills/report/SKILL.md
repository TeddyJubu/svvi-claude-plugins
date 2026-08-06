---
name: report
description: >-
  Generate a research briefing Claude artifact from a filtered slice of the SVVI
  corpus (platform, batch, search query, since/until). Use when the user asks for
  a report, briefing, memo, or summary of selected corpus docs.
argument-hint: "[platform=...] [batch=N] [query=...] [since=YYYY-MM-DD] [until=YYYY-MM-DD] [limit=N]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
compatibility: Requires synced local corpus/ and/or SVVI MCP. Prefer VPS-backed tools when connected.
version: 1.0.0
---

# /report — selected corpus research briefing

Produce a **research briefing** (not the full Prompt 1 pipeline) from a **filtered** corpus selection. Present the final briefing as a **Claude artifact**.

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
2. Build the selection (prefer **MCP** when connected so filters hit the live VPS corpus):

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

Omit empty flags. Use the JSON `files` list as the working set.

If `count` is 0, stop and tell the user to widen filters.

## Write the briefing

Create `reports/` if needed. Write:

`reports/briefing-YYYYMMDD-HHMM.md`

Use this structure:

```markdown
# SVVI briefing — <short theme>

- Generated: <ISO timestamp>
- Source: VPS corpus (plugin mirror / MCP)
- Filters: platform=…; batch=…; query=…; since=…; until=…; limit=…
- Documents: N

## Executive summary
3–6 sentences. Only what the selected docs support.

## Key takeaways
- …
- …

## Source notes
### 1. <title>
- File: `<filename>`
- Platform / date / url (if known)
- Relevance: one line
- Notable passages: 1–3 short quotes or tight paraphrases marked *(transcribed)* when from audio

(repeat per doc)

## Gaps & caveats
What the selection does **not** cover; filter bias.
```

**Hard rules**

- Only use selected documents. Do not invent quotes or sources outside the set.
- Prefer verbatim short quotes; truncate with ellipsis.
- Keep the briefing scannable (aim ~1–3 pages equivalent).

## Deliver as artifact

1. Save the markdown file.
2. **Present the briefing as a Claude artifact** in this chat (do not only paste a file path).
3. Reply with: filter summary, document count, and the `reports/…` path.
