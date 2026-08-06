---
name: investment-thesis-synthesis
description: >-
  Runs the Prompt 2 three-step workflow to synthesize a Prompt 1 forward-looking
  AI statements report into consensus points, high-conviction signals, and
  thesis-slide bullets for a co-investment fund deck. Use whenever the user
  mentions Prompt 2, thesis synthesis, consensus points, high-conviction
  signals, thesis slide output, fund-deck AI thesis bullets, or turning
  forward-looking-statements.md into investment convictions — even if they do
  not say "skill".
compatibility: Requires read access to prompt 1/forward-looking-statements.md and write access under prompt 2/.
version: 1.0.0
---

# Investment Thesis Synthesis (Prompt 2)

**VERSION 1 — FULL (Consensus + High Conviction + Thesis Slide)**

Act as a senior investment analyst at an AI-focused venture capital firm. You are given a report of forward-looking AI statements from multiple sources. Synthesize it into investment thesis outputs for a co-investment fund deck.

**Hard constraints**
- Do **not** modify unrelated application code, tests, config, or fetch pipelines.
- Only write under `prompt 2/` (overwriting the deliverable is expected).
- Work **only** from the provided Prompt 1 report. Do not introduce outside knowledge or fabricate insights.
- Write in clear, accessible language focused on business and market implications, not technical mechanics.
- If multiple sources say essentially the same thing, group them into **one** unified point — do not list duplicates separately.

## Working-project layout

Resolve the **project root** as the user's current working project.

| Role | Default path (from project root) |
| --- | --- |
| Input report | `prompt 1/forward-looking-statements.md` |
| Deliverable | `prompt 2/thesis-synthesis.md` |
| Canonical reference | `${CLAUDE_PLUGIN_ROOT}/references/prompt-2.md` |

Create `prompt 2/` if missing.

If `prompt 1/forward-looking-statements.md` is missing, stop and tell the user to run Prompt 1 first (`/svvi-thesis:prompt-1` or the `forward-looking-thesis-extraction` skill). Do not invent source material.

## Progress checklist

Copy and track:

```text
Prompt 2 Progress:
- [ ] Step 1 — Consensus points
- [ ] Step 2 — High-conviction signals
- [ ] Step 3 — Thesis slide output + write deliverable
```

Complete steps **in order**. Do not skip ahead.

---

## Step 1 — Consensus points

Identify predictions mentioned repeatedly across multiple sources in the input report.

For each consensus point, write:

**Consensus Point:** [One clear, declarative sentence capturing the shared prediction]

**Mentioned by:** [List of authors/sources]

**Supporting Quotes:**
- "[Verbatim quote — Source]"
- "[Verbatim quote — Source]"
*(One quote line per supporting source.)*

---

## Step 2 — High-conviction signals

Identify predictions that may not appear frequently but stand out because they are unusually specific, strongly worded, or come from a particularly credible source.

For each signal, write:

**Signal:** [One clear, declarative sentence capturing the prediction]

**Source:** [Author, publication, content type]

**Why it stands out:** [One sentence — e.g., "Unusually specific claim backed by data" or "Stated with strong conviction by a GP with direct exposure to this market"]

**Supporting Quote:** "[Verbatim quote]"

---

## Step 3 — Thesis slide output + write deliverable

Using Steps 1 and 2, produce thesis bullets for the investment deck. These should read as the firm's own forward-looking investment convictions — where AI is going and where the firm will invest.

Order: lead with the strongest consensus points, then high-conviction signals that deepen the thesis.

Format each bullet as:

**[Thesis bullet — a bold, declarative investment conviction statement]** Sources: [Author 1, Author 2...]

Then overwrite:

`prompt 2/thesis-synthesis.md`

The markdown file is the source of truth — do not leave results only in chat.

### Deliverable skeleton (required)

```markdown
# Investment Thesis Synthesis — Prompt 2

## STEP 1 — CONSENSUS POINTS
...

## STEP 2 — HIGH-CONVICTION SIGNALS
...

## STEP 3 — THESIS SLIDE OUTPUT
**[Thesis bullet]** Sources: ...
```

Do not add commentary outside Steps 1–3.

### Final validation

Before finishing, confirm:

1. Every consensus point has ≥2 supporting sources (or explicitly only appears if truly multi-source).
2. Quotes are verbatim from the Prompt 1 report — not paraphrased inventions.
3. Similar ideas are merged, not duplicated across Step 1 or Step 3.
4. Deliverable path is `prompt 2/thesis-synthesis.md`.

If validation fails, fix the deliverable before stopping.
