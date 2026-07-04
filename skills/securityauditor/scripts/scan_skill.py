"""CLI scanner for Codex and agent skill supply-chain review."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import check_file_operations
import check_prompt_injection
import check_shell_risk
from report import (
    Finding,
    ScanResult,
    exit_code_for_threshold,
    make_finding,
    render_json,
    render_text,
)

TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".py",
    ".sh",
    ".bash",
    ".zsh",
    ".ps1",
    ".js",
    ".ts",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".cfg",
    ".ini",
    ".lock",
}
DEFAULT_SKIP_DIRS = {
    ".git",
    "node_modules",
    ".venv",
    "venv",
    "__pycache__",
    "dist",
    "build",
    "target",
    "vendor",
}
RISK_DESCRIPTION_TERMS = {
    "audit",
    "credential",
    "delete",
    "file",
    "hook",
    "install",
    "network",
    "permission",
    "risk",
    "scan",
    "script",
    "secret",
    "security",
    "shell",
}


def _relative_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _should_skip(path: Path, root: Path, include_deps: bool) -> bool:
    if include_deps:
        return False
    try:
        relative_parts = path.relative_to(root).parts
    except ValueError:
        relative_parts = path.parts
    return any(part in DEFAULT_SKIP_DIRS for part in relative_parts)


def _is_text_file(path: Path) -> bool:
    return path.name == "SKILL.md" or path.suffix.lower() in TEXT_EXTENSIONS


def _iter_candidate_files(root: Path, include_deps: bool) -> list[Path]:
    if root.is_file():
        return [root] if _is_text_file(root) else []
    candidates: list[Path] = []
    for path in root.rglob("*"):
        if path.is_dir():
            continue
        if _should_skip(path, root, include_deps):
            continue
        if _is_text_file(path):
            candidates.append(path)
    return sorted(candidates)


def _read_text(path: Path, max_file_size: int) -> tuple[str | None, str | None]:
    try:
        size = path.stat().st_size
    except OSError as exc:
        return None, f"{path}: cannot stat file: {exc}"
    if size > max_file_size:
        return None, "skip-size"
    try:
        data = path.read_bytes()
    except OSError as exc:
        return None, f"{path}: cannot read file: {exc}"
    if b"\x00" in data:
        return None, "skip-binary"
    try:
        return data.decode("utf-8"), None
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace"), None


def _parse_skill_description(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    frontmatter = text[3:end]
    for line in frontmatter.splitlines():
        if line.lower().startswith("description:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return ""


def _description_omits_risk(description: str) -> bool:
    words = set(re.findall(r"[a-z0-9_-]+", description.lower()))
    return not bool(words & RISK_DESCRIPTION_TERMS)


def _add_misleading_metadata_findings(root: Path, texts: dict[Path, str], findings: list[Finding]) -> None:
    skill_files = [path for path in texts if path.name == "SKILL.md"]
    for skill_file in skill_files:
        skill_dir = skill_file.parent
        description = _parse_skill_description(texts[skill_file])
        if not _description_omits_risk(description):
            continue
        script_prefix = (skill_dir / "scripts").as_posix()
        risky_script_findings = [
            finding
            for finding in findings
            if finding.severity in {"high", "critical"}
            and (root / finding.file).as_posix().startswith(script_prefix)
        ]
        if not risky_script_findings:
            continue
        findings.append(
            make_finding(
                rule_id="misleading-skill-description",
                severity="medium",
                category="misleading_metadata",
                file=_relative_path(root, skill_file),
                line=2,
                message="SKILL.md description does not disclose high-risk behavior found in sibling scripts.",
                evidence=f"description: {description or '(empty)'}",
                recommendation="Update metadata to accurately describe risky scripts or remove the risky behavior.",
            )
        )


def scan_target(target: Path, *, include_deps: bool = False, max_file_size: int = 1_048_576) -> ScanResult:
    root = target.resolve()
    findings: list[Finding] = []
    skipped_files: list[str] = []
    errors: list[str] = []
    scanned_files = 0
    texts: dict[Path, str] = {}

    for path in _iter_candidate_files(root, include_deps):
        relative_path = _relative_path(root, path)
        text, error = _read_text(path, max_file_size)
        if error == "skip-size":
            skipped_files.append(f"{relative_path} (larger than {max_file_size} bytes)")
            continue
        if error == "skip-binary":
            skipped_files.append(f"{relative_path} (binary)")
            continue
        if error is not None:
            errors.append(error)
            continue
        if text is None:
            continue
        scanned_files += 1
        texts[path] = text
        findings.extend(check_prompt_injection.scan_text(path, relative_path, text))
        findings.extend(check_shell_risk.scan_text(path, relative_path, text))
        if path.name == "package.json":
            findings.extend(check_shell_risk.scan_package_json(path, relative_path, text))
        findings.extend(check_file_operations.scan_text(path, relative_path, text))

    _add_misleading_metadata_findings(root, texts, findings)
    return ScanResult(
        findings=findings,
        scanned_files=scanned_files,
        skipped_files=skipped_files,
        errors=errors,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Audit Codex or agent skill directories for suspicious static patterns.",
    )
    parser.add_argument("target", help="Path to a skill directory or repository.")
    parser.add_argument("--json", action="store_true", dest="json_output", help="Emit JSON output.")
    parser.add_argument(
        "--fail-on",
        choices=("info", "low", "medium", "high", "critical"),
        default="high",
        help="Exit 1 when findings are at or above this severity. Default: high.",
    )
    parser.add_argument(
        "--max-file-size",
        type=int,
        default=1_048_576,
        help="Maximum text file size to scan in bytes. Default: 1048576.",
    )
    parser.add_argument(
        "--include-deps",
        action="store_true",
        help="Include dependency and build directories that are skipped by default.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    target = Path(args.target)
    if not target.exists():
        print(f"Invalid input: target does not exist: {target}", file=sys.stderr)
        return 2
    if args.max_file_size < 1:
        print("Invalid input: --max-file-size must be greater than zero.", file=sys.stderr)
        return 2
    try:
        result = scan_target(
            target,
            include_deps=args.include_deps,
            max_file_size=args.max_file_size,
        )
    except Exception as exc:  # pragma: no cover - defensive CLI boundary
        print(f"Scanner error: {exc}", file=sys.stderr)
        return 2

    if args.json_output:
        print(render_json(result))
    else:
        print(render_text(result, fail_on=args.fail_on))
    if result.errors:
        return 2
    return exit_code_for_threshold(result, args.fail_on)


if __name__ == "__main__":
    raise SystemExit(main())
