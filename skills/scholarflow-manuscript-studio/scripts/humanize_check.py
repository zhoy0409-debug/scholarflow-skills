#!/usr/bin/env python3
"""Validate a ScholarFlow Manuscript Studio humanization matrix and scan for common AI-text patterns."""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path


AI_CONNECTORS = [
    "firstly", "secondly", "thirdly", "finally", "in conclusion", "to sum up",
    "furthermore", "moreover", "additionally", "it is worth noting",
    "it should be pointed out", "plays a crucial role", "significant implications",
    "comprehensive analysis", "robust framework", "from this perspective",
]

CNKI_DIMENSIONS = (
    "sentence structure",
    "paragraph similarity",
    "information density",
    "connector frequency",
    "term-context matching",
)


@dataclass
class HumanizeCheckResult:
    path: str
    ok: bool
    matrix_rows: int = 0
    manuscript_paragraphs: int = 0
    coverage_ratio: float = 0.0
    sentence_length_stddev: float = 0.0
    connector_density: float = 0.0
    findings: list[str] = field(default_factory=list)


def split_table_line(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    return bool(cells) and all(cell and set(cell) <= {"-", ":", " "} for cell in cells)


def table_rows(text: str) -> tuple[list[str], list[list[str]]]:
    rows: list[list[str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not (line.startswith("|") and line.endswith("|")):
            continue
        cells = split_table_line(line)
        if is_separator(cells):
            continue
        rows.append(cells)
    return (rows[0], rows[1:]) if rows else ([], [])


def paragraphs(text: str) -> list[str]:
    parts = re.split(r"\n\s*\n+", text)
    return [re.sub(r"\s+", " ", part).strip() for part in parts if len(part.strip()) > 50]


def sentence_lengths(text: str) -> list[int]:
    sentences = re.split(r"[.!?;:\n]+", text)
    return [len(sentence.strip()) for sentence in sentences if 5 < len(sentence.strip()) < 300]


def connector_count(text: str) -> int:
    lowered = text.lower()
    return sum(lowered.count(connector) for connector in AI_CONNECTORS)


def check_matrix(matrix_path: Path, manuscript_text: str) -> HumanizeCheckResult:
    result = HumanizeCheckResult(str(matrix_path), False)
    if not matrix_path.exists():
        result.findings.append("humanize_matrix.md not found")
        return result
    matrix_text = matrix_path.read_text(encoding="utf-8", errors="ignore")
    header, rows = table_rows(matrix_text)
    if not header:
        result.findings.append("humanize_matrix.md has no parseable markdown table")
        return result
    result.matrix_rows = len(rows)
    result.manuscript_paragraphs = len(paragraphs(manuscript_text))
    if result.manuscript_paragraphs:
        result.coverage_ratio = result.matrix_rows / result.manuscript_paragraphs
    if result.coverage_ratio < 0.5 and result.manuscript_paragraphs > 2:
        result.findings.append(
            f"Coverage is {result.coverage_ratio:.0%}: {result.matrix_rows} matrix rows for "
            f"{result.manuscript_paragraphs} manuscript paragraphs."
        )
    header_text = " ".join(cell.lower() for cell in header)
    for column in ("ai pattern", "detection", "severity", "change"):
        if column not in header_text:
            result.findings.append(f"Missing expected column: {column}")
    empty_rows = [idx for idx, row in enumerate(rows, start=1) if any(not cell.strip() for cell in row)]
    if empty_rows:
        result.findings.append(f"Rows with empty cells: {empty_rows[:8]}")
    dimension_hits = set()
    for row in rows:
        joined = " ".join(row).lower()
        for dimension in CNKI_DIMENSIONS:
            if dimension in joined:
                dimension_hits.add(dimension)
    missing_dimensions = set(CNKI_DIMENSIONS) - dimension_hits
    if result.matrix_rows > 2 and missing_dimensions:
        result.findings.append(f"Detection dimensions not covered: {', '.join(sorted(missing_dimensions))}")
    lengths = sentence_lengths(manuscript_text)
    if len(lengths) > 2:
        result.sentence_length_stddev = round(statistics.stdev(lengths), 2)
        if result.sentence_length_stddev < 6:
            result.findings.append("Sentence length variation is low; revise rhythm and paragraph structure.")
    if manuscript_text:
        result.connector_density = round(connector_count(manuscript_text) / (len(manuscript_text) / 1000), 2)
        if result.connector_density > 8:
            result.findings.append(f"Connector density is high: {result.connector_density}/1k characters.")
    if re.search(r"[-]{3,}", manuscript_text):
        result.findings.append("Long dash separators detected; use proper section headings or paragraph breaks.")
    result.ok = not result.findings
    return result


def report_markdown(result: HumanizeCheckResult) -> str:
    lines = [
        "# Humanize Check Report",
        "",
        f"- Matrix path: `{result.path}`",
        f"- Status: {'PASS' if result.ok else 'FAIL'}",
        f"- Matrix rows: {result.matrix_rows}",
        f"- Manuscript paragraphs: {result.manuscript_paragraphs}",
        f"- Coverage: {result.coverage_ratio:.0%}",
        f"- Sentence length stddev: {result.sentence_length_stddev}",
        f"- Connector density: {result.connector_density}/1k characters",
        "",
        "## Findings",
        "",
    ]
    lines.extend(f"- {finding}" for finding in result.findings) if result.findings else lines.append("- None")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", nargs="?", default="paper_rewriting_output")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    parser.add_argument("--write", action="store_true", help="Write humanize_report.md")
    args = parser.parse_args()
    out_dir = Path(args.output_dir)
    matrix_path = out_dir / "humanize_matrix.md"
    manuscript_parts = []
    for candidate in (out_dir / "final_paper.md", out_dir / "final_paper" / "main.tex"):
        if candidate.exists():
            manuscript_parts.append(candidate.read_text(encoding="utf-8", errors="ignore"))
    result = check_matrix(matrix_path, "\n\n".join(manuscript_parts))
    markdown = report_markdown(result)
    if args.write:
        (out_dir / "humanize_report.md").write_text(markdown, encoding="utf-8")
    if args.json:
        print(json.dumps(result.__dict__, ensure_ascii=False, indent=2))
    if args.markdown or not args.json:
        print(markdown)
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
