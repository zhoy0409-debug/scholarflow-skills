"""Health checks for school-access configuration."""

from __future__ import annotations

import json
import time
from typing import Any, Optional

from config import CONFIG_DIR, get_auth_info, load_config
from validators import validate_carsi_entry, validate_sso_domain


CACHE_FILE = CONFIG_DIR / "health_cache.json"
CACHE_TTL = 600


def _load_cache() -> Optional[dict[str, Any]]:
    if not CACHE_FILE.exists():
        return None
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, OSError):
        return None


def _save_cache(data: dict[str, Any]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def _diagnose_failure(cfg: dict[str, Any]) -> list[str]:
    access = cfg.get("access") or cfg.get("auth") or {}
    suggestions = ["Check the access route before running batch retrieval."]
    if access.get("sso_domain"):
        suggestions.append(f"Open the SSO domain in a browser and confirm VPN or campus-network requirements: {access['sso_domain']}")
    if access.get("carsi_entry"):
        suggestions.append("Open the CARSI entry page manually and confirm that the institution can be selected.")
    suggestions.append("If the institution recently changed authentication, regenerate the configuration from the official library portal.")
    return suggestions


def health_check(force: bool = False) -> dict[str, Any]:
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
            "checked_at_ts": time.time(),
            "cached": False,
            "details": ["No school configuration found."],
            "suggestions": ["Run configure_school.py preset <school> or configure_school.py url <library-url>."],
        }
    access = get_auth_info() or {}
    details: list[str] = []
    all_ok = True
    if access.get("sso_domain"):
        ok, message = validate_sso_domain(access["sso_domain"])
        details.append(f"[SSO] {message}")
        all_ok = all_ok and ok
    else:
        details.append("[SSO] No SSO domain configured.")
        all_ok = False
    if access.get("carsi_entry"):
        ok, message = validate_carsi_entry(access["carsi_entry"])
        details.append(f"[CARSI] {message}")
        all_ok = all_ok and ok
    else:
        details.append("[CARSI] No CARSI entry configured; this is acceptable for EZproxy or custom access routes.")
    result: dict[str, Any] = {
        "ok": all_ok,
        "checked_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "checked_at_ts": time.time(),
        "cached": False,
        "details": details,
    }
    if not all_ok:
        result["suggestions"] = _diagnose_failure(cfg)
    _save_cache(result)
    return result


def clear_cache() -> None:
    if CACHE_FILE.exists():
        CACHE_FILE.unlink()


if __name__ == "__main__":
    result = health_check(force=True)
    print(f"Status: {'OK' if result['ok'] else 'CHECK REQUIRED'}")
    print(f"Checked at: {result['checked_at']}")
    for detail in result.get("details", []):
        print(f"  {detail}")
    for suggestion in result.get("suggestions", []):
        print(f"  {suggestion}")
