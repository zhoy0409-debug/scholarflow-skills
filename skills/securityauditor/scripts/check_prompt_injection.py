"""Prompt-injection and hidden-instruction checks."""

from __future__ import annotations

import re
from pathlib import Path

from report import Finding, make_finding


RULES: tuple[dict[str, object], ...] = (
    {
        "rule_id": "prompt-ignore-instructions",
        "severity": "high",
        "category": "prompt_injection",
        "patterns": (
            r"\bignore\b.{0,80}\b(previous|prior|system|developer|user|higher[- ]priority)\b.{0,40}\binstructions?\b",
            r"\bdisregard\b.{0,80}\b(system|developer|user|previous|prior)\b.{0,40}\binstructions?\b",
        ),
        "message": "Instruction text appears to tell an agent to ignore higher-priority instructions.",
        "recommendation": "Remove hidden override instructions and keep skill behavior explicit.",
    },
    {
        "rule_id": "prompt-hide-behavior",
        "severity": "high",
        "category": "hidden_behavior",
        "patterns": (
            r"\bdo not disclose\b",
            r"\bhide (this|the) behavior\b",
            r"\bkeep (this|the) behavior secret\b",
            r"\bdo not tell (the )?user\b",
        ),
        "message": "Instruction text appears to hide behavior from the user or reviewer.",
        "recommendation": "Remove concealment language and document the behavior plainly.",
    },
    {
        "rule_id": "prompt-exfiltrate-secrets",
        "severity": "critical",
        "category": "credential_access",
        "patterns": (
            r"\bexfiltrat(e|es|ing)\b.{0,80}\b(secrets?|credentials?|tokens?|keys?)\b",
            r"\bsend\b.{0,80}\b(secrets?|credentials?|tokens?|keys?)\b",
            r"\bupload\b.{0,80}\b(secrets?|credentials?|tokens?|keys?)\b",
        ),
        "message": "Instruction text appears to request secret or credential disclosure.",
        "recommendation": "Remove any instruction that accesses or transmits secrets.",
    },
    {
        "rule_id": "prompt-disable-safety",
        "severity": "high",
        "category": "permission_expansion",
        "patterns": (
            r"\bdisable\b.{0,50}\b(safety|guardrails?|sandbox|policy|permissions?)\b",
            r"\bbypass\b.{0,50}\b(safety|guardrails?|sandbox|policy|permissions?)\b",
        ),
        "message": "Instruction text appears to weaken safety, policy, sandbox, or permission controls.",
        "recommendation": "Remove permission-expansion language and request explicit approval instead.",
    },
)


def _first_match_line(text: str, patterns: tuple[str, ...]) -> tuple[int, str] | None:
    compiled = [re.compile(pattern, re.IGNORECASE) for pattern in patterns]
    for line_number, line in enumerate(text.splitlines(), start=1):
        for pattern in compiled:
            if pattern.search(line):
                return line_number, line
    return None


def scan_text(path: Path, relative_path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for rule in RULES:
        match = _first_match_line(text, rule["patterns"])  # type: ignore[arg-type]
        if match is None:
            continue
        line_number, evidence = match
        findings.append(
            make_finding(
                rule_id=str(rule["rule_id"]),
                severity=str(rule["severity"]),
                category=str(rule["category"]),
                file=relative_path,
                line=line_number,
                message=str(rule["message"]),
                evidence=evidence,
                recommendation=str(rule["recommendation"]),
            )
        )
    return findings
