---
name: prompt-1
description: Run Prompt 1 — extract every forward-looking AI statement from the Markdown corpus into prompt 1/forward-looking-statements.md
argument-hint: "[corpus-dir]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# /prompt-1

Run the Prompt 1 workflow now.

Optional argument `$ARGUMENTS` is a corpus directory override (default: `output`).

1. Read and follow `${CLAUDE_PLUGIN_ROOT}/skills/forward-looking-thesis-extraction/SKILL.md` exactly.
2. If `$ARGUMENTS` is non-empty, use that path as `--output-dir` / corpus root instead of `output/`.
3. Write the deliverable to `prompt 1/forward-looking-statements.md`.
4. When finished, reply with the deliverable path and Step 3 summary counts only.
