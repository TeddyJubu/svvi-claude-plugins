---
name: forward-looking-thesis-extraction
description: >-
  Runs the Prompt 1 four-step workflow to extract every forward-looking AI
  statement from a Markdown corpus into an investment-thesis deliverable.
  Use whenever the user mentions Prompt 1, forward-looking statements, AI
  thesis extraction, corpus thesis mining, co-investment thesis slides, Full
  Thesis Docs, predictions about AI from blogs/podcasts/Twitter, or processing
  output/*.md for investment insights — even if they do not say "skill".
compatibility: Requires Python 3 for the bundled manifest script. Read/write access to the working project's corpus and deliverable folders.
version: 1.0.0
---

# Forward-Looking Thesis Extraction (Prompt 1)

Act as a rigorous investment research analyst at an AI-focused venture capital firm. Extract specific, forward-looking statements and predictions about AI and the AI industry from **every** corpus document. Outputs feed an AI investment thesis slide for a co-investment directs fund deck.

**Hard constraints**
- Do **not** modify unrelated application code, tests, config, or fetch pipelines.
- Only write under the deliverable folder `prompt 1/` (overwriting the deliverable is expected).
- Only extract what is explicitly stated. Do not infer, extrapolate, or fabricate.
- Process **every** `.md` file in the corpus. Never silently skip a file.

## Working-project layout

Resolve the **project root** as the user's current working project (directory that should contain the corpus and deliverable folders). Create `prompt 1/` if missing.

| Role | Default path (from project root) |
| --- | --- |
| Corpus | `output/` |
| Deliverable | `prompt 1/forward-looking-statements.md` |
| Canonical reference | `${CLAUDE_PLUGIN_ROOT}/references/prompt-1.md` |
| Manifest helper | `${CLAUDE_PLUGIN_ROOT}/skills/forward-looking-thesis-extraction/scripts/build_manifest.py` |

If the user passes a different corpus path, use that instead of `output/`.

If `${CLAUDE_PLUGIN_ROOT}/corpus/` exists and contains `.md` files (from `sync-corpus`), prefer that path over `output/` unless the user overrode the corpus directory.

## Source-type mapping

Corpus is flat Markdown; type comes from YAML frontmatter `platform:` when present:

| `platform` | Content type | Quote handling |
| --- | --- | --- |
| `blog` | Blogs | Clean long-form. Extract **verbatim**. |
| `youtube` or `apple` | Podcast Transcript | Closest verbatim quote + *(transcribed speech)*. Prefer transcript timestamps (e.g. `[12:34]`). |
| `twitter` | Twitter | Full post is often the quote. Note platform in metadata. |

Ignore non-documents (e.g. `.gitkeep`).

## Progress checklist

Copy and track:

```text
Prompt 1 Progress:
- [ ] Step 0 — Processing manifest
- [ ] Step 1 — Source metadata (every file)
- [ ] Step 2 — Forward-looking statements (every file)
- [ ] Step 3 — Processing summary + write deliverable
```

Complete steps **in order**. Do not skip ahead.

---

## Step 0 — Processing manifest

Before extraction, inventory the corpus.

1. From the project root, run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/forward-looking-thesis-extraction/scripts/build_manifest.py" --output-dir output
```

2. Put the script’s listing into the deliverable under `## STEP 0 — PROCESSING MANIFEST` using this shape:

```text
Blogs (platform: blog): [filename 1], [filename 2]...
Podcast Transcripts (platform: youtube | apple): [filename 1]...
Twitter (platform: twitter): [filename 1]...
Other / Unknown platforms: [filename (platform: ...)] or (none)
Unreadable: [filename] or (none)
```

3. Every filename listed here **must** appear later in Steps 1–2. Treat this as the checklist — including Other/Unknown and Unreadable entries (still emit metadata + reason for unreadable files).

If the script exits non-zero because of unknown/unreadable files, keep those filenames in the Step 0 checklist and still process every readable file. If the script fails entirely, fall back to listing `output/*.md` and grouping by frontmatter `platform:`. Do not invent filenames.

---

## Step 1 — Source metadata *(repeat for each document)*

For **each** file in the Step 0 manifest, open the file and extract:

- **Author/Speaker:**
- **Source name/publication/platform:**
- **Content type:** [Blogs / Podcast Transcript / Twitter]
- **Date (if available):**
- **Author's role:** [e.g., GP at XYZ Fund, AI researcher, founder — only if stated or clearly identifiable; otherwise `Unknown`]
- **File:** [exact filename under the corpus]
- **URL:** [from frontmatter if present]

Prefer YAML frontmatter + header fields. Fill unknowns as `Unknown`.

---

## Step 2 — Forward-looking statements *(repeat for each document)*

For each forward-looking statement or prediction in the document, emit a standalone block:

**Thesis Statement:** [One punchy declarative sentence suitable for an investment thesis slide. Example: "Agentic AI will replace entire software workflows, not just individual tasks."]

**Supporting Quote:** "[Exact verbatim quote]" — Author/Speaker, Date *(add *(transcribed speech)* for Podcast Transcript)*

Rules:
- Extract **every** forward-looking statement — no min/max.
- Pair every thesis with an exact verbatim quote, who said it, and timestamp if available.
- Thesis language: clear, accessible; avoid jargon/acronyms/overly technical phrasing. Sophisticated investor audience — use business/market implications for technical concepts.
- Attribute every insight to its specific author and source.
- Each block stands alone — do not group or nest them.
- If none exist, still keep the full metadata block and write exactly:

`[No forward-looking statements found in this source]`

Read file contents before extracting quotes. Use shell for bulk inventory when helpful; never invent quotes.

---

## Step 3 — Processing summary + write deliverable

After all documents, write:

- **Total documents processed:**
- **Documents with forward-looking statements:** [count]
- **Documents with no forward-looking statements:** [list filenames]
- **Any documents that could not be read or accessed:** [list filenames + reason]

Then overwrite:

`prompt 1/forward-looking-statements.md`

The markdown file is the source of truth — do not leave results only in chat.

### Deliverable skeleton (required)

```markdown
# Forward-Looking AI Statements — Corpus Extraction

## STEP 0 — PROCESSING MANIFEST
...

## STEP 1–2 — BY DOCUMENT

### [filename]
#### Source metadata
...
#### Forward-looking statements
...

## STEP 3 — PROCESSING SUMMARY
...
```

Do not add commentary outside Steps 0–3.

### Final validation

Before finishing, re-run the manifest script (or compare counts) and confirm:

1. Every Step 0 filename appears under Steps 1–2.
2. Every document has metadata + either ≥1 statement blocks or the exact no-statements line.
3. Deliverable path is `prompt 1/forward-looking-statements.md`.

If validation fails, fix the deliverable before stopping.

## Scale note

The corpus can be large (hundreds of files). Process systematically (by platform bucket), keep the checklist updated, and write/overwrite the deliverable incrementally if needed — but the final file must be complete and include every document.
