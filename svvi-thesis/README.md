# SVVI Thesis Plugin

**Install:** [SETUP.md](../../SETUP.md)

Cowork Desktop: download [svvi-thesis.zip](https://github.com/TeddyJubu/svvi-claude-plugins/releases/latest/download/svvi-thesis.zip) → Customize → Plugins → Upload.

**Design:** every visual artifact (dashboard, reports, presentations) follows [`references/DESIGN-apple.md`](references/DESIGN-apple.md) via the `design-system` skill.

On each session start the plugin:

1. Reminds the session of the Apple design system
2. Syncs corpus markdown from the VPS into `corpus/` (token required)
3. Rebuilds the **SVVI ops dashboard** HTML when the corpus etag changes and asks Claude to present it as an artifact

Local `*.md` not accessed for **90 days** (filesystem atime) are deleted automatically.

Slash commands: `/svvi-thesis:dashboard`, `/svvi-thesis:report`, `/svvi-thesis:present`, `/svvi-thesis:prompt-1`, `/svvi-thesis:prompt-2`, `/svvi-thesis:run-thesis-pipeline`, `/svvi-thesis:process-pending-jobs`, `/svvi-thesis:sync-corpus`.

**Report example:** `/svvi-thesis:report platform=blog query=Taiwan limit=10`  
**Presentation example:** `/svvi-thesis:present prompt 2/thesis-synthesis.md`
