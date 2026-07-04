---
name: securityauditor
description: Static security audit workflow for Codex skills, agent skills, SKILL.md files, bundled scripts, hooks, shell snippets, suspicious file operations, prompt-injection instructions, credential access, permission expansion, and supply-chain risk. Use when reviewing third-party or newly authored skills before installation, publication, CI gating, or public release.
---

# Skill Security Auditor

Use this skill to audit third-party or newly authored Codex and agent skill directories before installing, sharing, publishing, or trusting them.

Invoke the installed skill as `$securityauditor`. In chat surfaces that expose slash skill invocation, use `/securityauditor`.

Do not use this skill as proof that a skill is safe. It is a static review aid that detects common suspicious patterns and highlights areas that need human review.

## Workflow

1. Inspect the target path and confirm it is a skill directory or repository.
2. Run the scanner without executing any scanned files.
3. Review findings by severity and category.
4. Read `references/risk-patterns.md` when tuning or explaining a rule.
5. Read `references/safe-skill-review-checklist.md` before installation or publication decisions.
6. Recommend the smallest safe next action, such as removing a risky hook, documenting behavior, or asking the maintainer for clarification.

## Scripts

- `scripts/scan_skill.py`: scan a skill directory or repository.
  - Text report: `python scripts/scan_skill.py /path/to/skill`
  - JSON report: `python scripts/scan_skill.py /path/to/skill --json`
  - CI gate: `python scripts/scan_skill.py /path/to/skill --fail-on high`
- `scripts/check_prompt_injection.py`: prompt-injection and hidden-instruction checks.
- `scripts/check_shell_risk.py`: shell, hook, dependency-install, and network-call checks.
- `scripts/check_file_operations.py`: destructive file-operation and credential-access checks.
- `scripts/report.py`: shared finding, report, JSON, and exit-code helpers.

## Output Expectations

- Summarize findings by severity: `info`, `low`, `medium`, `high`, `critical`.
- Include file and line when available.
- Distinguish confirmed static matches from assumptions about intent.
- Avoid alarmist language and avoid claiming a scan proves safety.
- Prefer JSON output for CI and text output for human review.

## Safety Boundaries

- Do not execute untrusted scanned files.
- Do not install dependencies from scanned skills.
- Do not make network requests during review.
- Do not modify, delete, or auto-fix scanned files.
- Do not transmit file contents outside the local environment.
- Do not invent results or claim that a limited scan found no possible risk.
