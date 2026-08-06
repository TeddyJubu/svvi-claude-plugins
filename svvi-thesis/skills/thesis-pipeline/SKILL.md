---
name: thesis-pipeline
description: >-
  Runs the full SVVI thesis pipeline: Prompt 1 corpus extraction followed by
  Prompt 2 synthesis into consensus points, high-conviction signals, and thesis
  slide bullets. Use whenever the user asks for the full pipeline, both prompts,
  end-to-end thesis generation, Prompt 1 then Prompt 2, or building the fund
  deck thesis from the corpus in one pass.
compatibility: Requires Python 3, a Markdown corpus (default output/), and write access to prompt 1/ and prompt 2/.
version: 1.0.0
---

# Full Thesis Pipeline (Prompt 1 → Prompt 2)

Run the complete investment-thesis research workflow in order.

## Checklist

```text
Full Pipeline Progress:
- [ ] Phase A — Prompt 1 (forward-looking-thesis-extraction)
- [ ] Phase B — Prompt 2 (investment-thesis-synthesis)
- [ ] Confirm both deliverables exist
```

## Phase A — Prompt 1

Load and follow the skill at:

`${CLAUDE_PLUGIN_ROOT}/skills/forward-looking-thesis-extraction/SKILL.md`

Complete all Prompt 1 steps. Do not start Phase B until:

`prompt 1/forward-looking-statements.md`

exists and includes Steps 0–3.

## Phase B — Prompt 2

Load and follow the skill at:

`${CLAUDE_PLUGIN_ROOT}/skills/investment-thesis-synthesis/SKILL.md`

Complete all Prompt 2 steps and write:

`prompt 2/thesis-synthesis.md`

## Done criteria

Report brief completion status with paths to both deliverables. Do not modify unrelated application code.
