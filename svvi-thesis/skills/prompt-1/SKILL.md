---
name: prompt-1
description: Run Prompt 1 — extract every forward-looking AI statement from the Markdown corpus into prompt 1/forward-looking-statements.md
argument-hint: "[corpus-dir]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# /prompt-1

Run the Prompt 1 workflow now.

Optional argument `$ARGUMENTS` is a corpus directory override (default: plugin `corpus/` if synced, else `output`).

1. Read and follow `${CLAUDE_PLUGIN_ROOT}/skills/forward-looking-thesis-extraction/SKILL.md` exactly.
2. Resolve corpus directory:
   - If `$ARGUMENTS` is non-empty, use it.
   - Else if `${CLAUDE_PLUGIN_ROOT}/corpus` has `*.md`, use that.
   - Else use `output/`.
3. Write the deliverable to `prompt 1/forward-looking-statements.md`.
4. If the local corpus looks empty/stale, run `${CLAUDE_PLUGIN_ROOT}/skills/sync-corpus/SKILL.md` first.
4. When finished, reply with the deliverable path and Step 3 summary counts only.
