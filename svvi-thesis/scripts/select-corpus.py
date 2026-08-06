#!/usr/bin/env python3
"""Select local corpus markdown by platform/batch/query/date filters.

Self-contained for Cowork sandboxes (does not require svvi_fetch installed).
Prints JSON: { filters, count, files: [{filename, platform, title, date, path, bytes}] }
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

import yaml

FILENAME_RE = re.compile(
    r"^_(\d+)_(.+)_(\d{4}-\d{2}-\d{2})_(\d{2}-\d{2}-\d{2})\.md$"
)


def _parse_frontmatter(raw: str) -> tuple[dict, str]:
    text = raw.lstrip("\ufeff")
    if not text.startswith("---"):
        return {}, text
    parts = re.split(r"^---\s*$", text, maxsplit=2, flags=re.M)
    if len(parts) < 3:
        return {}, text
    try:
        data = yaml.safe_load(parts[1]) or {}
    except Exception:  # noqa: BLE001
        data = {}
    if not isinstance(data, dict):
        data = {}
    return data, parts[2]


def _load_doc(path: Path) -> dict | None:
    m = FILENAME_RE.match(path.name)
    if not m:
        return None
    batch = int(m.group(1))
    date = m.group(3)
    raw = path.read_text(encoding="utf-8", errors="replace")
    meta, body = _parse_frontmatter(raw)
    platform = str(meta.get("platform") or "unknown").strip().lower() or "unknown"
    title = str(meta.get("title") or path.stem).strip()
    url = str(meta.get("url") or "").strip()
    source_name = str(meta.get("source_name") or meta.get("source") or "").strip()
    return {
        "filename": path.name,
        "path": str(path),
        "batch": batch,
        "date": date,
        "platform": platform,
        "title": title,
        "url": url,
        "source_name": source_name,
        "bytes": path.stat().st_size,
        "body": body,
    }


def select(
    corpus_dir: Path,
    *,
    platform: str = "",
    batch: int | None = None,
    query: str = "",
    since: str = "",
    until: str = "",
    limit: int = 25,
) -> list[dict]:
    docs: list[dict] = []
    for path in sorted(corpus_dir.glob("*.md")):
        doc = _load_doc(path)
        if not doc:
            continue
        if platform and doc["platform"] != platform.strip().lower():
            continue
        if batch is not None and doc["batch"] != batch:
            continue
        if since and doc["date"] < since:
            continue
        if until and doc["date"] > until:
            continue
        if query:
            q = query.lower()
            hay = f"{doc['title']}\n{doc['filename']}\n{doc['body']}".lower()
            if q not in hay:
                continue
        docs.append(doc)
    docs.sort(key=lambda d: (d["date"], d["filename"]), reverse=True)
    return docs[: max(1, min(limit, 100))]


def main() -> int:
    parser = argparse.ArgumentParser(description="Select SVVI corpus docs by filters")
    parser.add_argument(
        "--corpus-dir",
        default="",
        help="Corpus directory (default: $CLAUDE_PLUGIN_ROOT/corpus or ./output)",
    )
    parser.add_argument("--platform", default="", help="blog|youtube|twitter|apple|unknown")
    parser.add_argument("--batch", type=int, default=None)
    parser.add_argument("--query", default="", help="Case-insensitive substring")
    parser.add_argument("--since", default="", help="YYYY-MM-DD inclusive")
    parser.add_argument("--until", default="", help="YYYY-MM-DD inclusive")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument(
        "--excerpt-chars",
        type=int,
        default=1200,
        help="Include body excerpt in JSON (0 = paths/meta only)",
    )
    args = parser.parse_args()

    root = Path(os.environ.get("CLAUDE_PLUGIN_ROOT") or Path(__file__).resolve().parents[1])
    if args.corpus_dir:
        corpus = Path(args.corpus_dir)
    elif (root / "corpus").is_dir() and any((root / "corpus").glob("*.md")):
        corpus = root / "corpus"
    elif Path("output").is_dir():
        corpus = Path("output")
    else:
        corpus = root / "corpus"

    if not corpus.is_dir():
        print(json.dumps({"error": f"corpus dir missing: {corpus}", "count": 0, "files": []}, indent=2))
        return 1

    files = select(
        corpus,
        platform=args.platform,
        batch=args.batch,
        query=args.query,
        since=args.since,
        until=args.until,
        limit=args.limit,
    )
    out_files = []
    for doc in files:
        item = {k: v for k, v in doc.items() if k != "body"}
        if args.excerpt_chars > 0:
            body = doc["body"].strip()
            item["excerpt"] = body[: args.excerpt_chars] + (
                "…" if len(body) > args.excerpt_chars else ""
            )
        out_files.append(item)

    payload = {
        "ok": True,
        "corpus_dir": str(corpus.resolve()),
        "filters": {
            "platform": args.platform or None,
            "batch": args.batch,
            "query": args.query or None,
            "since": args.since or None,
            "until": args.until or None,
            "limit": args.limit,
        },
        "count": len(out_files),
        "files": out_files,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
