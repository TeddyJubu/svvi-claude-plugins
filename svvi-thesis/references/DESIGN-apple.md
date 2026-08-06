---
version: alpha
name: Apple-design-analysis
description: A photography-first interface that turns marketing into a museum gallery. Edge-to-edge product tiles alternate light and dark canvases, framed by SF Pro Display headlines with negative letter-spacing and a single Action Blue (#0066cc) interactive color. UI chrome recedes so the product can speak — no decorative gradients, no shadows on chrome, only the one signature drop-shadow under product imagery resting on a surface.

colors:
  primary: "#0066cc"
  primary-focus: "#0071e3"
  primary-on-dark: "#2997ff"
  ink: "#1d1d1f"
  body: "#1d1d1f"
  body-on-dark: "#ffffff"
  body-muted: "#cccccc"
  ink-muted-80: "#333333"
  ink-muted-48: "#7a7a7a"
  divider-soft: "#f0f0f0"
  hairline: "#e0e0e0"
  canvas: "#ffffff"
  canvas-parchment: "#f5f5f7"
  surface-pearl: "#fafafc"
  surface-tile-1: "#272729"
  surface-tile-2: "#2a2a2c"
  surface-tile-3: "#252527"
  surface-black: "#000000"
  surface-chip-translucent: "#d2d2d7"
  on-primary: "#ffffff"
  on-dark: "#ffffff"

typography:
  hero-display:
    fontFamily: "SF Pro Display, system-ui, -apple-system, sans-serif"
    fontSize: 56px
    fontWeight: 600
    lineHeight: 1.07
    letterSpacing: -0.28px
  display-lg:
    fontFamily: "SF Pro Display, system-ui, -apple-system, sans-serif"
    fontSize: 40px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: 0
  display-md:
    fontFamily: "SF Pro Text, system-ui, -apple-system, sans-serif"
    fontSize: 34px
    fontWeight: 600
    lineHeight: 1.47
    letterSpacing: -0.374px
  lead:
    fontFamily: "SF Pro Display, system-ui, -apple-system, sans-serif"
    fontSize: 28px
    fontWeight: 400
    lineHeight: 1.14
    letterSpacing: 0.196px
  tagline:
    fontFamily: "SF Pro Display, system-ui, -apple-system, sans-serif"
    fontSize: 21px
    fontWeight: 600
    lineHeight: 1.19
    letterSpacing: 0.231px
  body:
    fontFamily: "SF Pro Text, system-ui, -apple-system, sans-serif"
    fontSize: 17px
    fontWeight: 400
    lineHeight: 1.47
    letterSpacing: -0.374px
  caption:
    fontFamily: "SF Pro Text, system-ui, -apple-system, sans-serif"
    fontSize: 14px
    fontWeight: 400
    lineHeight: 1.43
    letterSpacing: -0.224px
  fine-print:
    fontFamily: "SF Pro Text, system-ui, -apple-system, sans-serif"
    fontSize: 12px
    fontWeight: 400
    lineHeight: 1.0
    letterSpacing: -0.12px

rounded:
  none: 0px
  sm: 8px
  md: 11px
  lg: 18px
  pill: 9999px

spacing:
  xs: 8px
  sm: 12px
  md: 17px
  lg: 24px
  xl: 32px
  xxl: 48px
  section: 80px
---

# SVVI use of Apple design

**Canonical design system for everything visual in this plugin:** ops dashboard, research reports, presentations / slide decks, thesis deck pages, and any other HTML Claude artifact.

Agents must also follow `${CLAUDE_PLUGIN_ROOT}/skills/design-system/SKILL.md`.

## Non-negotiables

- Single accent: Action Blue `#0066cc` for all interactive affordances. Sky `#2997ff` only on dark tiles.
- Surfaces: white `#ffffff`, parchment `#f5f5f7`, near-black tile `#272729` — alternate for section rhythm. No decorative gradients.
- No shadows on UI chrome (cards/buttons/text). Flat + hairline only.
- Type: `SF Pro Display` / `SF Pro Text` with `system-ui, -apple-system, BlinkMacSystemFont` fallback; off-Apple platforms may load Inter as substitute with tightened tracking.
- Body at 17px / 400 / 1.47 / -0.374px. Display headlines weight 600, never 700. No weight 500.
- Full-bleed section/slide tiles use `rounded.none`. Utility panels use `rounded.lg` (18px) + hairline `#e0e0e0`.
- Pills use `rounded.pill` for primary actions.

Existing HTML shells: `dashboard/template.html`, `dashboard/report-template.html`. Presentations have no fixed shell — compose from these tokens.

See the remainder of this file / upstream Apple analysis for full component vocabulary.
