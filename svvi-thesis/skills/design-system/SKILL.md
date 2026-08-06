---
name: design-system
description: >-
  Mandatory Apple design system for EVERY SVVI visual output — dashboards,
  reports, presentations, slide decks, pitch pages, one-pagers, and any HTML
  Claude artifact. Use whenever creating, restyling, or reviewing SVVI visuals.
user-invocable: false
compatibility: Requires ${CLAUDE_PLUGIN_ROOT}/references/DESIGN-apple.md
version: 1.0.0
---

# SVVI design system (mandatory)

**Everything visual follows** `${CLAUDE_PLUGIN_ROOT}/references/DESIGN-apple.md`.

This includes: ops dashboard, research reports, **presentations / slide decks**, thesis deck pages, memos rendered as HTML, and any other Claude artifact with layout or styling.

## Rules (non-negotiable)

1. **Read** `references/DESIGN-apple.md` before writing or changing any HTML/CSS.
2. **Single accent:** Action Blue `#0066cc` for all interactive affordances. On dark tiles only, links may use Sky `#2997ff`. No second brand color.
3. **Surfaces:** alternate `#ffffff` / parchment `#f5f5f7` / near-black `#272729` (and tile-2/3 as needed). Color change = section divider. **No decorative gradients.**
4. **Type:** SF Pro Display + SF Pro Text with `system-ui, -apple-system, BlinkMacSystemFont` (Inter allowed as off-Apple substitute). Body **17px / 400 / 1.47 / -0.374px**. Display headlines **weight 600** (not 700). **No weight 500.**
5. **Chrome:** no shadows on cards, buttons, or text. Utility panels: `18px` radius + hairline `#e0e0e0`. Pills: full pill radius. Full-bleed tiles: `border-radius: 0`.
6. **Press:** `transform: scale(0.95)` on buttons — not a new fill color.
7. Prefer existing templates when they exist (`dashboard/template.html`, `dashboard/report-template.html`) and **do not restyle them ad hoc**. For presentations and other new surfaces, build HTML that expresses the same tokens/principles from DESIGN-apple.md (no competing design language).

## Presentations / decks

When the user asks for a presentation, slides, or deck:

- Prefer a self-contained **HTML** artifact (one idea per full-bleed tile/slide).
- Alternate light and dark tiles; museum-gallery whitespace; Action Blue CTAs only.
- Thesis content may still be written to markdown deliverables (`prompt 1/`, `prompt 2/`) for the pipeline — but **any presented deck/page shown to the user as an artifact must be Apple-styled HTML**.

## Quick check before delivering

- [ ] Only blue interactive color is `#0066cc` (or `#2997ff` on dark)
- [ ] No purple, no cream/terracotta theme, no glow, no multi-shadow cards
- [ ] No decorative CSS gradients
- [ ] Headlines use Display/system stack at weight 600 with tight tracking
- [ ] Body is 17px editorial leading
