#!/usr/bin/env python3
"""Heuristic audit of copy exposed by the standalone Atlas, not a source review.

Reports suspect internal/process language without printing the text itself.
Default mode is nonblocking while known defects are being remediated.
--strict blocks if any candidate remains; human sign-off is still mandatory.
"""
import argparse
import base64
import gzip
import json
import re
import sys
from collections import Counter
from pathlib import Path

from check_project import Page, expand_payload

PATTERNS = {
    "original_research_control": re.compile(r"original\\s+research\\s+wording", re.I),
    "internal_audit_id": re.compile(r"\\bAS-\\d{2,}\\b", re.I),
    "source_not_inspected": re.compile(
        r"\\b(?:uninspected|not inspected|not read|was not read)\\b", re.I
    ),
    "generated_intermediary": re.compile(
        r"\\b(?:AI[- ]generated\\s+HTML|AI[- ]generated\\s+transcript)\\b", re.I
    ),
    "batch_process_description": re.compile(
        r"\\b(?:in this batch|in this run|local research batch|audit checkpoint)\\b", re.I
    ),
}

def find_candidates(text):
    return [label for label, expression in PATTERNS.items() if expression.search(text)]

def strings_with_paths(value, prefix):
    if isinstance(value, str):
        yield prefix, value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield from strings_with_paths(child, prefix + "." + str(key))
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            yield from strings_with_paths(child, prefix + "[" + str(idx) + "]")

def check_edition(root, edition):
    html = (root / "docs" / edition / "index.html").read_text(encoding="utf8")
    findings = []
    for label in find_candidates(html):
        # UI strings are visible in the source bundle even when collapsed.
        findings.append({"location": "public HTML source", "rule": label})
    page = Page()
    page.feed(html)
    scripts = [
        s for s in page.scripts if s["attrs"].get("id") == "atlas-pilot-data"
    ]
    if len(scripts) != 1:
        raise ValueError(edition + ": expected exactly one embedded dataset")
    wrapper = json.loads(scripts[0]["text"])
    if wrapper.get("encoding") != "gzip-base64":
        raise ValueError(edition + ": unexpected packed dataset")
    packed = gzip.decompress(base64.b64decode(wrapper["payload"], validate=True))
    payload = expand_payload(json.loads(packed))
    for path, value in strings_with_paths(payload, "embedded"):
        for label in find_candidates(value):
            findings.append({"location": path, "rule": label})
    return findings

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    ap.add_argument("--strict", action="store_true",
                    help="Nonzero exit for any candidates (use after cleanup)")
    args = ap.parse_args()
    per_edition = {}
    total = []
    try:
        for edition in ("primary", "young-explorers"):
            matches = check_edition(args.root, edition)
            per_edition[edition] = {
                "candidates": len(matches),
                "by_rule": dict(Counter(item["rule"] for item in matches)),
                # Internal field paths only; never log excerpts from the text.
                "sample_locations": matches[:10],
            }
            total.extend(matches)
    except (OSError, KeyError, ValueError, EOFError) as exc:
        print(json.dumps({"status": "ERROR", "detail": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps({
        "status": "NEEDS_REVIEW" if total else "NO_HEURISTIC_MATCHES",
        "total_candidates": len(total),
        "editions": per_edition,
        "manual_review_required": True,
        "public_copy_certified": False,
        "release_gate": "OPEN; see project/PUBLIC_COPY_REMEDIATION.md",
        "mode": "strict" if args.strict else "report-only",
    }))
    if args.strict and total:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
