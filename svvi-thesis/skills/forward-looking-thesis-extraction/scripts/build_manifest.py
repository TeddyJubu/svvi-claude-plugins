#!/usr/bin/env python3
"""Build Prompt 1 Step 0 processing manifest from a Markdown corpus."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


BUCKETS = {
    "blog": "Blogs (platform: blog)",
    "youtube": "Podcast Transcripts (platform: youtube | apple)",
    "apple": "Podcast Transcripts (platform: youtube | apple)",
    "twitter": "Twitter (platform: twitter)",
}

BUCKET_ORDER = [
    "Blogs (platform: blog)",
    "Podcast Transcripts (platform: youtube | apple)",
    "Twitter (platform: twitter)",
    "Other / Unknown platforms",
    "Unreadable",
]


def read_platform(path: Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        print(f"# ERROR reading {path.name}: {exc}", file=sys.stderr)
        return None

    if not text.startswith("---"):
        return "unknown"

    end = text.find("\n---", 3)
    if end == -1:
        return "unknown"

    for line in text[3:end].splitlines():
        if line.startswith("platform:"):
            return line.split(":", 1)[1].strip().strip("\"'").lower()
    return "unknown"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output"),
        help="Path to corpus directory (default: ./output)",
    )
    args = parser.parse_args()
    output_dir: Path = args.output_dir

    if not output_dir.is_dir():
        print(f"ERROR: corpus directory not found: {output_dir}", file=sys.stderr)
        return 1

    files = sorted(p for p in output_dir.glob("*.md") if p.is_file())
    grouped: dict[str, list[str]] = {label: [] for label in BUCKET_ORDER}

    for path in files:
        platform = read_platform(path)
        if platform is None:
            grouped["Unreadable"].append(path.name)
            continue
        label = BUCKETS.get(platform)
        if label is None:
            grouped["Other / Unknown platforms"].append(
                f"{path.name} (platform: {platform})"
            )
            continue
        grouped[label].append(path.name)

    print("## STEP 0 — PROCESSING MANIFEST")
    print()
    for label in BUCKET_ORDER:
        names = grouped[label]
        joined = ", ".join(names) if names else "(none)"
        print(f"{label}: {joined}")
        print()

    print(f"Total documents: {len(files)}")
    print(f"Blogs: {len(grouped[BUCKET_ORDER[0]])}")
    print(f"Podcast Transcripts: {len(grouped[BUCKET_ORDER[1]])}")
    print(f"Twitter: {len(grouped[BUCKET_ORDER[2]])}")
    print(f"Other / Unknown: {len(grouped['Other / Unknown platforms'])}")
    print(f"Unreadable: {len(grouped['Unreadable'])}")

    if grouped["Other / Unknown platforms"] or grouped["Unreadable"]:
        print(
            "ERROR: every corpus *.md must be processed; "
            "unknown/unreadable files are listed in the Step 0 manifest above.",
            file=sys.stderr,
        )
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
