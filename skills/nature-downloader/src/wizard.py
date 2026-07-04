"""English text. 

7 English text, English text AI English text. 
English text prompt English text, English text. 

English text(AI English text): 
    from wizard import Wizard
    w = Wizard()
    # Step 1
    prompt = w.start()                # English text
    # English text
    result = w.handle_step1(user_input)
    # result = {"next": "step2"|"retry"|"done", "prompt": str, "data": dict}

English text: 
    w = Wizard()
    w.configure_from_preset("English text")  # English text
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional
from urllib.parse import parse_qs, urlparse

from config import save_config, backup_config, delete_config, CONFIG_FILE
from schools_loader import match_school, list_school_names
from validators import (
    KNOWN_DATABASES,
    validate_carsi_entry,
    validate_ezproxy_url,
    validate_libraries,
    validate_school_name,
    validate_sso_domain,
)


def infer_access_from_url(url: str) -> dict[str, Any]:
    """Infer the likely library access route from a user-provided resource URL."""
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
        "institution_hint": None,
        "notes": "",
    }

    if "metaersp" in host or "metaauth" in host:
        result.update(
            {
                "entry_type": "resource_portal",
                "auth_type": "cas",
                "sso_domain": "cas.whu.edu.cn" if host.startswith("whu.") else host,
                "institution_hint": host.split(".", 1)[0] if "." in host else None,
                "notes": "English text; English text, English text. ",
            }
        )
    elif "/authserver/login" in path or host.startswith("cas."):
        hint = None
        if service_host:
            service_parts = urlparse(service).path.strip("/").split("/")
            if len(service_parts) >= 2:
                hint = service_parts[1]
        result.update(
            {
                "entry_type": "cas_login",
                "auth_type": "cas",
                "sso_domain": host,
                "institution_hint": hint,
                "notes": "CAS English text; English text service English text, English text. ",
            }
        )
    elif "ezproxy" in host or "libproxy" in host:
        result.update({"entry_type": "ezproxy", "auth_type": "custom", "notes": "English text. "})
    elif "webvpn" in host or "vpn" in host:
        result.update({"entry_type": "webvpn", "auth_type": "custom", "notes": "WebVPN English text. "})
    elif "shibboleth" in path or "carsi" in host:
        result.update({"entry_type": "carsi", "auth_type": "sso", "notes": "CARSI/Shibboleth English text. "})

    return result


class Wizard:
    """English text. 

    English text: 
        step1 (English text) ->
            English text -> step4 (English text) -> step6 (English text) -> step7 (English text)
            English text -> step2 (CARSIEnglish text) -> step3 (SSOEnglish text) -> step4 -> step6 -> step7
                                                   English text step5 (EZproxy) -> step6 -> step7
    """

    def __init__(self) -> None:
        self.state: str = "step1"
        self.data: dict[str, Any] = {}
        self.matched_preset: Optional[dict[str, Any]] = None

    # ===== Step 1: English text =====
    def start(self) -> str:
        """English text. """
        self.state = "step1"
        return (
            "English text! English text. English text(English text). \n\n"
            "English text/English text. \n"
            "English text, English text, Web of Science English text, English text, "
            "English text. \n\n"
            "English text CAS/CARSI/EZproxy/WebVPN/English text; "
            "English text. "
        )

    def handle_step1(self, user_input: str) -> dict[str, Any]:
        """English text; English text URL English text. """
        value = user_input.strip()
        if not value:
            return {"next": "retry", "prompt": "English text, English text: "}

        if "://" in value or "." in value:
            inferred = infer_access_from_url(value)
            self.data.update(inferred)
            self.data["school_name"] = inferred.get("institution_hint") or inferred["entry_host"]
            self.data["source"] = "resource_url"
            self.data["auth_type"] = inferred["auth_type"]
            self.data["sso_domain"] = inferred["sso_domain"]
            self.data["carsi_entry"] = inferred["resource_entry"]
            self.data["libraries"] = ["Web of Science", "ScienceDirect", "Springer", "IEEE Xplore", "English text", "ACS"]
            self.data["notes"] = inferred.get("notes", "")
            self.data["discovery"] = {"resource_entry_url": inferred["resource_entry"]}
            if inferred["entry_type"] == "resource_portal":
                self.data["discovery"]["resource_portal_url"] = inferred["resource_entry"]
            if inferred.get("service_host"):
                self.data["discovery"]["auth_service_host"] = inferred["service_host"]

            self.state = "step4"
            return {
                "next": "step4",
                "prompt": (
                    "English text: \n"
                    f"  English text: {inferred['entry_type']}\n"
                    f"  English text: {inferred['auth_type']}\n"
                    f"  SSO English text: {inferred['sso_domain']}\n"
                    f"  English text: {inferred['resource_entry']}\n\n"
                    "English text? \n"
                    "  1. English text, English text\n"
                    "  2. English text\n"
                    "  3. English text/English text"
                ),
                "data": {"inferred": inferred},
            }

        name = value

        ok, msg = validate_school_name(name)
        if not ok:
            return {"next": "retry", "prompt": f"{msg}, English text: "}

        # English text
        preset = match_school(name)
        if preset:
            self.matched_preset = preset
            self.data["school_name"] = preset["name"]
            self.data["source"] = "preset"

            # English text
            auth = preset.get("auth", {})
            self.data["auth_type"] = auth.get("type", "cas")
            self.data["sso_domain"] = auth.get("sso_domain", "")
            self.data["carsi_entry"] = auth.get("carsi_entry", "")
            self.data["libraries"] = preset.get("libraries", [])
            self.data["notes"] = preset.get("notes", "")

            self.state = "step4"
            return {
                "next": "step4",
                "prompt": (
                    f"English text: {preset['name']}\n"
                    f"  English text: {auth.get('type', 'English text')}\n"
                    f"  SSO English text: {auth.get('sso_domain', 'English text')}\n"
                    f"  CARSI English text: {auth.get('carsi_entry', 'English text')}\n"
                    f"  English text: {', '.join(preset.get('libraries', []))}\n\n"
                    "English text? \n"
                    "  1. English text, English text\n"
                    "  2. English text\n"
                    "  3. English text, English text"
                ),
                "data": {"matched": preset["name"]},
            }

        # English text, English text
        self.data["school_name"] = name
        self.data["source"] = "manual"
        self.state = "step2"
        return {
            "next": "step2",
            "prompt": (
                f"English text「{name}」, English text. \n\n"
                "Step 2: English text/English text CARSI English text? \n"
                "(CARSI English text, English text: https://www.carsi.edu.cn/)\n\n"
                "  1. English text, English text CARSI\n"
                "  2. English text / English text, English text(EZproxy)\n"
                "  3. English text, English text VPN English text"
            ),
        }

    # ===== Step 2: CARSI English text =====
    def handle_step2(self, user_input: str) -> dict[str, Any]:
        """English text CARSI English text. """
        choice = user_input.strip()
        if choice == "1":
            self.data["use_carsi"] = True
            self.state = "step2b"
            return {
                "next": "step2b",
                "prompt": (
                    "English text CARSI English text URL. \n"
                    "(English text https://www.carsi.edu.cn/ English text, "
                    "English text https://xxx.edu.cn/idp/shibboleth English text)\n\n"
                    "English text, English text「English text」English text, English text. "
                ),
            }
        elif choice == "2":
            self.data["use_carsi"] = False
            self.state = "step3"
            return {
                "next": "step3",
                "prompt": (
                    "English text(EZproxy)English text. \n\n"
                    "Step 3: English text. \n"
                    "(English text id.xxx.edu.cn / cas.xxx.edu.cn / sso.xxx.edu.cn English text, "
                    "English text id.tsinghua.edu.cn)"
                ),
            }
        elif choice == "3":
            self.data["use_carsi"] = False
            self.data["use_vpn"] = True
            self.state = "step3"
            return {
                "next": "step3",
                "prompt": (
                    "English text, English text VPN English text. \n"
                    "English text VPN, English text. \n"
                    "(English text id.xxx.edu.cn / cas.xxx.edu.cn English text)"
                ),
            }
        return {"next": "retry", "prompt": "English text 1, 2 English text 3: "}

    # ===== Step 2b: CARSI English text URL =====
    def handle_step2b(self, user_input: str) -> dict[str, Any]:
        """English text CARSI English text URL English text. """
        url = user_input.strip()
        if url in ("English text", "skip", ""):
            self.data["carsi_entry"] = ""
            self.state = "step3"
            return {
                "next": "step3",
                "prompt": (
                    "English text CARSI English text(English text). \n\n"
                    "Step 3: English text. \n"
                    "(English text id.xxx.edu.cn / cas.xxx.edu.cn / sso.xxx.edu.cn English text)"
                ),
            }

        # English text
        ok, msg = validate_carsi_entry(url)
        if not ok:
            return {
                "next": "retry",
                "prompt": f"{msg}\n\nEnglish text CARSI English text URL, English text「English text」English text: ",
            }

        self.data["carsi_entry"] = url
        self.state = "step3"
        return {
            "next": "step3",
            "prompt": (
                f"CARSI English text. \n\n"
                "Step 3: English text. \n"
                "(English text id.xxx.edu.cn / cas.xxx.edu.cn / sso.xxx.edu.cn English text)"
            ),
        }

    # ===== Step 3: SSO English text =====
    def handle_step3(self, user_input: str) -> dict[str, Any]:
        """English text SSO English text. """
        domain = user_input.strip()
        if not domain:
            return {"next": "retry", "prompt": "English text, English text: "}

        ok, msg = validate_sso_domain(domain)
        if not ok:
            return {
                "next": "retry",
                "prompt": f"{msg}\n\nEnglish text SSO English text(English text id.xxx.edu.cn): ",
            }

        self.data["sso_domain"] = domain.split("://")[-1].split("/")[0]
        # English text auth_type, English text cas
        if "auth_type" not in self.data:
            self.data["auth_type"] = "cas"

        # English text EZproxy English text
        if not self.data.get("use_carsi", True) and not self.data.get("use_vpn"):
            self.state = "step5"
            return {
                "next": "step5",
                "prompt": (
                    f"SSO English text: {msg}\n\n"
                    "Step 5: English text EZproxy English text. \n"
                    "(English text: English text EZproxy English text「English text」English text)\n\n"
                    "English text, English text「English text」English text. "
                ),
            }

        self.state = "step4"
        return {
            "next": "step4",
            "prompt": (
                f"SSO English text: {msg}\n\n"
                "Step 4: English text? \n"
                f"English text: {', '.join(KNOWN_DATABASES[:10])} ...\n\n"
                "English text, English text: "
            ),
        }

    # ===== Step 4: English text =====
    def handle_step4(self, user_input: str) -> dict[str, Any]:
        """English text. """
        if user_input.strip() in ("English text", "1", "ok", "yes", "English text"):
            # English text
            if not self.data.get("libraries"):
                return {"next": "retry", "prompt": "English text: "}
        else:
            # English text
            libs = [s.strip() for s in user_input.replace(",", " ").split() if s.strip()]
            if libs:
                self.data["libraries"] = libs

        ok, msg = validate_libraries(self.data.get("libraries", []))
        if not ok:
            return {"next": "retry", "prompt": f"{msg}, English text: "}

        self.state = "step6"
        return {
            "next": "step6",
            "prompt": (
                f"English text {len(self.data['libraries'])} English text. \n\n"
                "Step 6: English text..."
            ),
        }

    # ===== Step 5: EZproxy English text =====
    def handle_step5(self, user_input: str) -> dict[str, Any]:
        """English text EZproxy English text. """
        url = user_input.strip()
        if url in ("English text", "skip", ""):
            self.data["ezproxy_url"] = None
            self.state = "step4"
            return {
                "next": "step4",
                "prompt": (
                    "English text EZproxy. \n\n"
                    "Step 4: English text? \n"
                    "English text, English text: "
                ),
            }

        ok, msg = validate_ezproxy_url(url)
        if not ok:
            return {
                "next": "retry",
                "prompt": f"{msg}\n\nEnglish text EZproxy English text, English text「English text」: ",
            }

        self.data["ezproxy_url"] = url
        self.state = "step4"
        return {
            "next": "step4",
            "prompt": (
                f"EZproxy English text: {msg}\n\n"
                "Step 4: English text? \n"
                "English text, English text: "
            ),
        }

    # ===== Step 6: English text =====
    def handle_step6(self, user_input: str = "") -> dict[str, Any]:
        """English text. """
        # English text
        from health_check import health_check, clear_cache

        # English text
        try:
            temp_config = self._build_config()
        except ValueError as e:
            return {"next": "retry", "prompt": f"English text: {e}"}

        # English text
        clear_cache()
        save_config(temp_config)
        result = health_check(force=True)

        self.state = "step7"
        details_text = "\n".join(f"  {d}" for d in result.get("details", []))
        if result["ok"]:
            return {
                "next": "step7",
                "prompt": (
                    f"English text: \n{details_text}\n\n"
                    "Step 7: English text? \n  1. English text\n  2. English text"
                ),
            }
        else:
            suggestions = "\n".join(f"  {s}" for s in result.get("suggestions", []))
            return {
                "next": "step7",
                "prompt": (
                    f"English text: \n{details_text}\n\n"
                    f"{suggestions}\n\n"
                    "Step 7: English text? \n"
                    "  1. English text(English text)\n"
                    "  2. English text"
                ),
                "data": {"warnings": result.get("details", [])},
            }

    # ===== Step 7: English text =====
    def handle_step7(self, user_input: str) -> dict[str, Any]:
        """English text. """
        choice = user_input.strip()
        if choice in ("2", "English text", "English text"):
            delete_config()
            self.__init__()
            return {"next": "step1", "prompt": self.start()}

        # English text
        try:
            config = self._build_config()
            # English text(English text)
            if self.data.get("warnings"):
                config["_warnings"] = self.data["warnings"]
            path = save_config(config)
            return {
                "next": "done",
                "prompt": (
                    f"English text「{self.data['school_name']}」English text! \n"
                    f"English text: {path}\n\n"
                    "English text. English text, English text「English text」English text「/reconfig」. "
                ),
                "data": {"school": self.data["school_name"], "path": str(path)},
            }
        except ValueError as e:
            return {"next": "retry", "prompt": f"English text: {e}\nEnglish text: "}

    # ===== English text =====
    def handle(self, user_input: str) -> dict[str, Any]:
        """English text. """
        handlers = {
            "step1": self.handle_step1,
            "step2": self.handle_step2,
            "step2b": self.handle_step2b,
            "step3": self.handle_step3,
            "step4": self.handle_step4,
            "step5": self.handle_step5,
            "step6": self.handle_step6,
            "step7": self.handle_step7,
        }
        handler = handlers.get(self.state)
        if handler is None:
            self.state = "step1"
            return {"next": "step1", "prompt": self.start()}
        return handler(user_input)

    # ===== English text: English text =====
    def configure_from_preset(self, school_name: str) -> dict[str, Any]:
        """English text(English text). 

        English text, English text ValueError. 
        """
        preset = match_school(school_name)
        if not preset:
            raise ValueError(f"English text「{school_name}」")

        auth = preset.get("auth", {})
        config = {
            "version": 1,
            "school": {
                "name": preset["name"],
                "code": preset.get("aliases", [""])[0] if preset.get("aliases") else None,
                "configured_at": datetime.now().isoformat(),
                "source": "preset",
            },
            "auth": {
                "type": auth.get("type", "cas"),
                "sso_domain": auth.get("sso_domain", ""),
                "carsi_entry": auth.get("carsi_entry") or None,
                "carsi_sp_entity_id": None,
            },
            "proxy": {
                "type": None,
                "ezproxy_url": None,
            },
            "libraries": preset.get("libraries", []),
            "discovery": preset.get("discovery", {}),
            "notes": preset.get("notes", ""),
        }

        path = save_config(config)
        return {"config": config, "path": str(path)}

    # ===== English text: English text =====
    def configure_from_resource_url(self, resource_url: str) -> dict[str, Any]:
        """Configure from a library resource portal or authentication URL."""
        inferred = infer_access_from_url(resource_url)
        self.data.update(inferred)
        self.data["school_name"] = inferred.get("institution_hint") or inferred["entry_host"]
        self.data["source"] = "resource_url"
        self.data["auth_type"] = inferred["auth_type"]
        self.data["sso_domain"] = inferred["sso_domain"]
        self.data["carsi_entry"] = inferred["resource_entry"]
        self.data["libraries"] = ["Web of Science", "ScienceDirect", "Springer", "IEEE Xplore", "English text", "ACS"]
        self.data["notes"] = inferred.get("notes", "")
        self.data["discovery"] = {"resource_entry_url": inferred["resource_entry"]}
        if inferred["entry_type"] == "resource_portal":
            self.data["discovery"]["resource_portal_url"] = inferred["resource_entry"]
        if inferred.get("service_host"):
            self.data["discovery"]["auth_service_host"] = inferred["service_host"]

        config = self._build_config()
        path = save_config(config)
        return {"config": config, "path": str(path), "inferred": inferred}

    # ===== English text: English text =====
    def _build_config(self) -> dict[str, Any]:
        """English text. """
        if not self.data.get("school_name"):
            raise ValueError("English text")
        if not self.data.get("sso_domain"):
            raise ValueError("SSO English text")
        if not self.data.get("libraries"):
            raise ValueError("English text")

        return {
            "version": 1,
            "school": {
                "name": self.data["school_name"],
                "code": None,
                "configured_at": datetime.now().isoformat(),
                "source": self.data.get("source", "manual"),
            },
            "auth": {
                "type": self.data.get("auth_type", "cas"),
                "sso_domain": self.data["sso_domain"],
                "carsi_entry": self.data.get("carsi_entry") or None,
                "carsi_sp_entity_id": None,
            },
            "proxy": {
                "type": "ezproxy" if self.data.get("ezproxy_url") else None,
                "ezproxy_url": self.data.get("ezproxy_url") or None,
            },
            "libraries": self.data["libraries"],
            "discovery": self.data.get("discovery", {}),
            "notes": self.data.get("notes", ""),
        }


if __name__ == "__main__":
    # English text
    w = Wizard()
    try:
        result = w.configure_from_preset("English text")
        print(f"English text: {result['config']['school']['name']}")
        print(f"English text: {result['path']}")
    except ValueError as e:
        print(f"English text: {e}")
        print(f"English text: {CONFIG_FILE}")
