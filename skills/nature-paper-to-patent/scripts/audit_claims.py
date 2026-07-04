#!/usr/bin/env python3
"""Run deterministic structural checks on Chinese patent claims."""

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


CLAIM_START = re.compile(r"(?m)^\s*(\d+)\s*[., ．]\s*")
REFERENCE = re.compile(
    r"English text\s*(\d+)(?:\s*[--~～English text]\s*(\d+))?"
    r"|English text\s*(\d+)\s*(?:English text|, )\s*(\d+)"
)
TERM_INTRO = re.compile(r"(?:English text|English text)([\u4e00-\u9fffA-Za-z][\u4e00-\u9fffA-Za-z0-9_-]{1,20})")
PLACEHOLDER = re.compile(r"\[(?:TO CONFIRM|English text)[^\]]*\]", re.IGNORECASE)


@dataclass
class Finding:
    level: str
    claim: int | None
    code: str
    message: str


def split_claims(text: str) -> list[tuple[int, str]]:
    matches = list(CLAIM_START.finditer(text))
    claims = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        claims.append((int(match.group(1)), text[match.end() : end].strip()))
    return claims


def references(body: str) -> list[int]:
    result = []
    for match in REFERENCE.finditer(body):
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
    findings = []
    if not claims:
        return [Finding("ERROR", None, "NO_CLAIMS", "English text"1."English text. ")]

    numbers = [number for number, _ in claims]
    expected = list(range(1, len(claims) + 1))
    if numbers != expected:
        findings.append(
            Finding("ERROR", None, "NUMBER_SEQUENCE", f"English text{expected}, English text{numbers}. ")
        )

    previous_text = ""
    claim_map = {}
    for number, body in claims:
        compact = normalize(body)
        claim_map[number] = compact
        refs = references(body)

        if not body:
            findings.append(Finding("ERROR", number, "EMPTY", "English text. "))
            continue
        if PLACEHOLDER.search(body):
            findings.append(
                Finding("ERROR", number, "PLACEHOLDER", "English text. ")
            )
        if number == 1 and refs:
            findings.append(
                Finding("ERROR", number, "INDEPENDENT_REFERENCE", "English text1English text. ")
            )
        if number > 1 and not refs:
            findings.append(
                Finding("WARNING", number, "NO_REFERENCE", "English text; English text. ")
            )
        for ref in refs:
            if ref >= number:
                findings.append(
                    Finding("ERROR", number, "FORWARD_REFERENCE", f"English text{ref}. ")
                )
            if ref not in claim_map:
                findings.append(
                    Finding("ERROR", number, "MISSING_REFERENCE", f"English text{ref}English text. ")
                )

        if "English text" not in compact:
            findings.append(
                Finding("WARNING", number, "TRANSITION", "English text"English text"English text. ")
            )
        if len(compact) < 25:
            findings.append(
                Finding("WARNING", number, "TOO_SHORT", "English text, English text. ")
            )
        if re.search(r"(English text|English text|English text|English text|English text|English text)", compact):
            findings.append(
                Finding("WARNING", number, "RESULT_LANGUAGE", "English text, English text. ")
            )

        searchable_basis = previous_text + "".join(
            claim_map.get(ref, "") for ref in refs
        )
        for term in sorted(set(TERM_INTRO.findall(body))):
            if term in {"English text", "English text", "English text", "English text", "English text", "English text"}:
                continue
            if term not in searchable_basis and compact.find(term) <= 4:
                findings.append(
                    Finding(
                        "WARNING",
                        number,
                        "ANTECEDENT_BASIS",
                        f"English text"{term}"English text. ",
                    )
                )
        previous_text += compact

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("claims", type=Path, help="UTF-8 claims text file")
    parser.add_argument("--json", action="store_true", help="Output findings as JSON")
    args = parser.parse_args()

    text = args.claims.read_text(encoding="utf-8")
    findings = audit(text)
    if args.json:
        print(json.dumps([finding.__dict__ for finding in findings], ensure_ascii=False, indent=2))
    elif not findings:
        print("PASS: English text. ")
    else:
        for finding in findings:
            location = f"English text{finding.claim}" if finding.claim else "English text"
            print(f"{finding.level}\t{location}\t{finding.code}\t{finding.message}")
        errors = sum(finding.level == "ERROR" for finding in findings)
        warnings = sum(finding.level == "WARNING" for finding in findings)
        print(f"\nEnglish text: {errors} English text, {warnings} English text")

    return 1 if any(finding.level == "ERROR" for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
