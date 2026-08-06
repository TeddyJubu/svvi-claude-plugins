---
name: process-pending-jobs
description: >-
  Claim and process pending SVVI schedule agent jobs (Prompt 1 / Prompt 2 phases
  enqueued by svvi-scheduler or schedule_run). Use whenever the user mentions
  pending jobs, scheduled thesis jobs, process-pending-jobs, or queue of Prompt
  1/2 work from the scheduler — even if they do not say "skill".
argument-hint: ""
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
compatibility: Prefer MCP tools jobs_list / jobs_claim / jobs_complete when available; otherwise read .state/schedules/jobs/*.json.
version: 1.0.0
---

# Process Pending Schedule Jobs

Drain pending agent jobs created by scheduled fetch/prompt runs.

## Checklist

```text
Pending Jobs Progress:
- [ ] List pending jobs
- [ ] Claim each job
- [ ] Run phases (prompt1 / prompt2)
- [ ] Mark each job done or failed
```

## Steps

1. **List pending jobs**
   - Prefer MCP tool `jobs_list` with `status=pending`.
   - Fallback: read `.state/schedules/jobs/job_*.json` where `"status": "pending"`.

2. If none, tell the user there are no pending jobs and stop.

3. For each pending job (oldest first):
   1. Claim via MCP `jobs_claim` (or set status to `running` in the JSON file).
   2. For each phase in `job.phases` (in order):
      - `prompt1` → follow `${CLAUDE_PLUGIN_ROOT}/skills/forward-looking-thesis-extraction/SKILL.md`
      - `prompt2` → follow `${CLAUDE_PLUGIN_ROOT}/skills/investment-thesis-synthesis/SKILL.md`
   3. Complete via MCP `jobs_complete` with `status=done` and a short note, or `status=failed` with the error if a phase fails. Stop further phases on failure.

4. Summarize: how many jobs processed, succeed/fail counts, and deliverable paths:
   - `prompt 1/forward-looking-statements.md`
   - `prompt 2/thesis-synthesis.md`

Do not modify application/fetch code. Do not invent quotes outside the corpus/report.
Any HTML presentation of job outputs must follow `${CLAUDE_PLUGIN_ROOT}/skills/design-system/SKILL.md`.
