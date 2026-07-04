"""Guided school-access configuration helper for literature downloads."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from urllib.parse import parse_qs, urlparse

from config import CONFIG_FILE, backup_config, save_config
from schools_loader import list_school_names, match_school
from validators import KNOWN_DATABASES, validate_libraries, validate_school_name


def infer_access_from_url(url: str) -> dict[str, Any]:
    raw_url = url.strip()
    parsed = urlparse(raw_url if "://" in raw_url else f"https://{raw_url}")
    host = parsed.netloc.lower()
    path = parsed.path.lower()
    query = parse_qs(parsed.query)
    service = query.get("service", [""])[0]
    service_host = urlparse(service).netloc.lower() if service else ""
    result: dict[str, Any] = {
        "resource_entry": raw_url,
        "entry_host": host,
        "entry_type": "resource_entry",
        "auth_type": "custom",
        "sso_domain": host,
        "service_host": service_host or None,
        "institution_hint": host.split(".", 1)[0] if "." in host else None,
        "notes": "Resource URL supplied by the user.",
    }
    if "metaersp" in host or "metaauth" in host:
        result.update({"entry_type": "resource_portal", "auth_type": "cas", "notes": "Institutional resource portal detected."})
    elif "/authserver/login" in path or host.startswith("cas."):
        result.update({"entry_type": "cas_login", "auth_type": "cas", "sso_domain": host, "notes": "CAS login endpoint detected."})
    elif "ezproxy" in host or "libproxy" in host:
        result.update({"entry_type": "ezproxy", "auth_type": "custom", "notes": "EZproxy-style access route detected."})
    elif "webvpn" in host or "vpn" in host:
        result.update({"entry_type": "webvpn", "auth_type": "custom", "notes": "WebVPN-style access route detected."})
    elif "shibboleth" in path or "carsi" in host:
        result.update({"entry_type": "carsi", "auth_type": "sso", "notes": "CARSI/Shibboleth access route detected."})
    return result


class Wizard:
    """Step-based school access setup flow."""

    def __init__(self) -> None:
        self.state = "step1"
        self.data: dict[str, Any] = {}
        self.matched_preset: Optional[dict[str, Any]] = None

    def start(self) -> str:
        self.state = "step1"
        return (
            "School access setup\n\n"
            "Enter your institution name or paste a library/database access URL. "
            "The wizard will infer the likely access route and create a reusable configuration."
        )

    def handle_step1(self, user_input: str) -> dict[str, Any]:
        value = user_input.strip()
        if not value:
            return {"next": "retry", "prompt": "Please enter an institution name or access URL."}
        if "://" in value or "." in value:
            inferred = infer_access_from_url(value)
            self.data.update(inferred)
            self.data["school_name"] = inferred.get("institution_hint") or inferred["entry_host"]
            self.data["libraries"] = ["Web of Science", "ScienceDirect", "SpringerLink", "IEEE Xplore", "Scopus", "ACS"]
            self.state = "step4"
            return {"next": "step4", "prompt": self._review_prompt(), "data": {"inferred": inferred}}
        ok, message = validate_school_name(value)
        if not ok:
            return {"next": "retry", "prompt": message}
        preset = match_school(value)
        if preset:
            self.matched_preset = preset
            self.data.update(
                {
                    "school_name": preset["name"],
                    "source": "preset",
                    "auth_type": preset.get("auth", {}).get("type", "cas"),
                    "sso_domain": preset.get("auth", {}).get("sso_domain", ""),
                    "carsi_entry": preset.get("auth", {}).get("carsi_entry", ""),
                    "libraries": preset.get("libraries", []),
                    "notes": preset.get("notes", ""),
                }
            )
            self.state = "step4"
            return {"next": "step4", "prompt": self._review_prompt(), "data": {"matched": preset["name"]}}
        self.data.update({"school_name": value, "source": "manual", "auth_type": "custom", "libraries": []})
        self.state = "step4"
        return {"next": "step4", "prompt": self._review_prompt()}

    def handle_step2(self, user_input: str) -> dict[str, Any]:
        self.data["use_carsi"] = user_input.strip() == "1"
        self.state = "step4"
        return {"next": "step4", "prompt": self._review_prompt()}

    def handle_step3(self, user_input: str) -> dict[str, Any]:
        self.data["sso_domain"] = user_input.strip()
        self.state = "step4"
        return {"next": "step4", "prompt": self._review_prompt()}

    def handle_step4(self, user_input: str) -> dict[str, Any]:
        value = user_input.strip()
        if value:
            libraries = [item.strip() for item in value.split(",") if item.strip()]
            ok, message = validate_libraries(libraries)
            if not ok:
                return {"next": "retry", "prompt": message}
            self.data["libraries"] = libraries
        self.state = "step6"
        return {"next": "step6", "prompt": "Add any notes for this institution, or press Enter to continue."}

    def handle_step5(self, user_input: str) -> dict[str, Any]:
        self.data["ezproxy_url"] = user_input.strip()
        self.state = "step6"
        return {"next": "step6", "prompt": "Add any notes for this institution, or press Enter to continue."}

    def handle_step6(self, user_input: str) -> dict[str, Any]:
        if user_input.strip():
            self.data["notes"] = user_input.strip()
        self.state = "step7"
        return {"next": "step7", "prompt": self._review_prompt()}

    def handle_step7(self, user_input: str) -> dict[str, Any]:
        if user_input.strip().lower() in {"y", "yes", "save", ""}:
            return self.save()
        return {"next": "retry", "prompt": "Type yes to save, or revise the setup before saving."}

    def _review_prompt(self) -> str:
        return (
            "Review the inferred setup:\n"
            f"  Institution: {self.data.get('school_name', '')}\n"
            f"  Auth type: {self.data.get('auth_type', '')}\n"
            f"  SSO domain: {self.data.get('sso_domain', '')}\n"
            f"  Libraries: {', '.join(self.data.get('libraries', [])) or 'not set'}\n\n"
            "Enter a comma-separated library list to update it, or press Enter to continue."
        )

    def build_config(self) -> dict[str, Any]:
        return {
            "version": 1,
            "updated_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "school": {
                "name": self.data.get("school_name", ""),
                "source": self.data.get("source", "manual"),
                "notes": self.data.get("notes", ""),
            },
            "access": {
                "type": self.data.get("auth_type", "custom"),
                "sso_domain": self.data.get("sso_domain", ""),
                "carsi_entry": self.data.get("carsi_entry", self.data.get("resource_entry", "")),
                "ezproxy_url": self.data.get("ezproxy_url", ""),
            },
            "libraries": self.data.get("libraries") or list(KNOWN_DATABASES[:4]),
            "discovery": self.data.get("discovery", {}),
        }

    def save(self) -> dict[str, Any]:
        config = self.build_config()
        backup_config()
        save_config(config)
        return {"next": "done", "prompt": f"Configuration saved to {CONFIG_FILE}", "config": config, "path": str(CONFIG_FILE)}

    def configure_from_preset(self, school: str) -> dict[str, Any]:
        result = self.handle_step1(school)
        if result.get("next") == "retry":
            raise ValueError(result["prompt"])
        return self.save()

    def configure_from_resource_url(self, url: str) -> dict[str, Any]:
        inferred = infer_access_from_url(url)
        self.data.update(inferred)
        self.data["school_name"] = inferred.get("institution_hint") or inferred["entry_host"]
        self.data["libraries"] = ["Web of Science", "ScienceDirect", "SpringerLink", "IEEE Xplore", "Scopus", "ACS"]
        saved = self.save()
        saved["inferred"] = inferred
        return saved


def available_presets() -> list[str]:
    return list_school_names()
