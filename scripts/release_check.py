#!/usr/bin/env python3
"""Block simple release regressions without third-party dependencies."""
from __future__ import print_function

import sys

if sys.version_info < (3, 10):
    print("Release check requires Python 3.10+.", file=sys.stderr)
    raise SystemExit(2)

import json
import hashlib
import re
from collections import defaultdict
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
RESOURCE_REFERENCE = re.compile(
    r"`((?:(?:\.\./)*)?(?:assets|config|modules|references|scripts|static|templates)/[A-Za-z0-9_./-]+)`"
)
NON_ENGLISH = re.compile(r"[\u4e00-\u9fff\ufffd]")


def skill_dirs(skill_root):
    return sorted(path for path in skill_root.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())


def public_text_files(root, skills):
    files = [root / name for name in REQUIRED_ROOT_FILES if name != "LICENSE"]
    files += [path for skill in skills for path in skill.rglob("*.md")]
    files += [path for skill in skills for path in skill.rglob("*.yaml")]
    files += [root / "showcase/elife-tea-seq-figure-3/README.md"]
    return files


def validate_frontmatter(path, expected_name, errors):
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0] != "---":
        errors.append("{}: missing opening frontmatter delimiter".format(path))
        return
    try:
        end = lines.index("---", 1)
    except ValueError:
        errors.append("{}: missing closing frontmatter delimiter".format(path))
        return
    fields = dict(line.split(":", 1) for line in lines[1:end] if ":" in line)
    name = fields.get("name", "").strip().strip("\"'")
    if name != expected_name:
        errors.append("{}: frontmatter name must be {}".format(path, expected_name))
    description_index = next((index for index, line in enumerate(lines[1:end], 1) if line.startswith("description:")), None)
    description = fields.get("description", "").strip().strip("\"'")
    if description_index is not None and description in {"|", "|-", ">", ">-"}:
        description = " ".join(
            line.strip() for line in lines[description_index + 1 : end] if line.startswith((" ", "\t"))
        )
    if not description:
        errors.append("{}: missing frontmatter description".format(path))
    elif not description.lower().startswith("use when "):
        errors.append("{}: description must begin with 'Use when'".format(path))


def validate_text(path, root, errors):
    text = path.read_text(encoding="utf-8-sig")
    if NON_ENGLISH.search(text):
        errors.append("{}: public text contains non-English or corrupted characters".format(path))
    for raw_link in LINK.findall(text):
        link = raw_link.split("#", 1)[0]
        if not link or "://" in link or link.startswith("mailto:"):
            continue
        target = (path.parent / link).resolve()
        if not target.exists() or (root not in target.parents and target != root):
            errors.append("{}: broken local link {}".format(path, raw_link))


def skill_owner(path, skills):
    return next((skill for skill in skills if skill in path.parents), None)


def validate_resource_references(path, root, skills, errors):
    text = path.read_text(encoding="utf-8-sig")
    skill = skill_owner(path, skills)
    for raw_path in RESOURCE_REFERENCE.findall(text):
        candidates = [(path.parent / raw_path).resolve()]
        if skill is not None and not raw_path.startswith("../"):
            candidates.append((skill / raw_path).resolve())
        if any(candidate.exists() and (candidate == root or root in candidate.parents) for candidate in candidates):
            continue
        errors.append("{}: referenced local resource does not exist: {}".format(path, raw_path))


def validate_duplicate_scripts(skill_root, errors):
    by_hash = defaultdict(list)
    for path in skill_root.rglob("*.py"):
        if path.name == "__init__.py" or path.stat().st_size < 128:
            continue
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        by_hash[digest].append(path)
    for paths in by_hash.values():
        if len(paths) > 1:
            rendered = ", ".join(str(path.relative_to(skill_root)) for path in paths)
            errors.append("duplicate Python script content: {}".format(rendered))


def main():
    root = Path(__file__).resolve().parents[1]
    errors = []
    for name in REQUIRED_ROOT_FILES:
        if not (root / name).is_file():
            errors.append("missing root file: {}".format(name))

    skill_root = root / "skills"
    skills = skill_dirs(skill_root) if skill_root.is_dir() else []
    actual_names = {skill.name for skill in skills}
    missing_core = CORE_SKILLS - actual_names
    if missing_core:
        errors.append("missing Core skills: {}".format(sorted(missing_core)))

    for skill in skills:
        metadata = skill / "agents/openai.yaml"
        validate_frontmatter(skill / "SKILL.md", skill.name, errors)
        if not metadata.is_file():
            errors.append("{}: missing agents/openai.yaml".format(skill.name))
            continue
        metadata_text = metadata.read_text(encoding="utf-8-sig")
        if "product_owner: Zhoy" not in metadata_text:
            errors.append("{}: product_owner must be Zhoy".format(skill.name))
        if "display_name:" not in metadata_text:
            errors.append("{}: missing display_name metadata".format(skill.name))
        elif "ownership:" in metadata_text:
            errors.append("{}: deprecated ownership metadata is not allowed".format(skill.name))

    for path in public_text_files(root, skills):
        if path.is_file():
            validate_text(path, root, errors)
            validate_resource_references(path, root, skills, errors)

    validate_duplicate_scripts(skill_root, errors)

    for path in [root / ".claude-plugin/plugin.json", root / ".claude-plugin/marketplace.json"]:
        try:
            json.loads(path.read_text(encoding="utf-8-sig"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append("{}: invalid JSON ({})".format(path, exc))

    showcase = root / "showcase/elife-tea-seq-figure-3"
    for name in ["figure3a-d-atlas-rerender.png", "figure3e-marker-heatmap-rerender.png", "reproduce_elife_63632_figure3_umaps.py"]:
        if not (showcase / name).is_file():
            errors.append("missing showcase asset: {}".format(name))

    if errors:
        print("Release check failed:")
        print("\n".join("- {}".format(error) for error in errors))
        return 1
    print("Release check passed for {} skills.".format(len(skills)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
