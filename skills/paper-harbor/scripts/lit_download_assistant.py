#!/usr/bin/env python3
"""Parse a natural-language literature download request into a runnable plan."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ALIASES = {
    "science direct": "sciencedirect",
    "sciencedirect": "sciencedirect",
    "elsevier": "sciencedirect",
    "cnki": "cnki",
    "web of science": "wos",
    "wos": "wos",
    "pubmed": "pubmed",
}


def normalize_site(value: str | None) -> str | None:
    if not value:
        return None
    key = value.strip().lower()
    return ALIASES.get(key, key)


def parse_prompt(prompt: str) -> dict[str, Any]:
    text = prompt.strip()
    compact = text.lower().replace(" ", "")
    result: dict[str, Any] = {}
    for alias, site in ALIASES.items():
        if alias.replace(" ", "") in compact:
            result["site"] = site
            break
    quoted = re.findall(r'["“](.+?)["”]', text)
    if quoted:
        for item in quoted:
            value = item.strip()
            if normalize_site(value) in set(ALIASES.values()):
                continue
            if re.search(r"[\\/]|^[A-Za-z]:", value):
                continue
            result["keywords"] = value
            break
    if "keywords" not in result:
        match = re.search(r"(?:keywords?|query|topic)\s*[:=]\s*([^,;\n]+)", text, re.I)
        if match:
            result["keywords"] = match.group(1).strip()
    year_match = re.search(r"(20\d{2}|19\d{2})\s*[-to]+\s*(20\d{2}|19\d{2})", text, re.I)
    if year_match:
        result["year_from"], result["year_to"] = year_match.group(1), year_match.group(2)
    else:
        years = re.findall(r"\b(20\d{2}|19\d{2})\b", text)
        if years:
            result["year_from"] = min(years)
            result["year_to"] = max(years)
    if_match = re.search(r"\bIF\s*[>=:]*\s*(\d+(?:\.\d+)?)", text, re.I)
    if if_match:
        result["if_min"] = float(if_match.group(1))
    max_match = re.search(r"\b(?:top|max|limit)\s*(\d{1,3})\b", text, re.I)
    if max_match:
        result["max_records"] = int(max_match.group(1))
    result.setdefault("site", "sciencedirect")
    result.setdefault("keywords", text if text else "")
    result.setdefault("year_from", "")
    result.setdefault("year_to", "")
    result.setdefault("max_records", 50)
    return result


def build_plan(parsed: dict[str, Any]) -> dict[str, Any]:
    site = parsed["site"]
    if site == "sciencedirect":
        command = [
            "python",
            "sciencedirect_drission_run.py",
            parsed["keywords"],
            "--year-from",
            parsed.get("year_from", ""),
            "--year-to",
            parsed.get("year_to", ""),
            "--max-records",
            str(parsed.get("max_records", 50)),
        ]
        if parsed.get("if_min") is not None:
            command.extend(["--if-min", str(parsed["if_min"])])
    elif site == "cnki":
        command = ["python", "cnki_drission_run.py", parsed["keywords"]]
    else:
        command = ["manual", site, parsed["keywords"]]
    return {
        "site": site,
        "keywords": parsed["keywords"],
        "filters": {
            "year_from": parsed.get("year_from", ""),
            "year_to": parsed.get("year_to", ""),
            "if_min": parsed.get("if_min"),
            "max_records": parsed.get("max_records", 50),
        },
        "command": command,
        "checks": [
            "Confirm institutional access before downloading.",
            "Review copyright and publisher terms.",
            "Verify metadata before importing into Zotero or a reference manager.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", nargs="*", help="Natural-language request.")
    parser.add_argument("--prompt-file", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    prompt = " ".join(args.prompt)
    if args.prompt_file:
        prompt = args.prompt_file.read_text(encoding="utf-8")
    plan = build_plan(parse_prompt(prompt))
    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print("# Literature Download Plan\n")
        print(f"- Site: {plan['site']}")
        print(f"- Keywords: {plan['keywords']}")
        print(f"- Command: {' '.join(plan['command'])}")
        print("\n## Checks")
        for item in plan["checks"]:
            print(f"- {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
