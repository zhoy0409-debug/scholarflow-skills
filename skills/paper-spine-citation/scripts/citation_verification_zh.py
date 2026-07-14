#!/usr/bin/env python3
"""Extract and sanity-check reference strings from a manuscript."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path


REFERENCE_LINE_RE = re.compile(r"^\s*(?:\[(?P<num>\d+)\]|\d+[.)])\s*(?P<body>.+)")
DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+\b", re.IGNORECASE)
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
TITLE_RE = re.compile(r'"([^"]+)"|“([^”]+)”')


@dataclass
class ReferenceCheck:
    number: int | None
    text: str
    has_year: bool
    has_doi: bool
    title: str | None
    findings: list[str]


def iter_reference_lines(text: str) -> list[tuple[int | None, str]]:
    lines: list[tuple[int | None, str]] = []
    for raw in text.splitlines():
        match = REFERENCE_LINE_RE.match(raw)
        if match:
            num = int(match.group("num")) if match.group("num") else None
            lines.append((num, match.group("body").strip()))
    return lines


def check_reference(number: int | None, body: str) -> ReferenceCheck:
    findings: list[str] = []
    has_year = bool(YEAR_RE.search(body))
    has_doi = bool(DOI_RE.search(body))
    title_match = TITLE_RE.search(body)
    title = next((group for group in title_match.groups() if group), None) if title_match else None
    if not has_year:
        findings.append("missing publication year")
    if len(body) < 30:
        findings.append("reference is unusually short")
    if not has_doi:
        findings.append("no DOI detected; verify manually if the style requires DOI")
    return ReferenceCheck(number, body, has_year, has_doi, title, findings)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manuscript", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    text = args.manuscript.read_text(encoding="utf-8", errors="ignore")
    checks = [check_reference(num, body) for num, body in iter_reference_lines(text)]
    if args.json:
        print(json.dumps([asdict(item) for item in checks], ensure_ascii=False, indent=2))
    else:
        print("# Citation Verification Report\n")
        print(f"- References detected: {len(checks)}")
        for item in checks:
            if item.findings:
                label = f"[{item.number}]" if item.number is not None else "[unnumbered]"
                print(f"- {label} {'; '.join(item.findings)}")
    return 1 if any(item.findings for item in checks) else 0


if __name__ == "__main__":
    raise SystemExit(main())
