# SVVI Thesis Plugin

**Install:** [SETUP.md](../../SETUP.md)

Cowork Desktop: download [svvi-thesis.zip](https://github.com/TeddyJubu/svvi-claude-plugins/releases/latest/download/svvi-thesis.zip) → Customize → Plugins → Upload.

On each session start the plugin syncs corpus markdown from the VPS into `corpus/` (token required). Local `*.md` not accessed for **90 days** (filesystem atime) are deleted automatically.

Slash commands after install: `/svvi-thesis:prompt-1`, `/svvi-thesis:prompt-2`, `/svvi-thesis:run-thesis-pipeline`, `/svvi-thesis:process-pending-jobs`, `/svvi-thesis:sync-corpus`.
