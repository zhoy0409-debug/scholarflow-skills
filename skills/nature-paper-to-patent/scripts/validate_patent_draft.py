#!/usr/bin/env python3
"""Validate traceability, completeness, and quality gates in a patent draft."""

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


SOURCE_ID = re.compile(r"^[PEFC]\d{3,}$")
PLACEHOLDER = re.compile(r"\[(?:TO CONFIRM|English text)[^\]]*\]", re.IGNORECASE)
VAGUE_RESULT = re.compile(r"(English text|English text|English text)")
QUALITY_THRESHOLDS = {
    "evidence_support": 4,
    "claim_architecture": 4,
    "terminology_consistency": 4,
    "enablement_detail": 3,
    "technical_effect_reasoning": 3,
}


@dataclass
class Finding:
    level: str
    code: str
    message: str


def add(findings: list[Finding], level: str, code: str, message: str) -> None:
    findings.append(Finding(level, code, message))


def validate(data: dict) -> list[Finding]:
    findings: list[Finding] = []
    required = (
        "title",
        "metadata",
        "source_analysis",
        "source_map",
        "terminology_ledger",
        "formula_inventory",
        "figure_inventory",
        "evidence_ledger",
        "claims",
        "claim_feature_map",
        "figures",
        "specification",
        "abstract",
        "quality_assessment",
    )
    for key in required:
        if key not in data:
            add(findings, "ERROR", "MISSING_KEY", f"English text: {key}. ")

    claims = data.get("claims", [])
    numbers = [claim.get("number") for claim in claims]
    if not claims:
        add(findings, "ERROR", "NO_CLAIMS", "English text. ")
    elif numbers != list(range(1, len(numbers) + 1)):
        add(findings, "ERROR", "CLAIM_SEQUENCE", f"English text: {numbers}. ")
    for claim in claims:
        text = str(claim.get("text", ""))
        if not text.strip():
            add(findings, "ERROR", "EMPTY_CLAIM", f"English text{claim.get('number')}English text. ")
        if PLACEHOLDER.search(text):
            add(
                findings,
                "ERROR",
                "CLAIM_PLACEHOLDER",
                f"English text{claim.get('number')}English text. ",
            )

    source_records = data.get("source_map", [])
    source_ids = set()
    for record in source_records:
        source_id = str(record.get("id", ""))
        if not SOURCE_ID.fullmatch(source_id):
            add(findings, "ERROR", "SOURCE_ID", f"English textID: {source_id!r}. ")
        if source_id in source_ids:
            add(findings, "ERROR", "DUPLICATE_SOURCE_ID", f"English textIDEnglish text: {source_id}. ")
        source_ids.add(source_id)
        if not record.get("locator"):
            add(findings, "WARNING", "SOURCE_LOCATOR", f"{source_id}English text, English text. ")

    canonical_terms = set()
    forbidden_aliases = set()
    for item in data.get("terminology_ledger", []):
        canonical = str(item.get("canonical_zh", "")).strip()
        if not canonical:
            add(findings, "ERROR", "CANONICAL_TERM", "English textcanonical_zh. ")
        elif canonical in canonical_terms:
            add(findings, "ERROR", "DUPLICATE_TERM", f"English text: {canonical}. ")
        canonical_terms.add(canonical)
        forbidden_aliases.update(
            str(alias).strip() for alias in item.get("forbidden_aliases", []) if str(alias).strip()
        )

    ledger_ids = set()
    for item in data.get("evidence_ledger", []):
        ledger_id = str(item.get("id", ""))
        if not ledger_id:
            add(findings, "ERROR", "LEDGER_ID", "English textID. ")
        elif ledger_id in ledger_ids:
            add(findings, "ERROR", "DUPLICATE_LEDGER_ID", f"English textIDEnglish text: {ledger_id}. ")
        ledger_ids.add(ledger_id)
        status = item.get("support_status")
        if status not in {"explicit", "inherent", "needs-confirmation", "unsupported"}:
            add(findings, "ERROR", "SUPPORT_STATUS", f"{ledger_id}English text: {status}. ")
        referenced = item.get("source_ids", [])
        if status in {"explicit", "inherent"} and not referenced:
            add(findings, "ERROR", "MISSING_SOURCE_LINK", f"{ledger_id}English textID. ")
        for source_id in referenced:
            if source_ids and source_id not in source_ids:
                add(findings, "ERROR", "UNKNOWN_SOURCE_ID", f"{ledger_id}English textID: {source_id}. ")

    mapped_claims = set()
    for mapping in data.get("claim_feature_map", []):
        claim_number = mapping.get("claim_number")
        mapped_claims.add(claim_number)
        if claim_number not in numbers:
            add(findings, "ERROR", "UNKNOWN_CLAIM", f"English text: {claim_number}. ")
        if not str(mapping.get("feature", "")).strip():
            add(findings, "ERROR", "EMPTY_FEATURE", "English text. ")
        evidence_ids = mapping.get("evidence_ids", [])
        if not evidence_ids:
            add(
                findings,
                "ERROR",
                "UNMAPPED_FEATURE",
                f"English text{claim_number}English text"{mapping.get('feature', '')}"English textID. ",
            )
        for evidence_id in evidence_ids:
            if evidence_id not in ledger_ids:
                add(
                    findings,
                    "ERROR",
                    "UNKNOWN_EVIDENCE_ID",
                    f"English text{claim_number}English textID: {evidence_id}. ",
                )
    for number in numbers:
        if number not in mapped_claims:
            add(findings, "ERROR", "CLAIM_NOT_MAPPED", f"English text{number}English text. ")
    formal_text = "\n".join(str(claim.get("text", "")) for claim in claims)
    formal_text += "\n" + json.dumps(data.get("specification", {}), ensure_ascii=False)
    for alias in sorted(forbidden_aliases):
        if alias in formal_text:
            add(findings, "ERROR", "FORBIDDEN_ALIAS", f"English text: {alias}. ")

    source_analysis = data.get("source_analysis", {})
    spec = data.get("specification", {})
    equations = spec.get("equations", [])
    formula_inventory = data.get("formula_inventory", [])
    for item in formula_inventory:
        source_id = item.get("source_id")
        if source_ids and source_id not in source_ids:
            add(findings, "ERROR", "FORMULA_INVENTORY_SOURCE", f"English textID: {source_id}. ")
        if not item.get("disposition"):
            add(findings, "ERROR", "FORMULA_DISPOSITION", f"English text{source_id}English text. ")
    expected_formula_count = source_analysis.get("formula_count_in_source")
    if isinstance(expected_formula_count, int) and expected_formula_count != len(formula_inventory):
        add(
            findings,
            "WARNING",
            "FORMULA_INVENTORY_COUNT",
            f"English text{expected_formula_count}English text, English text{len(formula_inventory)}English text. ",
        )
    if "equations" not in spec:
        add(findings, "ERROR", "EQUATIONS_ARRAY", "English textequationsEnglish text. ")
    if source_analysis.get("contains_core_formulas") and not equations:
        add(findings, "ERROR", "MISSING_CORE_EQUATIONS", "English text, English text. ")
    equation_numbers = [equation.get("number") for equation in equations]
    if equation_numbers and equation_numbers != list(range(1, len(equation_numbers) + 1)):
        add(findings, "ERROR", "EQUATION_SEQUENCE", f"English text: {equation_numbers}. ")
    for equation in equations:
        number = equation.get("number")
        if not equation.get("latex"):
            add(findings, "ERROR", "EQUATION_LATEX", f"English text{number}English textLaTeXEnglish text. ")
        if not equation.get("source_ids"):
            add(findings, "ERROR", "EQUATION_SOURCE", f"English text{number}English textID. ")
        for source_id in equation.get("source_ids", []):
            if source_ids and source_id not in source_ids:
                add(findings, "ERROR", "EQUATION_SOURCE", f"English text{number}English textID: {source_id}. ")
        if not equation.get("symbols"):
            add(findings, "ERROR", "EQUATION_SYMBOLS", f"English text{number}English text. ")
        if not equation.get("technical_role"):
            add(findings, "ERROR", "EQUATION_ROLE", f"English text{number}English text. ")

    figures = data.get("figures", [])
    for item in data.get("figure_inventory", []):
        source_id = item.get("source_id")
        if source_ids and source_id not in source_ids:
            add(findings, "ERROR", "FIGURE_INVENTORY_SOURCE", f"English textID: {source_id}. ")
        if not item.get("disposition"):
            add(findings, "ERROR", "FIGURE_DISPOSITION", f"English text{source_id}English text. ")
    figure_numbers = [figure.get("number") for figure in figures]
    if not figures:
        add(findings, "ERROR", "NO_FIGURES", "English text. ")
    elif figure_numbers != list(range(1, len(figure_numbers) + 1)):
        add(findings, "ERROR", "FIGURE_SEQUENCE", f"English text: {figure_numbers}. ")
    abstract_figure = data.get("abstract_figure_number")
    if abstract_figure not in figure_numbers:
        add(findings, "ERROR", "ABSTRACT_FIGURE", "English text. ")
    for figure in figures:
        if not figure.get("source_ids"):
            add(findings, "WARNING", "FIGURE_SOURCE", f"English text{figure.get('number')}English textIDEnglish text. ")
        for source_id in figure.get("source_ids", []):
            if source_ids and source_id not in source_ids:
                add(
                    findings,
                    "ERROR",
                    "FIGURE_SOURCE",
                    f"English text{figure.get('number')}English textID: {source_id}. ",
                )
        end_nodes = set(str(node.get("id")) for node in figure.get("nodes", []))
        for edge in figure.get("edges", []):
            end_nodes.discard(str(edge.get("from")))
        for node in figure.get("nodes", []):
            if str(node.get("id")) in end_nodes and VAGUE_RESULT.search(str(node.get("label", ""))):
                add(
                    findings,
                    "ERROR",
                    "VAGUE_FINAL_RESULT",
                    f"English text{figure.get('number')}English text. ",
                )

    for field in ("technical_field", "background", "embodiments", "figure_descriptions"):
        if not spec.get(field):
            add(findings, "ERROR", "SPEC_SECTION", f"English text: {field}. ")
    invention = spec.get("invention_content", {})
    for field in ("problem", "solution", "beneficial_effects"):
        if not invention.get(field):
            add(findings, "ERROR", "INVENTION_CONTENT", f"English text: {field}. ")

    abstract = re.sub(r"\s+", "", str(data.get("abstract", "")))
    if not abstract:
        add(findings, "ERROR", "EMPTY_ABSTRACT", "English text. ")
    elif len(abstract) > 300:
        add(findings, "WARNING", "ABSTRACT_LENGTH", f"English text{len(abstract)}English text, English text. ")

    quality = data.get("quality_assessment", {})
    if quality.get("status") not in {"review-draft", "incomplete-draft"}:
        add(
            findings,
            "WARNING",
            "DRAFT_STATUS",
            "quality_assessment.statusEnglish textreview-draftEnglish textincomplete-draft. ",
        )
    scores = quality.get("scores", {})
    for dimension, threshold in QUALITY_THRESHOLDS.items():
        item = scores.get(dimension)
        if not isinstance(item, dict) or not isinstance(item.get("score"), int):
            add(findings, "ERROR", "QUALITY_SCORE", f"English text: {dimension}. ")
            continue
        score = item["score"]
        if score < 1 or score > 5:
            add(findings, "ERROR", "QUALITY_RANGE", f"{dimension}English text1-5: {score}. ")
        elif score < threshold:
            add(
                findings,
                "ERROR",
                "QUALITY_THRESHOLD",
                f"{dimension}English text{score}, English text{threshold}. ",
            )
        if not str(item.get("evidence", "")).strip():
            add(findings, "WARNING", "QUALITY_EVIDENCE", f"{dimension}English text. ")

    if source_analysis.get("contains_core_formulas"):
        formula_item = scores.get("formula_coverage", {})
        if formula_item.get("score", 0) < 4:
            add(findings, "ERROR", "FORMULA_SCORE", "English text, formula_coverageEnglish text4. ")
    if figures:
        figure_item = scores.get("figure_alignment", {})
        if figure_item.get("score", 0) < 4:
            add(findings, "ERROR", "FIGURE_SCORE", "English text, figure_alignmentEnglish text4. ")

    return findings


def format_report(findings: list[Finding]) -> str:
    if not findings:
        return "PASS: English text, English text. \n"
    lines = [f"{item.level}\t{item.code}\t{item.message}" for item in findings]
    errors = sum(item.level == "ERROR" for item in findings)
    warnings = sum(item.level == "WARNING" for item in findings)
    lines.extend(("", f"English text: {errors} English text, {warnings} English text"))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("draft", type=Path, help="UTF-8 structured patent draft JSON")
    parser.add_argument("--report", type=Path, help="Write the validation report to a file")
    parser.add_argument("--json", action="store_true", help="Print findings as JSON")
    args = parser.parse_args()

    data = json.loads(args.draft.read_text(encoding="utf-8"))
    findings = validate(data)
    report = format_report(findings)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(report, encoding="utf-8")
    if args.json:
        print(json.dumps([item.__dict__ for item in findings], ensure_ascii=False, indent=2))
    else:
        print(report, end="")
    return 1 if any(item.level == "ERROR" for item in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
