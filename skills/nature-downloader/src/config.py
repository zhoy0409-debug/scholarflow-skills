"""Read, validate, save, and remove literature-download school configuration."""

from __future__ import annotations

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

try:
    import jsonschema  # type: ignore
except ImportError:
    jsonschema = None  # type: ignore


CONFIG_DIR = Path(os.environ.get("LIT_DL_CONFIG_DIR", Path.home() / ".config" / "lit-dl"))
CONFIG_FILE = CONFIG_DIR / "school.json"
SCHEMA_FILE = Path(__file__).resolve().parent.parent / "data" / "school.schema.json"


def load_schema() -> dict[str, Any]:
    """Load the bundled JSON schema."""
    with open(SCHEMA_FILE, "r", encoding="utf-8") as handle:
        return json.load(handle)


def config_exists() -> bool:
    """Return True when a school configuration has already been saved."""
    return CONFIG_FILE.exists()


def _access(config: dict[str, Any]) -> dict[str, Any]:
    return config.get("access") or config.get("auth") or {}


def validate(config: dict[str, Any]) -> list[str]:
    """Return configuration validation errors without raising."""
    errors: list[str] = []
    if not isinstance(config, dict):
        return ["configuration must be a JSON object"]
    if "version" not in config:
        errors.append("missing version")
    school = config.get("school", {})
    if not isinstance(school, dict) or not school.get("name"):
        errors.append("missing school.name")
    access = _access(config)
    if not isinstance(access, dict) or not access.get("type"):
        errors.append("missing access.type")
    if not config.get("libraries"):
        errors.append("libraries must contain at least one database or publisher platform")
    if jsonschema is not None and not errors:
        try:
            jsonschema.validate(instance=config, schema=load_schema())
        except jsonschema.ValidationError as exc:  # type: ignore[attr-defined]
            errors.append(f"schema validation failed: {exc.message}")
    return errors


def load_config() -> Optional[dict[str, Any]]:
    """Load configuration. Return None if the file is missing or unreadable."""
    if not CONFIG_FILE.exists():
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        backup = CONFIG_FILE.with_suffix(".json.broken")
        shutil.copy2(CONFIG_FILE, backup)
        try:
            CONFIG_FILE.unlink()
        except OSError:
            pass
        print(f"Configuration was unreadable and has been backed up to {backup}: {exc}")
        return None


def save_config(config: dict[str, Any]) -> Path:
    """Validate and save configuration with private file permissions."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    config.setdefault("version", 1)
    config.setdefault("school", {})
    config["school"].setdefault("configured_at", datetime.now().isoformat(timespec="seconds"))
    errors = validate(config)
    if errors:
        raise ValueError("; ".join(errors))
    with open(CONFIG_FILE, "w", encoding="utf-8") as handle:
        json.dump(config, handle, ensure_ascii=False, indent=2)
        handle.write("\n")
    try:
        os.chmod(CONFIG_FILE, 0o600)
    except OSError:
        pass
    return CONFIG_FILE


def backup_config() -> Optional[Path]:
    """Create a timestamped backup and return its path."""
    if not CONFIG_FILE.exists():
        return None
    backup = CONFIG_FILE.with_suffix(f".json.{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak")
    shutil.copy2(CONFIG_FILE, backup)
    return backup


def delete_config() -> bool:
    """Back up and remove the current configuration."""
    if not CONFIG_FILE.exists():
        return False
    backup_config()
    CONFIG_FILE.unlink()
    return True


def get_school_name() -> Optional[str]:
    cfg = load_config()
    return None if cfg is None else cfg.get("school", {}).get("name")


def get_auth_info() -> Optional[dict[str, Any]]:
    cfg = load_config()
    return None if cfg is None else _access(cfg)


if __name__ == "__main__":
    if not config_exists():
        print(f"No configuration found. Expected path: {CONFIG_FILE}")
        raise SystemExit(1)
    cfg = load_config()
    if cfg is None:
        print("Configuration could not be loaded.")
        raise SystemExit(1)
    errors = validate(cfg)
    print(f"School: {cfg.get('school', {}).get('name', 'unknown')}")
    print(f"Path: {CONFIG_FILE}")
    print("Status: valid" if not errors else f"Status: invalid ({'; '.join(errors)})")
