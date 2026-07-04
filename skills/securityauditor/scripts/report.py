"""Shared reporting primitives for skill-security-auditor."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from typing import Iterable

SEVERITIES: tuple[str, ...] = ("info", "low", "medium", "high", "critical")
SEVERITY_RANK: dict[str, int] = {severity: index for index, severity in enumerate(SEVERITIES)}
CATEGORIES: tuple[str, ...] = (
    "prompt_injection",
    "credential_access",
    "network_exfiltration",
    "destructive_file_operation",
    "shell_risk",
    "dependency_install_risk",
    "misleading_metadata",
    "permission_expansion",
    "hidden_behavior",
    "unsafe_hook",
)


@dataclass(frozen=True)
class Finding:
    rule_id: str
    severity: str
    category: str
    file: str
    line: int | None
    message: str
    evidence: str
    recommendation: str


@dataclass
class ScanResult:
    findings: list[Finding]
    scanned_files: int
    skipped_files: list[str]
    errors: list[str]


def validate_severity(severity: str) -> str:
    if severity not in SEVERITY_RANK:
        raise ValueError(f"Unknown severity: {severity}")
    return severity


def validate_category(category: str) -> str:
    if category not in CATEGORIES:
        raise ValueError(f"Unknown category: {category}")
    return category


def severity_at_or_above(severity: str, threshold: str) -> bool:
    validate_severity(severity)
    validate_severity(threshold)
    return SEVERITY_RANK[severity] >= SEVERITY_RANK[threshold]


def sort_findings(findings: Iterable[Finding]) -> list[Finding]:
    return sorted(
        findings,
        key=lambda finding: (
            -SEVERITY_RANK[validate_severity(finding.severity)],
            finding.file,
            finding.line if finding.line is not None else 0,
            finding.rule_id,
            finding.evidence,
        ),
    )


def clip_evidence(evidence: str, limit: int = 200) -> str:
    cleaned = " ".join(evidence.strip().split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 1].rstrip() + "…"


def make_finding(
    *,
    rule_id: str,
    severity: str,
    category: str,
    file: str,
    line: int | None,
    message: str,
    evidence: str,
    recommendation: str,
) -> Finding:
    validate_severity(severity)
    validate_category(category)
    return Finding(
        rule_id=rule_id,
        severity=severity,
        category=category,
        file=file,
        line=line,
        message=message,
        evidence=clip_evidence(evidence),
        recommendation=recommendation,
    )


def findings_by_severity(findings: Iterable[Finding]) -> dict[str, int]:
    counts = {severity: 0 for severity in SEVERITIES}
    for finding in findings:
        counts[validate_severity(finding.severity)] += 1
    return counts


def result_to_dict(result: ScanResult) -> dict[str, object]:
    sorted_findings = sort_findings(result.findings)
    return {
        "summary": {
            "scanned_files": result.scanned_files,
            "skipped_files": len(result.skipped_files),
            "errors": len(result.errors),
            "findings": len(sorted_findings),
            "findings_by_severity": findings_by_severity(sorted_findings),
        },
        "findings": [asdict(finding) for finding in sorted_findings],
        "skipped_files": sorted(result.skipped_files),
        "errors": sorted(result.errors),
    }


def render_json(result: ScanResult) -> str:
    return json.dumps(result_to_dict(result), indent=2, ensure_ascii=False)


def render_text(result: ScanResult, *, fail_on: str = "high") -> str:
    validate_severity(fail_on)
    findings = sort_findings(result.findings)
    lines: list[str] = [
        "Skill Security Audit Report",
        f"Scanned files: {result.scanned_files}",
        f"Skipped files: {len(result.skipped_files)}",
        f"Errors: {len(result.errors)}",
        f"Findings: {len(findings)}",
    ]
    if not findings:
        lines.append("No findings.")
    elif not any(severity_at_or_above(finding.severity, fail_on) for finding in findings):
        lines.append(f"No findings at or above threshold: {fail_on}.")

    for severity in reversed(SEVERITIES):
        severity_findings = [finding for finding in findings if finding.severity == severity]
        if not severity_findings:
            continue
        lines.extend(("", severity.upper()))
        for finding in severity_findings:
            location = finding.file
            if finding.line is not None:
                location = f"{location}:{finding.line}"
            lines.extend(
                (
                    f"- [{finding.rule_id}] {location}",
                    f"  Category: {finding.category}",
                    f"  Message: {finding.message}",
                    f"  Evidence: {finding.evidence}",
                    f"  Recommendation: {finding.recommendation}",
                )
            )

    if result.skipped_files:
        lines.extend(("", "Skipped files"))
        lines.extend(f"- {path}" for path in sorted(result.skipped_files))

    if result.errors:
        lines.extend(("", "Errors"))
        lines.extend(f"- {error}" for error in sorted(result.errors))

    return "\n".join(lines)


def exit_code_for_threshold(result: ScanResult, threshold: str) -> int:
    validate_severity(threshold)
    if any(severity_at_or_above(finding.severity, threshold) for finding in result.findings):
        return 1
    return 0
