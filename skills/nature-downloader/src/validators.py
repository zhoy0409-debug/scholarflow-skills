"""English text. 

English text: 
- sso_domain: DNS English text + TCP 443 + HTTPS English text
- carsi_entry: HTTP GET English text
- ezproxy_url: HTTP GET English text

English text (ok: bool, message: str). 
"""

from __future__ import annotations

import socket
import ssl
import urllib.parse
import urllib.request


def validate_sso_domain(domain: str, timeout: float = 5.0) -> tuple[bool, str]:
    """English text SSO English text: DNS English text + TCP 443 + HTTPS English text. 

    English text (English text, English text). 
    """
    domain = domain.strip().lower()
    if not domain:
        return False, "English text"

    # English text
    for prefix in ("https://", "http://"):
        if domain.startswith(prefix):
            domain = domain[len(prefix):]
    domain = domain.split("/")[0]

    # DNS English text
    try:
        addrs = socket.getaddrinfo(domain, 443, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror:
        return False, f"DNS English text: {domain}, English text"

    # TCP 443 English text + TLS English text
    last_err = ""
    for family, socktype, proto, _, sockaddr in addrs:
        try:
            with socket.create_connection(sockaddr, timeout=timeout) as sock:
                ctx = ssl.create_default_context()
                with ctx.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    if cert is None:
                        return False, f"HTTPS English text: {domain}"
            return True, f"SSO English text: https://{domain}"
        except (socket.timeout, ConnectionRefusedError, OSError) as e:
            last_err = str(e)
            continue

    return False, f"English text https://{domain}(443 English text): {last_err}"


def validate_carsi_entry(url: str, timeout: float = 8.0) -> tuple[bool, str]:
    """English text CARSI English text: HTTP GET English text. 

    English text: English text 2xx/3xx, English text「CARSI」「Shibboleth」English text SSO English text. 
    """
    url = url.strip()
    if not url:
        return False, "CARSI English text URL English text"

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (lit-dl-config-validator)",
                "Accept": "text/html",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            body = resp.read(4096).decode("utf-8", errors="ignore").lower()

            if status >= 400:
                return False, f"CARSI English text HTTP {status}"

            # English text
            keywords = ["carsi", "shibboleth", "idp", "sso", "login", "English text", "English text"]
            matched = [k for k in keywords if k in body]
            if matched:
                return True, f"CARSI English text, English text: {', '.join(matched[:3])}"

            # 3xx English text(English text SSO)
            if 300 <= status < 400:
                location = resp.headers.get("Location", "")
                return True, f"CARSI English text: {location}"

            return True, f"CARSI English text(HTTP {status}), English text SSO English text"

    except urllib.error.URLError as e:
        return False, f"CARSI English text: {e.reason}"
    except Exception as e:
        return False, f"CARSI English text: {e}"


def validate_ezproxy_url(url: str, timeout: float = 8.0) -> tuple[bool, str]:
    """English text EZproxy English text: HTTP GET English text. 

    English text: English text password English text. 
    """
    url = url.strip()
    if not url:
        return False, "EZproxy URL English text"

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (lit-dl-config-validator)",
                "Accept": "text/html",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = resp.getcode()
            body = resp.read(8192).decode("utf-8", errors="ignore").lower()

            if status >= 400:
                return False, f"EZproxy English text HTTP {status}"

            if "password" in body or "English text" in body:
                return True, "EZproxy English text, English text"

            return True, f"EZproxy English text(HTTP {status}), English text"

    except urllib.error.URLError as e:
        return False, f"EZproxy English text: {e.reason}"
    except Exception as e:
        return False, f"EZproxy English text: {e}"


def validate_school_name(name: str) -> tuple[bool, str]:
    """English text. """
    name = name.strip()
    if len(name) < 2:
        return False, "English text"
    if len(name) > 100:
        return False, "English text"
    return True, name


def validate_libraries(libraries: list[str]) -> tuple[bool, str]:
    """English text. """
    if not libraries:
        return False, "English text"
    if len(libraries) > 50:
        return False, "English text"
    return True, f"English text {len(libraries)} English text"


# English text(English text)
KNOWN_DATABASES = [
    "English text (CNKI)",
    "English text",
    "English text",
    "Web of Science",
    "Scopus",
    "IEEE Xplore",
    "ScienceDirect",
    "Springer Link",
    "Wiley Online Library",
    "ACS Publications",
    "RSC Publishing",
    "Nature",
    "Science",
    "Elsevier ScienceDirect",
    "Taylor & Francis",
    "SAGE Journals",
    "EBSCO",
    "ProQuest",
    "JSTOR",
    "English text",
]


if __name__ == "__main__":
    # English text
    print("=== SSO English text ===")
    ok, msg = validate_sso_domain("jaccount.sjtu.edu.cn")
    print(f"  {ok}: {msg}")

    print("\n=== CARSI English text ===")
    ok, msg = validate_carsi_entry("https://www.carsi.edu.cn/")
    print(f"  {ok}: {msg}")
