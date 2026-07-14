#!/usr/bin/env python3
"""Block simple release regressions without third-party dependencies."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


CORE_SKILLS = {
    "bioinformatics-workbench",
    "journal-selection-advisor",
    "journal-submission-normalizer",
    "polish-sci-figures",
    "research-integrity-guardrail",
}
REQUIRED_ROOT_FILES = {
    "README.md",
    "GETTING_STARTED.md",
    "QUALITY_STANDARD.md",
    "SKILL_INDEX.md",
    "LICENSE",
}
LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")
NON_ENGLISH = re.compile(r"[\u4e00-\u9fff\ufffd]")


def skill_dirs(skill_root: Path) -> list[Path]:
    return sorted(path for path in skill_root.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())


def public_text_files(root: Path, skills: list[Path]) -> list[Path]:
    files = [root / name for name in REQUIRED_ROOT_FILES if name != "LICENSE"]
    files += [path for skill in skills for path in skill.rglob("*.md")]
    files += [path for skill in skills for path in skill.rglob("*.yaml")]
    files += [root / "showcase/elife-tea-seq-figure-3/README.md"]
    return files


def validate_frontmatter(path: Path, expected_name: str, errors: list[str]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        errors.append(f"{path}: missing opening frontmatter delimiter")
        return
    try:
        end = lines.index("---", 1)
    except ValueError:
        errors.append(f"{path}: missing closing frontmatter delimiter")
        return
    fields = dict(line.split(":", 1) for line in lines[1:end] if ":" in line)
    name = fields.get("name", "").strip().strip("\"'")
    if name != expected_name:
        errors.append(f"{path}: frontmatter name must be {expected_name}")
    if not fields.get("description", "").strip():
        errors.append(f"{path}: missing frontmatter description")


def validate_text(path: Path, root: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if NON_ENGLISH.search(text):
        errors.append(f"{path}: public text contains non-English or corrupted characters")
    for raw_link in LINK.findall(text):
        link = raw_link.split("#", 1)[0]
        if not link or "://" in link or link.startswith("mailto:"):
            continue
        target = (path.parent / link).resolve()
        if not target.exists() or (root not in target.parents and target != root):
            errors.append(f"{path}: broken local link {raw_link}")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    for name in REQUIRED_ROOT_FILES:
        if not (root / name).is_file():
            errors.append(f"missing root file: {name}")

    skill_root = root / "skills"
    skills = skill_dirs(skill_root) if skill_root.is_dir() else []
    actual_names = {skill.name for skill in skills}
    missing_core = CORE_SKILLS - actual_names
    if missing_core:
        errors.append(f"missing Core skills: {sorted(missing_core)}")

    for skill in skills:
        metadata = skill / "agents/openai.yaml"
        validate_frontmatter(skill / "SKILL.md", skill.name, errors)
        if not metadata.is_file() or "display_name:" not in metadata.read_text(encoding="utf-8"):
            errors.append(f"{skill.name}: missing display_name metadata")

    for path in public_text_files(root, skills):
        if path.is_file():
            validate_text(path, root, errors)

    for path in [root / ".claude-plugin/plugin.json", root / ".claude-plugin/marketplace.json"]:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{path}: invalid JSON ({exc})")

    showcase = root / "showcase/elife-tea-seq-figure-3"
    for name in ["figure3a-d-atlas-rerender.png", "figure3e-marker-heatmap-rerender.png", "reproduce_elife_63632_figure3_umaps.py"]:
        if not (showcase / name).is_file():
            errors.append(f"missing showcase asset: {name}")

    if errors:
        print("Release check failed:")
        print("\n".join(f"- {error}" for error in errors))
        return 1
    print(f"Release check passed for {len(skills)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
