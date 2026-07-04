"""Destructive file-operation and credential-access checks."""

from __future__ import annotations

import re
from pathlib import Path

from report import Finding, make_finding


TEXT_RULES: tuple[dict[str, object], ...] = (
    {
        "rule_id": "file-rm-rf",
        "severity": "high",
        "category": "destructive_file_operation",
        "pattern": r"\brm\s+-[A-Za-z]*r[A-Za-z]*f[A-Za-z]*\b|\bRemove-Item\b[^\n]*\b-Recurse\b[^\n]*\b-Force\b",
        "message": "Command performs a recursive forced delete.",
        "recommendation": "Avoid destructive recursive deletes or constrain them to explicit temporary paths.",
    },
    {
        "rule_id": "file-recursive-delete-root-or-home",
        "severity": "critical",
        "category": "destructive_file_operation",
        "pattern": r"\brm\s+-[A-Za-z]*r[A-Za-z]*f[A-Za-z]*\s+(/|~|\$HOME|%USERPROFILE%|[A-Za-z]:\\)|\bshutil\.rmtree\([\"'](/|~|[A-Za-z]:\\)",
        "message": "Recursive delete appears to target root, home, or an absolute drive path.",
        "recommendation": "Remove broad destructive deletes and require explicit user approval for file removal.",
    },
    {
        "rule_id": "credential-dotenv-read",
        "severity": "high",
        "category": "credential_access",
        "pattern": r"\b(open|read_text|cat|type|Get-Content|read)\b[^\n]*(\.env\b|\.env\.)",
        "message": "File operation appears to read .env content.",
        "recommendation": "Do not read environment files unless the user explicitly authorizes secret handling.",
    },
    {
        "rule_id": "credential-ssh-key-read",
        "severity": "critical",
        "category": "credential_access",
        "pattern": r"\.ssh[/\\](id_rsa|id_ed25519|config)",
        "message": "File operation references SSH key material or SSH configuration.",
        "recommendation": "Remove access to SSH credentials from skill scripts.",
    },
    {
        "rule_id": "credential-cloud-config-read",
        "severity": "critical",
        "category": "credential_access",
        "pattern": r"\.aws[/\\]credentials|\.config[/\\]gcloud|azure[/\\](credentials|profile)|AZURE_CLIENT_SECRET",
        "message": "File operation references cloud credential material.",
        "recommendation": "Remove access to cloud credentials and rely on explicit user-provided inputs.",
    },
    {
        "rule_id": "credential-github-token-read",
        "severity": "critical",
        "category": "credential_access",
        "pattern": r"\bGITHUB_TOKEN\b|\bGH_TOKEN\b|\bghp_[A-Za-z0-9_]+",
        "message": "File or script references GitHub token material.",
        "recommendation": "Avoid reading or printing GitHub tokens; request scoped access through documented flows.",
    },
    {
        "rule_id": "env-mass-dump",
        "severity": "high",
        "category": "credential_access",
        "pattern": r"\bos\.environ\b|\bprintenv\b|(^|[;&|` \t])env([ \t;&|`]|$)",
        "message": "Command or script appears to dump environment variables.",
        "recommendation": "Read only explicitly required variables and never dump the full environment.",
    },
    {
        "rule_id": "hidden-dotfile-write",
        "severity": "medium",
        "category": "hidden_behavior",
        "pattern": r">\s*(~[/\\])?\.[A-Za-z0-9_-]+|\bopen\([\"'][^\"']*[/\\]?\.[A-Za-z0-9_-]+[\"']\s*,\s*[\"'][wa]",
        "message": "File operation appears to write a hidden dotfile.",
        "recommendation": "Document hidden file writes or avoid them unless the user explicitly requests persistent state.",
    },
)

IGNORED_HIDDEN_WRITES = (".cache", ".log", ".gitignore", ".env.example")


def _first_regex_match(text: str, pattern: str, *, ignore_hidden_examples: bool = False) -> tuple[int, str] | None:
    compiled = re.compile(pattern, re.IGNORECASE)
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not compiled.search(line):
            continue
        if ignore_hidden_examples and any(marker in line for marker in IGNORED_HIDDEN_WRITES):
            continue
        return line_number, line
    return None


def scan_text(path: Path, relative_path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for rule in TEXT_RULES:
        ignore_hidden_examples = rule["rule_id"] == "hidden-dotfile-write"
        match = _first_regex_match(
            text,
            str(rule["pattern"]),
            ignore_hidden_examples=ignore_hidden_examples,
        )
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
