---
name: run-thesis-pipeline
description: Run the full Prompt 1 → Prompt 2 thesis pipeline end-to-end against the project corpus
argument-hint: "[corpus-dir]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
---

# /run-thesis-pipeline

Run the full thesis pipeline now.

Optional argument `$ARGUMENTS` is a corpus directory override for Prompt 1 (default: `output`).

1. Read and follow `${CLAUDE_PLUGIN_ROOT}/skills/thesis-pipeline/SKILL.md` exactly.
2. Pass any corpus override through to Prompt 1.
3. Produce both:
   - `prompt 1/forward-looking-statements.md`
   - `prompt 2/thesis-synthesis.md`
4. When finished, reply with both deliverable paths and brief Phase A / Phase B counts.
