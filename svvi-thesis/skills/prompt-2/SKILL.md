---
name: prompt-2
description: Run Prompt 2 — synthesize Prompt 1 output into consensus points, high-conviction signals, and thesis slide bullets
argument-hint: "[input-report]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# /prompt-2

Run the Prompt 2 workflow now.

Optional argument `$ARGUMENTS` is an input-report path override (default: `prompt 1/forward-looking-statements.md`).

1. Read and follow `${CLAUDE_PLUGIN_ROOT}/skills/investment-thesis-synthesis/SKILL.md` exactly.
2. If `$ARGUMENTS` is non-empty, use that file as the Prompt 1 report instead of the default.
3. Write the deliverable to `prompt 2/thesis-synthesis.md`.
4. When finished, reply with the deliverable path and a short count of consensus points, signals, and thesis bullets.
