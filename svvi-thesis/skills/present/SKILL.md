---
name: present
description: >-
  Build or restyle an SVVI presentation / slide deck / pitch page as an HTML
  Claude artifact using the mandatory Apple design system. Use when the user
  asks for slides, a deck, presentation, pitch, or thesis slides.
argument-hint: "[topic or source path]"
allowed-tools: [Read, Write, Edit, Glob, Grep, Bash]
compatibility: Requires references/DESIGN-apple.md
version: 1.0.0
---

# /present — Apple-styled presentation artifact

Create a **self-contained HTML presentation** and present it as a Claude artifact.

## Mandatory design

1. Follow `${CLAUDE_PLUGIN_ROOT}/skills/design-system/SKILL.md` exactly.
2. Read `${CLAUDE_PLUGIN_ROOT}/references/DESIGN-apple.md` before writing CSS.
3. There is **no separate presentation template** — compose HTML that encodes Apple tokens directly (same colors, type, tiles, pills as the ops dashboard / report).

## Content sources

Resolve `$ARGUMENTS`:

- If it points to a file (e.g. `prompt 2/thesis-synthesis.md`), base slides on that.
- If it is a topic string, pull supporting facts via SVVI MCP / local corpus first.
- If empty, ask what the deck should cover (thesis bullets, briefing, ops story, etc.).

## Slide grammar

Use full-bleed **tiles** stacked vertically (one idea per tile), not a dense SaaS dashboard:

1. Dark or black global strip with **SVVI**
2. Hero light tile — `display` headline + lead + optional Action Blue pill
3. Alternating parchment / dark / white tiles for each major point
4. Optional closing tile with next-step CTA

Each content tile: headline (40px-class Display 600) → short body (17px) → optional caption. Quotes get a 2px Action Blue left rule — no card shadows.

Save to `presentations/deck-YYYYMMDD-HHMM.html` (create folder if needed).

## Deliver

1. Write the HTML file.
2. **Present it as an interactive HTML artifact** in chat.
3. Reply with slide count and file path.

Do not ship Inter-purple SaaS chrome, multi-colored charts unless data-critical (then monochrome + Action Blue only), or markdown-only when the user asked for a presentation.
