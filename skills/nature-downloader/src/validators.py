"""Validation helpers for institutional literature-access configuration."""

from __future__ import annotations

import socket
import ssl
import urllib.error
import urllib.request


def validate_sso_domain(domain: str, timeout: float = 5.0) -> tuple[bool, str]:
    """Validate an SSO host with DNS lookup, TCP 443, and TLS handshake."""
    domain = domain.strip().lower()
    if not domain:
        return False, "SSO domain is empty"
    for prefix in ("https://", "http://"):
        if domain.startswith(prefix):
            domain = domain[len(prefix):]
    domain = domain.split("/")[0]
    try:
        addresses = socket.getaddrinfo(domain, 443, socket.AF_UNSPEC, socket.SOCK_STREAM)
    except socket.gaierror:
        return False, f"DNS lookup failed for {domain}"
    last_error = ""
    for family, socktype, proto, _, sockaddr in addresses:
        try:
            with socket.create_connection(sockaddr, timeout=timeout) as sock:
                context = ssl.create_default_context()
                with context.wrap_socket(sock, server_hostname=domain) as tls_sock:
                    if tls_sock.getpeercert() is None:
                        return False, f"No TLS certificate returned by {domain}"
            return True, f"SSO domain reachable: https://{domain}"
        except (socket.timeout, ConnectionRefusedError, OSError) as exc:
            last_error = str(exc)
    return False, f"Could not connect to https://{domain}: {last_error}"


def _http_probe(url: str, timeout: float, label: str) -> tuple[bool, str]:
    url = url.strip()
    if not url:
        return False, f"{label} URL is empty"
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (lit-dl-config-validator)", "Accept": "text/html"},
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            status = response.getcode()
            body = response.read(8192).decode("utf-8", errors="ignore").lower()
            if status >= 400:
                return False, f"{label} returned HTTP {status}"
            keywords = ["carsi", "shibboleth", "idp", "sso", "login", "ezproxy", "proxy"]
            matched = [item for item in keywords if item in body]
            detail = f"; matched: {', '.join(matched[:3])}" if matched else ""
            return True, f"{label} reachable (HTTP {status}){detail}"
    except urllib.error.URLError as exc:
        return False, f"{label} probe failed: {exc.reason}"
    except Exception as exc:
        return False, f"{label} probe failed: {exc}"


def validate_carsi_entry(url: str, timeout: float = 8.0) -> tuple[bool, str]:
    """Validate a CARSI/Shibboleth entry URL."""
    return _http_probe(url, timeout, "CARSI entry")


def validate_ezproxy_url(url: str, timeout: float = 8.0) -> tuple[bool, str]:
    """Validate an EZproxy entry URL."""
    return _http_probe(url, timeout, "EZproxy")


def validate_school_name(name: str) -> tuple[bool, str]:
    name = name.strip()
    if len(name) < 2:
        return False, "Institution name is too short"
    if len(name) > 120:
        return False, "Institution name is too long"
    return True, name


def validate_libraries(libraries: list[str]) -> tuple[bool, str]:
    if not libraries:
        return False, "At least one library platform is required"
    if len(libraries) > 50:
        return False, "Library list is unusually long; keep only relevant platforms"
    return True, f"{len(libraries)} library platforms configured"


KNOWN_DATABASES = [
    "CNKI",
    "Wanfang Data",
    "VIP",
    "Web of Science",
    "Scopus",
    "PubMed",
    "IEEE Xplore",
    "ScienceDirect",
    "SpringerLink",
    "Wiley Online Library",
    "ACS Publications",
    "RSC Publishing",
    "Nature",
    "Science",
    "Taylor & Francis",
    "SAGE Journals",
    "EBSCO",
    "ProQuest",
]
