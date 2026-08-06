#!/usr/bin/env bash
# Remind the session that all SVVI visuals use the Apple design system.
set -euo pipefail
ROOT="${CLAUDE_PLUGIN_ROOT:-}"
if [[ -z "$ROOT" ]]; then
  ROOT="$(cd "$(dirname "$0")/.." && pwd)"
fi
echo "SVVI_DESIGN_SYSTEM=${ROOT}/references/DESIGN-apple.md"
echo "ACTION: All SVVI visual artifacts (dashboard, reports, presentations/decks, any HTML) MUST follow ${ROOT}/skills/design-system/SKILL.md and ${ROOT}/references/DESIGN-apple.md. Single accent #0066cc; parchment/dark tile rhythm; no decorative gradients or chrome shadows."
