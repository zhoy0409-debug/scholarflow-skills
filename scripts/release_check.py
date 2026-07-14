#!/usr/bin/env python3
"""Block simple release regressions without third-party dependencies."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


EXPECTED_SKILLS = {
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


def public_text_files(root: Path) -> list[Path]:
    files = [root / name for name in REQUIRED_ROOT_FILES if name != "LICENSE"]
    files += list((root / "skills").glob("*/SKILL.md"))
    files += list((root / "skills").glob("*/agents/openai.yaml"))
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
    if fields.get("name", "").strip() != expected_name:
        errors.append(f"{path}: frontmatter name must be {expected_name}")
    if not fields.get("description", "").strip():
        errors.append(f"{path}: missing frontmatter description")


def validate_links(path: Path, root: Path, errors: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    if re.search(r"[\u4e00-\u9fff\ufffd]|鈥", text):
        errors.append(f"{path}: public text contains non-English or corrupted characters")
    for raw_link in LINK.findall(text):
        link = raw_link.split("#", 1)[0]
        if not link or "://" in link or link.startswith("mailto:"):
            continue
        target = (path.parent / link).resolve()
        if not target.exists() or root not in target.parents and target != root:
            errors.append(f"{path}: broken local link {raw_link}")


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors: list[str] = []
    for name in REQUIRED_ROOT_FILES:
        if not (root / name).is_file():
            errors.append(f"missing root file: {name}")

    skill_root = root / "skills"
    actual_skills = {path.name for path in skill_root.iterdir() if path.is_dir()} if skill_root.is_dir() else set()
    if actual_skills != EXPECTED_SKILLS:
        errors.append(f"skills must be exactly {sorted(EXPECTED_SKILLS)}, found {sorted(actual_skills)}")

    for name in EXPECTED_SKILLS:
        skill = skill_root / name / "SKILL.md"
        metadata = skill_root / name / "agents/openai.yaml"
        if not skill.is_file() or not metadata.is_file():
            errors.append(f"{name}: missing SKILL.md or agents/openai.yaml")
            continue
        validate_frontmatter(skill, name, errors)
        if "display_name:" not in metadata.read_text(encoding="utf-8"):
            errors.append(f"{metadata}: missing display_name")

    for path in public_text_files(root):
        if path.is_file():
            validate_links(path, root, errors)

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
    print("Release check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
