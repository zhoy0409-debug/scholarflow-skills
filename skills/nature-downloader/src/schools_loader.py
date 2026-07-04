"""Load and match bundled institution presets."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Optional

try:
    import yaml  # type: ignore
except ImportError:
    yaml = None  # type: ignore


SCHOOLS_FILE = Path(__file__).resolve().parent.parent / "data" / "schools.yaml"


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in ("", "null", "None"):
        return None
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        return [] if not inner else [part.strip().strip("\"'") for part in inner.split(",")]
    return value.strip("\"'")


def _load_schools_without_yaml(text: str) -> list[dict[str, Any]]:
    schools: list[dict[str, Any]] = []
    current: Optional[dict[str, Any]] = None
    section: Optional[str] = None
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#") or stripped in {"schools:", "version: 1"}:
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        if stripped.startswith("- name:"):
            if current:
                schools.append(current)
            current = {"name": _parse_scalar(stripped.split(":", 1)[1]), "auth": {}}
            section = None
            continue
        if current is None or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        if indent == 4 and value.strip() == "":
            section = key.strip()
            current.setdefault(section, {})
        elif section and indent >= 6:
            current.setdefault(section, {})[key.strip()] = _parse_scalar(value)
        else:
            section = None
            current[key.strip()] = _parse_scalar(value)
    if current:
        schools.append(current)
    return schools


def load_schools() -> list[dict[str, Any]]:
    if not SCHOOLS_FILE.exists():
        return []
    text = SCHOOLS_FILE.read_text(encoding="utf-8")
    if yaml is None:
        return _load_schools_without_yaml(text)
    data = yaml.safe_load(text)
    return data.get("schools", []) if isinstance(data, dict) else []


def match_school(query: str) -> Optional[dict[str, Any]]:
    query = query.strip().lower()
    if not query:
        return None
    schools = load_schools()
    for school in schools:
        if school.get("name", "").lower() == query:
            return school
    for school in schools:
        for alias in school.get("aliases", []) or []:
            if str(alias).lower() == query:
                return school
    for school in schools:
        if query in school.get("name", "").lower():
            return school
    for school in schools:
        for alias in school.get("aliases", []) or []:
            if query in str(alias).lower():
                return school
    return None


def list_school_names() -> list[str]:
    return [school["name"] for school in load_schools() if school.get("name")]


if __name__ == "__main__":
    schools = load_schools()
    print(f"Loaded {len(schools)} school presets")
    for school in schools[:8]:
        print(f"  - {school['name']} ({', '.join(school.get('aliases', []))})")
    if len(schools) > 8:
        print(f"  ... and {len(schools) - 8} more")
