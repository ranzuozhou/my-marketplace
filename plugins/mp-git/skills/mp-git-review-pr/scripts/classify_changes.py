#!/usr/bin/env python3
"""
classify_changes.py — File classification for mp-git-review-pr

Classifies changed files in a PR into categories for the review checklist.

Usage:
    python classify_changes.py <file1> <file2> ...
    echo "file1\nfile2" | python classify_changes.py --stdin

Categories:
    Plugin  — plugin.json, .mcp.json, CLAUDE.md, README.md (plugin-level)
    Skill   — skills/**/SKILL.md + reference files
    Config  — .claude-plugin/, VERSION, marketplace.json
    Docs    — docs/**
    Scripts — scripts/**
    CI      — .github/**
    Other   — unclassified
"""

import sys
import re
from collections import defaultdict


CLASSIFICATION_RULES = [
    # (category, pattern_description, regex_pattern)
    ("Config", ".claude-plugin/", re.compile(r"^\.claude-plugin/")),
    ("Config", "VERSION", re.compile(r"^VERSION$")),
    ("CI", ".github/", re.compile(r"^\.github/")),
    ("Scripts", "scripts/", re.compile(r"^scripts/")),
    ("Docs", "docs/", re.compile(r"^docs/")),
    ("Skill", "SKILL.md + references", re.compile(r"^plugins/[^/]+/skills/.+")),
    ("Plugin", "plugin-level metadata", re.compile(
        r"^plugins/[^/]+/(\.claude-plugin/plugin\.json|\.mcp\.json|CLAUDE\.md|README\.md|CHANGELOG\.md)$"
    )),
]


def classify_file(filepath: str) -> str:
    """Classify a single file path into a category."""
    for category, _desc, pattern in CLASSIFICATION_RULES:
        if pattern.search(filepath):
            return category
    return "Other"


def classify_files(filepaths: list[str]) -> dict[str, list[str]]:
    """Classify a list of file paths, returning {category: [files]}."""
    result = defaultdict(list)
    for fp in filepaths:
        fp = fp.strip()
        if fp:
            category = classify_file(fp)
            result[category].append(fp)
    return dict(result)


def main():
    if "--stdin" in sys.argv:
        filepaths = sys.stdin.read().strip().split("\n")
    else:
        filepaths = [a for a in sys.argv[1:] if not a.startswith("--")]

    if not filepaths or (len(filepaths) == 1 and not filepaths[0]):
        print("Usage: python classify_changes.py <file1> [file2] ...")
        print("       echo 'file1\\nfile2' | python classify_changes.py --stdin")
        sys.exit(1)

    classified = classify_files(filepaths)

    # Summary
    total = sum(len(v) for v in classified.values())
    categories_order = ["Plugin", "Skill", "Config", "Docs", "Scripts", "CI", "Other"]

    print(f"Total: {total} files")
    print()

    for cat in categories_order:
        files = classified.get(cat, [])
        if files:
            print(f"[{cat}] ({len(files)} files)")
            for f in sorted(files):
                print(f"  {f}")
            print()

    # One-line summary for comment template
    summary_parts = []
    for cat in categories_order:
        count = len(classified.get(cat, []))
        if count:
            summary_parts.append(f"{cat} {count}")
    print(f"Summary: {' | '.join(summary_parts)}")


if __name__ == "__main__":
    main()
