"""English text. 

English text, English text 10 English text. 
English text. 
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Optional

from config import CONFIG_DIR, load_config
from validators import validate_carsi_entry, validate_sso_domain

# English text
CACHE_FILE = CONFIG_DIR / "health_cache.json"
CACHE_TTL = 600  # 10 English text


def _load_cache() -> Optional[dict[str, Any]]:
    if not CACHE_FILE.exists():
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return None


def _save_cache(data: dict[str, Any]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _clear_cache() -> None:
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()


def _diagnose_failure(cfg: dict[str, Any]) -> list[str]:
    """English text. """
    suggestions: list[str] = []
    auth = cfg.get("auth", {})
    sso_domain = auth.get("sso_domain", "")
    carsi_entry = auth.get("carsi_entry", "")

    suggestions.append("English text: ")

    if sso_domain:
        suggestions.append(
            f"1. English text: English text VPN? "
            f"English text {sso_domain} English text VPN. "
        )
    if carsi_entry:
        suggestions.append(
            f"2. CARSI English text: English text https://www.carsi.edu.cn/ "
            f"English text, English text「English text」English text. "
        )
    suggestions.append("3. English text, English text. ")
    suggestions.append("4. English text, English text「English text」English text. ")

    return suggestions


def health_check(force: bool = False) -> dict[str, Any]:
    """English text. 

    English text: 
        force: English text

    English text: 
        {
            "ok": bool,
            "checked_at": str,
            "cached": bool,
            "details": [...],
            "suggestions": [...]  # English text
        }
    """
    # English text
    if not force:
        cache = _load_cache()
        if cache and (time.time() - cache.get("checked_at_ts", 0)) < CACHE_TTL:
            cache["cached"] = True
            return cache

    cfg = load_config()
    if cfg is None:
        return {
            "ok": False,
            "checked_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "cached": False,
            "details": ["English text, English text"],
            "suggestions": ["English text「English text」English text「/reconfig」English text"],
        }

    details: list[str] = []
    all_ok = True

    auth = cfg.get("auth", {})
    sso_domain = auth.get("sso_domain", "")
    carsi_entry = auth.get("carsi_entry", "")

    # 1. SSO English text
    if sso_domain:
        ok, msg = validate_sso_domain(sso_domain)
        details.append(f"[SSO] {msg}")
        if not ok:
            all_ok = False
    else:
        details.append("[SSO] English text sso_domain")
        all_ok = False

    # 2. CARSI English text(English text)
    if carsi_entry:
        ok, msg = validate_carsi_entry(carsi_entry)
        details.append(f"[CARSI] {msg}")
        if not ok:
            all_ok = False
    else:
        details.append("[CARSI] English text CARSI English text(English text CARSI English text)")

    result: dict[str, Any] = {
        "ok": all_ok,
        "checked_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "checked_at_ts": time.time(),
        "cached": False,
        "details": details,
    }

    if not all_ok:
        result["suggestions"] = _diagnose_failure(cfg)

    # English text
    _save_cache(result)

    return result


def clear_cache() -> None:
    """English text(English text). """
    _clear_cache()


if __name__ == "__main__":
    result = health_check(force=True)
    print(f"English text: {'English text' if result['ok'] else 'English text'}")
    print(f"English text: {result['checked_at']}")
    for d in result.get("details", []):
        print(f"  {d}")
    for s in result.get("suggestions", []):
        print(f"  {s}")
