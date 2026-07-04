#!/usr/bin/env python3
"""Audit patent claim numbering, dependency, and drafting hygiene."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


CLAIM_START_RE = re.compile(r"^\s*(\d+)[.)]\s*(.*)")
REFERENCE_RE = re.compile(r"\bclaim\s+(\d+)(?:\s*[-to]+\s*(\d+))?\b|\bclaims\s+(\d+)\s*(?:and|,)\s*(\d+)\b", re.I)
PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME)\b|\[\[|\]\]|\?\?", re.I)
RESULT_ONLY_RE = re.compile(r"\b(improve|optimize|enhance|increase|reduce|better|more efficient)\b", re.I)


@dataclass
class Finding:
    level: str
    claim: int | None
    code: str
    message: str


def split_claims(text: str) -> list[tuple[int, str]]:
    claims: list[tuple[int, str]] = []
    current_number: int | None = None
    current_lines: list[str] = []
    for raw in text.splitlines():
        match = CLAIM_START_RE.match(raw)
        if match:
            if current_number is not None:
                claims.append((current_number, " ".join(current_lines).strip()))
            current_number = int(match.group(1))
            current_lines = [match.group(2).strip()]
        elif current_number is not None:
            current_lines.append(raw.strip())
    if current_number is not None:
        claims.append((current_number, " ".join(current_lines).strip()))
    return claims


def references(text: str) -> list[int]:
    result: list[int] = []
    for match in REFERENCE_RE.finditer(text):
        if match.group(1):
            start = int(match.group(1))
            finish = int(match.group(2) or start)
            result.extend(range(start, finish + 1))
        else:
            result.extend((int(match.group(3)), int(match.group(4))))
    return sorted(set(result))


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text)


def audit(text: str) -> list[Finding]:
    claims = split_claims(text)
    findings: list[Finding] = []
    if not claims:
        return [Finding("ERROR", None, "NO_CLAIMS", "No numbered claims were detected.")]
    numbers = [number for number, _ in claims]
    expected = list(range(1, len(claims) + 1))
    if numbers != expected:
        findings.append(Finding("ERROR", None, "NUMBER_SEQUENCE", f"Expected claim numbers {expected}, found {numbers}."))
    claim_map: dict[int, str] = {}
    previous_text = ""
    for number, body in claims:
        compact = normalize(body)
        claim_map[number] = compact
        refs = references(body)
        if not body:
            findings.append(Finding("ERROR", number, "EMPTY", "Claim body is empty."))
            continue
        if PLACEHOLDER_RE.search(body):
            findings.append(Finding("ERROR", number, "UNRESOLVED_MARKER", "Unresolved drafting marker remains."))
        if number == 1 and refs:
            findings.append(Finding("ERROR", number, "INDEPENDENT_REFERENCE", "Claim 1 should not depend on another claim."))
        if number > 1 and not refs:
            findings.append(Finding("WARNING", number, "NO_REFERENCE", "Dependent claim does not reference an earlier claim."))
        for ref in refs:
            if ref >= number:
                findings.append(Finding("ERROR", number, "FORWARD_REFERENCE", f"Claim references non-previous claim {ref}."))
            if ref not in claim_map:
                findings.append(Finding("ERROR", number, "MISSING_REFERENCE", f"Referenced claim {ref} has not appeared yet."))
        if len(compact) < 25:
            findings.append(Finding("WARNING", number, "TOO_SHORT", "Claim is unusually short; verify support and scope."))
        if RESULT_ONLY_RE.search(body) and not re.search(r"\bwherein\b|\bcomprising\b|\bconfigured to\b", body, re.I):
            findings.append(Finding("WARNING", number, "RESULT_LANGUAGE", "Claim may describe a result without enough technical structure."))
        if previous_text and compact == previous_text:
            findings.append(Finding("WARNING", number, "DUPLICATE", "Claim repeats the previous claim."))
        previous_text = compact
    return findings


def format_report(findings: list[Finding]) -> str:
    if not findings:
        return "PASS: no blocking claim-audit findings.\n"
    lines = ["# Claim Audit Report", ""]
    for finding in findings:
        location = f"claim {finding.claim}" if finding.claim else "document"
        lines.append(f"- **{finding.level}** `{finding.code}` at {location}: {finding.message}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("claims", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    findings = audit(args.claims.read_text(encoding="utf-8", errors="ignore"))
    report = format_report(findings)
    if args.output:
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)
    return 1 if any(item.level == "ERROR" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
