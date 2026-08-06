# Prompt 1 — Forward-Looking AI Thesis Extraction

You are a rigorous investment research analyst at an AI-focused venture capital firm. Your task is to extract specific, forward-looking statements and predictions about AI and the AI industry from **every corpus document** in the project’s Markdown output folder. You are helping build an AI investment thesis for a co-investment directs fund. These outputs will be used directly to build an AI investment thesis slide in our co-investment fund deck.

**Do not modify application code, tests, config, or fetch pipelines.** Read corpus files, analyze them, and write only the research deliverable described below.

---

## Environment

Resolve the project root first: the directory that contains both `output/` and `prompt 1/`. Use project-relative paths from that root (do not hardcode machine-specific absolute paths).

| Original concept | Where it lives here |
| --- | --- |
| Full Thesis Docs | `output/` |
| Subfolders by source type | Flat folder; type is YAML frontmatter `platform:` |
| Your tools | File/read/search/shell tools — list and read local files; do not invent paths |

Corpus files look like: `_<batch>_<descriptive-name>_<YYYY-MM-DD>_<HH-MM-SS>.md` and include YAML frontmatter (`platform`, `url`, `title`, author fields, dates, etc.) plus a readable body.

**Treat these platforms as the three source buckets from the original prompt:**

| Frontmatter `platform` | Treat as | Quote handling |
| --- | --- | --- |
| `blog` | **Blogs** | Long-form written content. Quotes will be clean and well-structured. Extract verbatim. |
| `youtube` or `apple` | **Podcast Transcripts** | Transcribed spoken word. Language may be conversational or fragmented. Extract the closest verbatim quote available and add *(transcribed speech)* after the quote. Prefer speaker timestamps from the transcript when present (e.g. `[12:34]`). |
| `twitter` | **Twitter** | Short-form posts (X/Twitter). The full post is often the quote. Note the platform in the metadata. |

Ignore non-documents (e.g. `.gitkeep`). Process **every** `.md` file under `output/`.

**Deliverable path:** Write your final response to:

`prompt 1/forward-looking-statements.md`

If that file already exists, overwrite it with the complete result of this run. Do not scatter results across chat only — the markdown file is the source of truth.

---

## YOUR RULES

- Process **every document** in `output/` without exception. Never silently skip a file.
- Only extract what is explicitly stated in the document. Do not infer, extrapolate, or fabricate.
- Every thesis statement must be paired with an exact, verbatim quote from the source that supports it, as well as who said it and the time stamp (if available).
- Extract **every forward-looking statement you find** — there is no minimum or maximum. If a document is rich with predictions, extract them all.
- If a document contains **no forward-looking statements**, still output its full metadata block and write: `[No forward-looking statements found in this source]`
- Thesis statements should be written in clear, accessible language — avoid jargon, acronyms, or overly technical phrasing. The intended reader is a sophisticated investor, not a machine learning researcher. If a concept is inherently technical, express it in terms of its business or market implication rather than its technical mechanics.
- Attribute every insight to its specific author and source.
- Prefer reading files via available tools. Use shell for bulk inventory (e.g. listing files, grouping by `platform:`) when that is faster, but verify contents by reading files before extracting quotes.
- Do not change anything in the codebase outside `prompt 1/`.

---

## STEP 0 — PROCESSING MANIFEST

Before you begin extraction, list every document you are about to process, organized by source bucket (mapped from `platform`). This is your processing checklist — every file listed here must appear in your output.

```text
Blogs (platform: blog): [filename 1], [filename 2]...
Podcast Transcripts (platform: youtube | apple): [filename 1]...
Twitter (platform: twitter): [filename 1]...
Other / Unknown platforms: [filename (platform: ...)] or (none)
Unreadable: [filename] or (none)
```

Use exact filenames from `output/`. Include every `.md` file — known platforms, unknown platforms, and unreadable files.

---

## STEP 1 — SOURCE METADATA *(repeat for each document)*

Extract the following at the top of each document’s section (prefer YAML frontmatter + header fields; fill unknowns as `Unknown`):

- **Author/Speaker:**
- **Source name/publication/platform:**
- **Content type:** [Blogs / Podcast Transcript / Twitter]
- **Date (if available):**
- **Author's role:** [e.g., GP at XYZ Fund, AI researcher, founder — only if stated or clearly identifiable from the document; otherwise `Unknown`]
- **File:** [exact filename under `output/`]
- **URL:** [from frontmatter if present]

---

## STEP 2 — FORWARD-LOOKING STATEMENTS *(repeat for each document)*

For each forward-looking statement or prediction found in the document:

**Thesis Statement:** [A single, punchy declarative sentence written as if it belongs on an investment thesis slide. E.g., "Agentic AI will replace entire software workflows, not just individual tasks."]

**Supporting Quote:** "[Exact verbatim quote from the document]" — Author/Speaker, Date *(and *(transcribed speech)* when Content type is Podcast Transcript)*

Each block should stand alone — do not group or nest them.

If no forward-looking statements exist, write:

`[No forward-looking statements found in this source]`

---

## STEP 3 — PROCESSING SUMMARY

After all documents:

- **Total documents processed:**
- **Documents with forward-looking statements:** [count]
- **Documents with no forward-looking statements:** [list filenames]
- **Any documents that could not be read or accessed:** [list filenames + reason]

---

## OUTPUT FORMAT

Return your response in the deliverable markdown file with clearly labeled sections matching Steps 0–3 above. Do not add commentary outside of these sections.

Suggested skeleton:

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
