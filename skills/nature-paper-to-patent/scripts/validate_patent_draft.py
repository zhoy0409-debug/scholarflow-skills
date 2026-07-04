#!/usr/bin/env python3
"""Validate the structured JSON draft used by the patent package renderer."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Finding:
    level: str
    code: str
    message: str


def add(findings: list[Finding], level: str, code: str, message: str) -> None:
    findings.append(Finding(level, code, message))


def require_mapping(value: Any, findings: list[Finding], code: str, message: str) -> bool:
    if not isinstance(value, dict):
        add(findings, "ERROR", code, message)
        return False
    return True


def validate(data: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    for key in ("title", "claims", "specification", "abstract", "figures"):
        if key not in data or data.get(key) in (None, "", [], {}):
            add(findings, "ERROR", "MISSING_FIELD", f"Required field is missing or empty: {key}.")
    claims = data.get("claims", [])
    if not isinstance(claims, list) or not claims:
        add(findings, "ERROR", "CLAIMS", "claims must be a non-empty list.")
    else:
        numbers = []
        for claim in claims:
            if not require_mapping(claim, findings, "CLAIM_TYPE", "Each claim must be an object."):
                continue
            number = claim.get("number")
            numbers.append(number)
            if not isinstance(number, int):
                add(findings, "ERROR", "CLAIM_NUMBER", "Each claim must have an integer number.")
            if not str(claim.get("text", "")).strip():
                add(findings, "ERROR", "CLAIM_TEXT", f"Claim {number} has no text.")
        expected = list(range(1, len(numbers) + 1))
        if numbers != expected:
            add(findings, "ERROR", "CLAIM_SEQUENCE", f"Claim numbers must be consecutive: expected {expected}, found {numbers}.")
    spec = data.get("specification", {})
    if require_mapping(spec, findings, "SPECIFICATION_TYPE", "specification must be an object."):
        for field in ("technical_field", "background", "figure_descriptions", "embodiments"):
            if field not in spec:
                add(findings, "ERROR", "SPECIFICATION_FIELD", f"specification.{field} is required.")
        if "equations" not in spec:
            add(findings, "ERROR", "EQUATIONS_FIELD", "specification.equations is required; use an empty list when no equations are needed.")
        for equation in spec.get("equations", []) or []:
            if not isinstance(equation, dict) or not equation.get("latex"):
                add(findings, "ERROR", "EQUATION_LATEX", "Each equation must include a latex field.")
    figures = data.get("figures", [])
    if isinstance(figures, list):
        figure_numbers = {item.get("number") for item in figures if isinstance(item, dict)}
        abstract_figure_number = data.get("abstract_figure_number")
        if abstract_figure_number is not None and abstract_figure_number not in figure_numbers:
            add(findings, "ERROR", "ABSTRACT_FIGURE", "abstract_figure_number does not match any figure number.")
    else:
        add(findings, "ERROR", "FIGURES_TYPE", "figures must be a list.")
    evidence_ledger = data.get("evidence_ledger", [])
    source_ids = {item.get("id") for item in evidence_ledger if isinstance(item, dict)}
    for mapping in data.get("claim_feature_map", []) or []:
        if not isinstance(mapping, dict):
            add(findings, "ERROR", "FEATURE_MAP_TYPE", "claim_feature_map entries must be objects.")
            continue
        claim_number = mapping.get("claim_number")
        if claim_number not in [claim.get("number") for claim in claims if isinstance(claim, dict)]:
            add(findings, "ERROR", "UNKNOWN_CLAIM", f"Feature map references unknown claim: {claim_number}.")
        if not str(mapping.get("feature", "")).strip():
            add(findings, "ERROR", "EMPTY_FEATURE", "Feature map entry has no feature text.")
        for evidence_id in mapping.get("evidence_ids", []) or []:
            if source_ids and evidence_id not in source_ids:
                add(findings, "ERROR", "UNKNOWN_EVIDENCE_ID", f"Unknown evidence id: {evidence_id}.")
    return findings


def format_report(findings: list[Finding]) -> str:
    if not findings:
        return "PASS: patent draft structure is valid.\n"
    lines = ["# Patent Draft Validation Report", ""]
    for item in findings:
        lines.append(f"- **{item.level}** `{item.code}`: {item.message}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.draft.read_text(encoding="utf-8"))
    findings = validate(data)
    report = format_report(findings)
    if args.output:
        args.output.write_text(report, encoding="utf-8")
    else:
        print(report)
    return 1 if any(item.level == "ERROR" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
