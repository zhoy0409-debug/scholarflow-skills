#!/usr/bin/env python3
"""Create items in Zotero via the local connector server's /connector/saveItems
endpoint. Use this as a FALLBACK when the Zotero Connector browser extension's
translator cannot handle a page, or to attach an open-access (public) PDF found
via oa_pdf.py.

IMPORTANT: The Zotero process running this endpoint has NO browser cookies, so
any attachment URL you pass must be PUBLICLY downloadable (OA PDF / PMC / arXiv).
Gated PDFs (CNKI, Wanfang, subscription publishers) must be captured by the
browser extension inside the user's logged-in session, not here.

Input: a JSON file (or stdin) shaped as either
  (a) a full payload: {"items": [ ... ]}
  (b) a bare list:    [ {item1}, {item2} ]

Each item uses Zotero item format (not CSL-JSON). Minimal example:
  {"itemType": "journalArticle", "title": "...", "creators": [...], "date": "2024"}

Usage:
    python zotero_save.py items.json
    cat items.json | python zotero_save.py -
    python zotero_save.py items.json --port 23119
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


def load_payload(path: str) -> dict:
    raw = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
    data = json.loads(raw)
    if isinstance(data, list):
        data = {"items": data}
    if "items" not in data or not isinstance(data["items"], list):
        raise ValueError("Payload must contain an 'items' list.")
    return data


def save_items(payload: dict, port: int) -> int:
    url = f"http://127.0.0.1:{port}/connector/saveItems"
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=HEADERS, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            out = resp.read().decode("utf-8", "replace")
            print(f"HTTP {resp.status}")
            print(out)
            return 0
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")
        print(f"HTTP {e.code}: {detail}", file=sys.stderr)
        if e.code == 403:
            print("-> 403 usually means the 'zotero-allowed-request' header was "
                  "rejected; ensure Zotero is up to date.", file=sys.stderr)
        return 1
    except (urllib.error.URLError, OSError) as e:
        print(f"Cannot reach Zotero on {url}: {e}", file=sys.stderr)
        print("-> Open the Zotero desktop app and retry.", file=sys.stderr)
        return 1


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("payload", help="path to JSON file, or '-' for stdin")
    p.add_argument("--port", type=int, default=23119)
    args = p.parse_args()

    try:
        payload = load_payload(args.payload)
    except (ValueError, json.JSONDecodeError, OSError) as e:
        print(f"Bad input: {e}", file=sys.stderr)
        return 2

    n = len(payload["items"])
    print(f"Sending {n} item(s) to Zotero...")
    return save_items(payload, args.port)


if __name__ == "__main__":
    raise SystemExit(main())
