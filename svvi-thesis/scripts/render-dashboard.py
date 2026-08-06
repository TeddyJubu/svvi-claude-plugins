#!/usr/bin/env python3
"""Fetch VPS dashboard JSON and render the SVVI ops HTML artifact."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path


def _token(root: Path) -> str:
    env = os.environ.get("SVVI_MCP_TOKEN", "").strip()
    if env:
        return env
    path = root / ".svvi" / "token"
    if path.is_file():
        return path.read_text(encoding="utf-8").strip()
    return ""


def _fetch(url: str, token: str) -> dict:
    """Auth via Authorization header only — never put the token in the URL."""
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"dashboard HTTP {exc.code}") from None
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", None)
        raise RuntimeError(f"dashboard network error: {type(reason).__name__ if reason else 'URLError'}") from None


def _html_safe_json(data: dict) -> str:
    """Embed JSON in a <script> tag without allowing </script> breakout."""
    return (
        json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )


def main() -> int:
    root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT") or Path(__file__).resolve().parents[1])
    base = os.environ.get("SVVI_BASE_URL", "https://srv1825737.hstgr.cloud").rstrip("/")
    url = os.environ.get("SVVI_DASHBOARD_URL", f"{base}/corpus/dashboard.json")
    token = _token(root)
    if not token:
        print("svvi-dashboard: no token; skip", file=sys.stderr)
        return 0

    data = _fetch(url, token)
    template_path = root / "dashboard" / "template.html"
    template = template_path.read_text(encoding="utf-8")
    html = template.replace("__SVVI_DATA_JSON__", _html_safe_json(data))

    out_dir = root / "dashboard"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "svvi-ops.html"
    out_path.write_text(html, encoding="utf-8")

    cwd_copy = Path.cwd() / "svvi-ops-dashboard.html"
    try:
        if cwd_copy.resolve() != out_path.resolve():
            cwd_copy.write_text(html, encoding="utf-8")
    except OSError:
        cwd_copy = None

    state_dir = root / ".svvi"
    state_dir.mkdir(parents=True, exist_ok=True)
    state = {
        "path": str(out_path),
        "cwd_copy": str(cwd_copy) if cwd_copy else None,
        "corpus_etag": data.get("corpus_etag"),
        "corpus_count": data.get("corpus_count"),
        "generated_at_iso": data.get("generated_at_iso"),
    }
    (state_dir / "dashboard.json").write_text(json.dumps(state, indent=2) + "\n", encoding="utf-8")

    print(f"svvi-dashboard: wrote {out_path}")
    print(
        "SVVI_DASHBOARD_ARTIFACT="
        f"{out_path}\n"
        "ACTION: Present the SVVI ops dashboard as an interactive HTML artifact now. "
        f"Read `{out_path}` and render it as a Claude artifact for the user. "
        "Data is synced from the VPS (source of truth)."
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        # Never print exception strings that might contain URLs with secrets.
        print(f"svvi-dashboard: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise SystemExit(1)
