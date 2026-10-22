#!/usr/bin/env python3
"""Copy a research log's page into the site and give it the site's head tags.

The log is authored elsewhere and lands here as one self-contained HTML file. Everything
this script adds is keyed to a marker comment, so running it again replaces the old block
instead of stacking a second copy.

    python3 tools/sync_log.py <source.html> search-trees
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

SITE = "https://amit-prasad.github.io/catalan-research"
MARK_OPEN = "<!-- site:head -->"
MARK_CLOSE = "<!-- /site:head -->"

LOGS = {
    "search-trees": {
        "title": "The search trees",
        "description": (
            "A tree search over six thousand LLM-written intraday strategies for the Nifty 50, "
            "and the nine failures in its own scoring that void its leaderboard."
        ),
    },
}


def head_block(slug: str, meta: dict[str, str]) -> str:
    url = f"{SITE}/{slug}/"
    return "\n".join([
        MARK_OPEN,
        f'<link rel="canonical" href="{url}">',
        '<link rel="icon" href="../favicon.svg" type="image/svg+xml">',
        f'<meta name="description" content="{meta["description"]}">',
        '<meta property="og:type" content="article">',
        '<meta property="og:site_name" content="Catalan">',
        f'<meta property="og:title" content="{meta["title"]}">',
        f'<meta property="og:description" content="{meta["description"]}">',
        f'<meta property="og:url" content="{url}">',
        '<meta name="twitter:card" content="summary">',
        MARK_CLOSE,
    ])


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    source, slug = Path(sys.argv[1]), sys.argv[2]
    if slug not in LOGS:
        print(f"unknown log {slug!r}; known: {', '.join(LOGS)}")
        return 2

    html = source.read_text(encoding="utf-8")

    # drop a previous block, so the script is safe to re-run
    html = re.sub(re.escape(MARK_OPEN) + ".*?" + re.escape(MARK_CLOSE) + r"\n?", "", html, flags=re.S)

    anchor = "<title>"
    if anchor not in html:
        print("no <title> found; refusing to guess where the head starts")
        return 1
    html = html.replace(anchor, head_block(slug, LOGS[slug]) + "\n" + anchor, 1)

    target = Path(slug) / "index.html"
    target.write_text(html, encoding="utf-8")
    print(f"wrote {target} ({len(html):,} bytes) with canonical {SITE}/{slug}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
