#!/usr/bin/env python3
"""Validate metadata.json and the article files it points to.

Usage: python3 scripts/validate.py
Exits non-zero if any check fails. No third-party dependencies.
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://iggym.github.io/scaling-ai-systems/"
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
WINDOW_RE = re.compile(r"^\d{4}-\d{2}-\d{2} to \d{4}-\d{2}-\d{2}$")
SHARE_RE = re.compile(
    r'href="(https://(?:twitter\.com|x\.com)/intent/tweet\?[^"]*'
    r'|https://www\.linkedin\.com/sharing/share-offsite/\?[^"]*)"'
)
REQUIRED = ["id", "slug", "title", "hook", "path", "date", "status",
            "format", "tags", "reading_time_minutes", "pinned"]

errors, warnings = [], []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def check_shares(name, html, canonical):
    for raw in SHARE_RE.findall(html):
        q = parse_qs(urlsplit(raw.replace("&amp;", "&")).query)
        url = (q.get("url") or [""])[0]
        if not url:
            err(f"{name}: share link with empty url= ({raw[:60]}…)")
        elif url != canonical:
            err(f"{name}: share link points to {url}, expected {canonical}")


def main():
    data = json.loads((ROOT / "metadata.json").read_text())
    articles = data.get("articles", [])
    seen_ids, seen_slugs = {}, {}

    for a in articles:
        label = a.get("slug", "<no slug>")
        for key in REQUIRED:
            if key not in a:
                err(f"{label}: missing field '{key}'")
        if a.get("id") in seen_ids:
            err(f"{label}: duplicate id {a['id']} (also {seen_ids[a['id']]})")
        seen_ids[a.get("id")] = label
        if label in seen_slugs:
            err(f"{label}: duplicate slug")
        seen_slugs[label] = True

        if not DATE_RE.match(str(a.get("date", ""))):
            err(f"{label}: date must be YYYY-MM-DD")
        if "research_window" in a and not WINDOW_RE.match(a["research_window"]):
            warn(f"{label}: research_window not 'YYYY-MM-DD to YYYY-MM-DD'")

        path = a.get("path", "")
        if path != f"articles/{label}.html":
            err(f"{label}: path '{path}' does not match slug")
        f = ROOT / path
        if not f.is_file():
            err(f"{label}: file {path} does not exist")
            continue

        html = f.read_text()
        canonical = SITE + path
        check_shares(label, html, canonical)
        if 'name="description"' not in html:
            warn(f"{label}: missing meta description")
        if 'rel="canonical"' not in html:
            warn(f"{label}: missing canonical link")

    listed = {a.get("path") for a in articles}
    for f in sorted((ROOT / "articles").glob("*")):
        rel = f"articles/{f.name}"
        if not f.name.endswith(".html") or f.name.count(".html") != 1:
            err(f"{rel}: malformed file name")
        elif rel not in listed and not f.name.startswith("_"):
            warn(f"{rel}: not listed in metadata.json")

    for w in warnings:
        print(f"warn:  {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{len(articles)} articles, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
