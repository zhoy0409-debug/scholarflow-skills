#!/usr/bin/env python3
"""Check whether required ScholarFlow Manuscript Studio workflow artifacts exist and look usable."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass, asdict
from pathlib import Path


COMMON_ARTIFACTS = [
    "scholarflow_manuscript_config.json",
    "source_map.md",
    "research_dossier.md",
    "exemplar_learning_dossier.md",
    "style_profile.md",
    "citation_support_bank.md",
    "confirmed_motivation.md",
    "section_blueprints.md",
    "writing_rationale_matrix.md",
]
FINAL_ARTIFACTS = [
    "final_artifact_manifest.md",
    "final_paper/main.tex",
]
PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME)\b|\[\[|\]\]|\?\?", re.IGNORECASE)


@dataclass
class ArtifactFinding:
    level: str
    path: str
    message: str


def check_file(root: Path, rel: str, min_chars: int) -> list[ArtifactFinding]:
    path = root / rel
    findings: list[ArtifactFinding] = []
    if not path.exists():
        findings.append(ArtifactFinding("ERROR", rel, "required artifact is missing"))
        return findings
    if path.is_file():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if len(text.strip()) < min_chars:
            findings.append(ArtifactFinding("WARN", rel, f"artifact is short: {len(text.strip())} characters"))
        if PLACEHOLDER_RE.search(text):
            findings.append(ArtifactFinding("ERROR", rel, "unresolved placeholder markers remain"))
    return findings


def audit(root: Path, min_chars: int = 120) -> list[ArtifactFinding]:
    findings: list[ArtifactFinding] = []
    for rel in COMMON_ARTIFACTS + FINAL_ARTIFACTS:
        findings.extend(check_file(root, rel, min_chars))
    config_path = root / "scholarflow_manuscript_config.json"
    if config_path.exists():
        try:
            json.loads(config_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            findings.append(ArtifactFinding("ERROR", "scholarflow_manuscript_config.json", f"invalid JSON: {exc}"))
    return findings


def to_markdown(findings: list[ArtifactFinding]) -> str:
    lines = ["# Artifact Check", "", f"- Status: {'PASS' if not any(f.level == 'ERROR' for f in findings) else 'FAIL'}", ""]
    if findings:
        lines.append("## Findings")
        lines.append("")
        lines.extend(f"- **{f.level}** `{f.path}`: {f.message}" for f in findings)
    else:
        lines.extend(["## Findings", "", "- None"])
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_dir", nargs="?", default="paper_rewriting_output")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    findings = audit(Path(args.output_dir))
    if args.write:
        (Path(args.output_dir) / "artifact_check.md").write_text(to_markdown(findings), encoding="utf-8")
    if args.json:
        print(json.dumps([asdict(f) for f in findings], ensure_ascii=False, indent=2))
    if args.markdown or not args.json:
        print(to_markdown(findings))
    return 1 if any(f.level == "ERROR" for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
