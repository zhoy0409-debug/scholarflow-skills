#!/usr/bin/env python3
"""Check whether Zotero desktop is running and reachable via its local
connector HTTP server (127.0.0.1:23119).

Usage:
    python zotero_check.py            # ping only
    python zotero_check.py --port 23119

Exit code 0 = Zotero is running and reachable; 1 = not reachable.

The connector server rejects requests whose User-Agent starts with "Mozilla/"
unless the header `zotero-allowed-request: 1` is present, so we always send it.
"""
import argparse
import json
import sys
import urllib.request
import urllib.error

HEADERS = {
    "zotero-allowed-request": "1",
    "X-Zotero-Connector-API-Version": "3",
    "Content-Type": "application/json",
}


def base_url(port: int) -> str:
    return f"http://127.0.0.1:{port}"


def ping(port: int) -> bool:
    url = base_url(port) + "/connector/ping"
    req = urllib.request.Request(url, headers=HEADERS, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            ok = resp.status == 200
            if ok:
                print(f"OK: Zotero connector server responded on {url}")
            return ok
    except urllib.error.HTTPError as e:
        # A response at all (even 4xx) means the server is up.
        print(f"Server reachable but returned HTTP {e.code} on {url}")
        return True
    except (urllib.error.URLError, ConnectionError, OSError) as e:
        print(f"NOT reachable on {url}: {e}", file=sys.stderr)
        print("-> Is the Zotero desktop app open? Open it and retry.", file=sys.stderr)
        return False


def selected_collection(port: int):
    """Best-effort: report the collection currently selected in Zotero."""
    url = base_url(port) + "/connector/getSelectedCollection"
    req = urllib.request.Request(url, data=b"{}", headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode("utf-8", "replace")
            print("Selected collection:", body)
    except Exception as e:  # noqa: BLE001 - informational only
        print(f"(could not read selected collection: {e})")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--port", type=int, default=23119)
    p.add_argument("--collection", action="store_true",
                   help="also report the currently selected Zotero collection")
    args = p.parse_args()

    up = ping(args.port)
    if up and args.collection:
        selected_collection(args.port)
    return 0 if up else 1


if __name__ == "__main__":
    raise SystemExit(main())
