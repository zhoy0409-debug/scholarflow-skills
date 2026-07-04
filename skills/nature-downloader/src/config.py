"""English text. 

English text school.json English text, English text, English text, English text. 
English text: ~/.config/lit-dl/school.json
"""

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

# English text(English text, English text profile)
CONFIG_DIR = Path(os.environ.get("LIT_DL_CONFIG_DIR", Path.home() / ".config" / "lit-dl"))
CONFIG_FILE = CONFIG_DIR / "school.json"

# schema English text(English text)
SCHEMA_FILE = Path(__file__).resolve().parent.parent / "data" / "school.schema.json"


def load_schema() -> dict[str, Any]:
    """English text JSON Schema. """
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def config_exists() -> bool:
    """English text. """
    return CONFIG_FILE.exists()


def validate(config: dict[str, Any]) -> list[str]:
    """English text schema. 

    English text, English text. 
    English text jsonschema English text schema English text, English text. 
    """
    errors: list[str] = []

    # English text(English text jsonschema)
    if not isinstance(config, dict):
        return ["English text JSON English text"]
    if "version" not in config:
        errors.append("English text version English text")
    if "school" not in config or "name" not in config.get("school", {}):
        errors.append("English text school.name English text")
    auth = config.get("auth", {})
    if "type" not in auth:
        errors.append("English text auth.type English text")
    if "sso_domain" not in auth or not auth["sso_domain"]:
        errors.append("English text auth.sso_domain English text")
    if not config.get("libraries"):
        errors.append("libraries English text")

    # schema English text(English text)
    if jsonschema is not None and not errors:
        try:
            jsonschema.validate(instance=config, schema=load_schema())
        except jsonschema.ValidationError as e:  # type: ignore
            errors.append(f"schema English text: {e.message}")

    return errors


def load_config() -> Optional[dict[str, Any]]:
    """English text. 

    English text, English text None. 
    English text JSON English text, English text None. 
    """
    if not CONFIG_FILE.exists():
        return None

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        # English text, English text None
        backup = CONFIG_FILE.with_suffix(".json.broken")
        shutil.copy2(CONFIG_FILE, backup)
        try:
            CONFIG_FILE.unlink()
        except OSError:
            pass
        print(f"English text, English text {backup}, English text. English text: {e}")
        return None


def save_config(config: dict[str, Any]) -> Path:
    """English text. 

    English text, English text configured_at English text. 
    English text. 
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    # English text
    if not config.get("school", {}).get("configured_at"):
        config.setdefault("school", {})["configured_at"] = datetime.now().isoformat()

    # English text
    errors = validate(config)
    if errors:
        raise ValueError(f"English text: {'; '.join(errors)}")

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

    # English text(English text)
    os.chmod(CONFIG_FILE, 0o600)

    return CONFIG_FILE


def backup_config() -> Optional[Path]:
    """English text, English text. English text None. """
    if not CONFIG_FILE.exists():
        return None
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup = CONFIG_FILE.with_suffix(f".json.{timestamp}.bak")
    shutil.copy2(CONFIG_FILE, backup)
    return backup


def delete_config() -> bool:
    """English text(English text). English text. """
    if CONFIG_FILE.exists():
        backup_config()
        CONFIG_FILE.unlink()
        return True
    return False


def get_school_name() -> Optional[str]:
    """English text. English text None. """
    cfg = load_config()
    if cfg is None:
        return None
    return cfg.get("school", {}).get("name")


def get_auth_info() -> Optional[dict[str, Any]]:
    """English text. English text None. """
    cfg = load_config()
    if cfg is None:
        return None
    return cfg.get("auth")


if __name__ == "__main__":
    # CLI English text
    if config_exists():
        cfg = load_config()
        if cfg:
            print(f"English text: {cfg.get('school', {}).get('name', 'English text')}")
            print(f"English text: {CONFIG_FILE}")
            errors = validate(cfg)
            if errors:
                print(f"English text: {errors}")
            else:
                print("English text")
        else:
            print("English text, English text")
    else:
        print(f"English text, English text: {CONFIG_FILE}")
