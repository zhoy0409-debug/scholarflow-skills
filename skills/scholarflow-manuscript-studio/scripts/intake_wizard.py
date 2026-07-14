#!/usr/bin/env python3
"""Create a ScholarFlow Manuscript Studio configuration from a guided terminal intake."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path


WORKFLOWS = ("rewrite_existing", "build_from_materials")
SCENES = ("journal", "conference", "report_review", "competition")
TIERS = ("flash", "pro")
LANGUAGES = ("en", "zh")
WORD_OUTPUTS = ("none", "docx")
REFERENCE_MODES = ("local_first", "specified_paths", "web")
HUMANIZE_TIERS = ("none", "light", "medium", "heavy")


@dataclass
class ManuscriptStudioConfig:
    workflow: str = "rewrite_existing"
    scene: str = "journal"
    tier: str = "flash"
    output_language: str = "en"
    word_output: str = "docx"
    target_name: str = ""
    draft_path: str = ""
    materials_dir: str = ""
    user_motivation: str = ""
    official_urls: list[str] | None = None
    reference_mode: str = "local_first"
    reference_paths: list[str] | None = None
    citation_target_count: int = 30
    special_requirements: str = ""
    detection_platform: str = "general"
    humanize_tier: str = "medium"


def choose(label: str, options: tuple[str, ...], default: str) -> str:
    print(f"\n{label}")
    for idx, option in enumerate(options, start=1):
        marker = " (default)" if option == default else ""
        print(f"  {idx}. {option}{marker}")
    raw = input("> ").strip()
    if not raw:
        return default
    if raw.isdigit() and 1 <= int(raw) <= len(options):
        return options[int(raw) - 1]
    return raw if raw in options else default


def ask(label: str, default: str = "") -> str:
    suffix = f" [{default}]" if default else ""
    value = input(f"{label}{suffix}: ").strip()
    return value or default


def split_list(value: str) -> list[str]:
    return [part.strip() for part in value.replace("\n", ";").split(";") if part.strip()]


def build_config() -> ManuscriptStudioConfig:
    print("ScholarFlow Manuscript Studio Intake")
    print("Answer only what you know. You can refine the configuration later.")
    config = ManuscriptStudioConfig()
    config.workflow = choose("Workflow", WORKFLOWS, config.workflow)
    config.scene = choose("Target scene", SCENES, config.scene)
    config.tier = choose("Research depth", TIERS, config.tier)
    config.output_language = choose("Final output language", LANGUAGES, config.output_language)
    config.word_output = choose("Word output", WORD_OUTPUTS, config.word_output)
    config.target_name = ask("Target journal, conference, report name, or project title")
    config.draft_path = ask("Existing draft path")
    config.materials_dir = ask("Materials folder")
    config.user_motivation = ask("What do you want this manuscript to achieve?")
    config.official_urls = split_list(ask("Official URLs, separated by semicolons"))
    config.reference_mode = choose("Reference mode", REFERENCE_MODES, config.reference_mode)
    config.reference_paths = split_list(ask("Local reference paths, separated by semicolons"))
    citation_raw = ask("Target citation count", str(config.citation_target_count))
    try:
        config.citation_target_count = int(citation_raw)
    except ValueError:
        pass
    config.special_requirements = ask("Special requirements")
    config.humanize_tier = choose("Humanization level", HUMANIZE_TIERS, config.humanize_tier)
    return config


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path("scholarflow_manuscript_config.json"))
    parser.add_argument("--non-interactive", action="store_true")
    args = parser.parse_args()
    config = ManuscriptStudioConfig() if args.non_interactive else build_config()
    data = asdict(config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote configuration: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
