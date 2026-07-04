"""Shell, hook, dependency-install, and network-call checks."""

from __future__ import annotations

import ipaddress
import json
import re
from pathlib import Path
from urllib.parse import urlparse

from report import Finding, make_finding

SAFE_DOMAINS = {"example.com", "example.org", "example.net", "localhost"}
SAFE_NETWORKS = tuple(
    ipaddress.ip_network(value)
    for value in ("192.0.2.0/24", "198.51.100.0/24", "203.0.113.0/24", "127.0.0.0/8")
)

TEXT_RULES: tuple[dict[str, object], ...] = (
    {
        "rule_id": "shell-curl-pipe",
        "severity": "high",
        "category": "shell_risk",
        "pattern": r"\bcurl\b[^\n|]*\|[ \t]*(sh|bash|zsh)\b",
        "message": "Shell snippet downloads content and pipes it into a shell.",
        "recommendation": "Avoid download-and-execute patterns; require reviewable local scripts instead.",
    },
    {
        "rule_id": "shell-wget-pipe",
        "severity": "high",
        "category": "shell_risk",
        "pattern": r"\bwget\b[^\n|]*\|[ \t]*(sh|bash|zsh)\b",
        "message": "Shell snippet downloads content and pipes it into a shell.",
        "recommendation": "Avoid download-and-execute patterns; require reviewable local scripts instead.",
    },
    {
        "rule_id": "shell-powershell-download-exec",
        "severity": "high",
        "category": "shell_risk",
        "pattern": r"\b(iex|invoke-expression)\b.*\b(downloadstring|downloadfile|iwr|irm|invoke-webrequest|invoke-restmethod)\b|\b(downloadstring|downloadfile|iwr|irm|invoke-webrequest|invoke-restmethod)\b.*\b(iex|invoke-expression)\b",
        "message": "PowerShell snippet appears to download and execute remote content.",
        "recommendation": "Avoid PowerShell download-and-execute patterns and document any network access.",
    },
    {
        "rule_id": "shell-base64-exec",
        "severity": "high",
        "category": "hidden_behavior",
        "pattern": r"\bbase64\b[^\n|]*(--decode|-d)[^\n|]*\|[ \t]*(sh|bash|zsh|python|perl|ruby|powershell)\b",
        "message": "Snippet decodes base64 content and executes it.",
        "recommendation": "Remove encoded execution and keep scripts readable.",
    },
    {
        "rule_id": "python-subprocess-shell-true",
        "severity": "high",
        "category": "shell_risk",
        "pattern": r"\bsubprocess\.(run|call|Popen|check_output|check_call)\([^)\n]*shell[ \t]*=[ \t]*True",
        "message": "Python subprocess call enables shell=True.",
        "recommendation": "Use argument arrays with shell=False unless shell behavior is explicitly required and reviewed.",
    },
    {
        "rule_id": "runtime-package-install",
        "severity": "medium",
        "category": "dependency_install_risk",
        "pattern": r"\b((python|python3|py)[ \t]+-m[ \t]+pip|pip|pip3|npm|pnpm|yarn)[ \t]+(install|add)\b",
        "message": "Runtime command appears to install packages.",
        "recommendation": "Move dependency installation to documented setup steps and require user consent.",
    },
)


def _first_regex_match(text: str, pattern: str) -> tuple[int, str] | None:
    compiled = re.compile(pattern, re.IGNORECASE)
    for line_number, line in enumerate(text.splitlines(), start=1):
        if compiled.search(line):
            return line_number, line
    return None


def _is_documentation_safe_host(host: str) -> bool:
    normalized = host.lower().strip("[]")
    if normalized in SAFE_DOMAINS or normalized.endswith(".example.com"):
        return True
    try:
        ip = ipaddress.ip_address(normalized)
    except ValueError:
        return False
    return any(ip in network for network in SAFE_NETWORKS)


def _network_findings(relative_path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    seen_hosts: set[str] = set()
    for line_number, line in enumerate(text.splitlines(), start=1):
        for url in re.findall(r"https?://[^\s\"'`<>)]+" , line, flags=re.IGNORECASE):
            host = urlparse(url).hostname
            if not host or _is_documentation_safe_host(host) or host in seen_hosts:
                continue
            seen_hosts.add(host)
            findings.append(
                make_finding(
                    rule_id="network-call-unknown-domain",
                    severity="medium",
                    category="network_exfiltration",
                    file=relative_path,
                    line=line_number,
                    message="File references a network endpoint outside documentation-safe hosts.",
                    evidence=line,
                    recommendation="Document why network access is needed or remove the call.",
                )
            )
    return findings


def scan_text(path: Path, relative_path: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for rule in TEXT_RULES:
        match = _first_regex_match(text, str(rule["pattern"]))
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
    findings.extend(_network_findings(relative_path, text))
    return findings


def scan_package_json(path: Path, relative_path: str, text: str) -> list[Finding]:
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    scripts = data.get("scripts", {})
    if not isinstance(scripts, dict):
        return []
    findings: list[Finding] = []
    for hook in ("preinstall", "install", "postinstall", "prepare"):
        value = scripts.get(hook)
        if not isinstance(value, str):
            continue
        if hook == "postinstall":
            findings.append(
                make_finding(
                    rule_id="npm-postinstall-hook",
                    severity="high",
                    category="unsafe_hook",
                    file=relative_path,
                    line=None,
                    message="package.json defines a postinstall hook.",
                    evidence=f"scripts.{hook}: {value}",
                    recommendation="Remove lifecycle hooks unless they are essential, documented, and reviewed.",
                )
            )
        findings.extend(scan_text(path, relative_path, value))
    return findings
