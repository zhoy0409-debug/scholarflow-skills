#!/usr/bin/env python3
"""Search ScienceDirect in a browser session and export reviewable candidates."""

from __future__ import annotations

import argparse
import csv
import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

try:
    from DrissionPage import Chromium, ChromiumOptions
except Exception as exc:
    raise SystemExit(
        "DrissionPage is required for this runner. Install it in the active Python environment "
        f"or use the browser-guided workflow. Original error: {exc}"
    )


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

try:
    from zotero_bridge import save_metadata_item
except Exception:
    save_metadata_item = None


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in headers})


def assert_cdp_port_ready(port: int) -> None:
    try:
        with urlopen(f"http://127.0.0.1:{port}/json/version", timeout=3) as response:
            response.read(256)
    except Exception as exc:
        raise RuntimeError(
            f"Browser CDP port {port} is not available. Start a browser with remote debugging, "
            "open ScienceDirect, sign in if needed, and rerun this script."
        ) from exc


def connect_browser(port: int):
    assert_cdp_port_ready(port)
    opts = ChromiumOptions()
    opts.set_local_port(port)
    try:
        return Chromium(opts)
    except TypeError:
        return Chromium(addr_or_opts=opts)


def open_tab(browser, url: str):
    try:
        tab = browser.new_tab(url)
    except Exception:
        tab = getattr(browser, "latest_tab", None)
        if isinstance(tab, str):
            tab = browser.get_tab(tab)
        if tab is None:
            raise RuntimeError("Could not open or locate a browser tab.")
        tab.get(url)
    try:
        tab.set.timeouts(12)
    except Exception:
        pass
    return tab


def search_url(query: str, year_from: str, year_to: str) -> str:
    params = {"qs": query, "show": "100"}
    if year_from or year_to:
        params["date"] = f"{year_from or ''}-{year_to or ''}"
    return "https://www.sciencedirect.com/search?" + urlencode(params)


def collect_js() -> str:
    return r"""
const clean = (s) => (s || '').replace(/\s+/g, ' ').trim();
const anchors = [...document.querySelectorAll('a[href*="/science/article/"]')];
const seen = new Set();
const items = [];
for (const a of anchors) {
  const href = new URL(a.getAttribute('href'), location.href).href.split('#')[0];
  const title = clean(a.innerText || a.textContent || '');
  if (!title || title.length < 8 || /\/pdfft\?/i.test(href) || seen.has(href)) continue;
  seen.add(href);
  const card = a.closest('li, article, div[class*="result"], div[class*="Result"], div[class*="card"]') || a.parentElement;
  const text = card ? clean(card.innerText || '') : '';
  const year = (text.match(/\b(19|20)\d{2}\b/) || [''])[0];
  const journal = clean((text.match(/Journal|Book|Volume|Issue/i) || [''])[0]);
  const access = /open access|view pdf|download pdf/i.test(text) ? 'full text visible' : 'check access';
  const ifMatch = text.match(/\bIF\s*[:：]?\s*(\d+(?:\.\d+)?)/i);
  items.push({ title, url: href, year, journal, access, impact_factor: ifMatch ? ifMatch[1] : '', source_text: text.slice(0, 500) });
}
return JSON.stringify(items);
"""


def classify(row: dict[str, str], if_min: float | None) -> str:
    try:
        impact_factor = float(row.get("impact_factor") or "nan")
    except ValueError:
        impact_factor = float("nan")
    if if_min is not None and impact_factor == impact_factor:
        return "high" if impact_factor >= if_min else "low"
    if "full text" in row.get("access", "").lower():
        return "medium"
    return "review"


def save_html(path: Path, rows: list[dict[str, str]], args: argparse.Namespace) -> None:
    items = "\n".join(
        f"<tr><td>{html.escape(row.get('priority',''))}</td><td>{html.escape(row.get('title',''))}</td>"
        f"<td>{html.escape(row.get('year',''))}</td><td><a href=\"{html.escape(row.get('url',''))}\">open</a></td>"
        f"<td>{html.escape(row.get('notes',''))}</td></tr>"
        for row in rows
    )
    path.write_text(
        f"""<!doctype html>
<html lang="en"><meta charset="utf-8"><title>ScienceDirect Search Summary</title>
<body><h1>ScienceDirect Search Summary</h1>
<p><strong>Query:</strong> {html.escape(args.query)}</p>
<p><strong>Year range:</strong> {html.escape(args.year_from or 'any')} - {html.escape(args.year_to or 'any')}</p>
<p><strong>Records:</strong> {len(rows)}</p>
<table border="1" cellspacing="0" cellpadding="6">
<tr><th>Priority</th><th>Title</th><th>Year</th><th>URL</th><th>Notes</th></tr>
{items}
</table></body></html>
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--year-from", default="")
    parser.add_argument("--year-to", default="")
    parser.add_argument("--port", type=int, default=9225)
    parser.add_argument("--if-min", type=float)
    parser.add_argument("--max-records", type=int, default=50)
    parser.add_argument("--output-dir", type=Path, default=Path("paper_harbor_runs"))
    parser.add_argument("--zotero-collection", default="")
    parser.add_argument("--save-zotero", action="store_true")
    args = parser.parse_args()
    run_dir = args.output_dir / datetime.now().strftime("sciencedirect-%Y%m%d-%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)
    browser = connect_browser(args.port)
    tab = open_tab(browser, search_url(args.query, args.year_from, args.year_to))
    raw = tab.run_js(collect_js())
    rows = json.loads(raw or "[]")[: args.max_records]
    for idx, row in enumerate(rows, start=1):
        row["record_id"] = str(idx)
        row["priority"] = classify(row, args.if_min)
        row["source"] = "ScienceDirect"
        row["notes"] = "Verify full text access, journal fit, and citation metadata before importing."
    headers = ["record_id", "priority", "title", "year", "journal", "impact_factor", "access", "source", "url", "notes"]
    write_csv(run_dir / "science_direct_candidates.csv", headers, rows)
    zotero_rows: list[dict[str, str]] = []
    if args.save_zotero and save_metadata_item is not None:
        for row in rows:
            result = save_metadata_item(
                title=row.get("title", ""),
                url=row.get("url", ""),
                publication_title=row.get("journal", ""),
                year=row.get("year", ""),
                collection=args.zotero_collection or None,
            )
            zotero_rows.append({**row, "zotero_status": str(result)})
    write_csv(run_dir / "zotero_saved_items.csv", headers + ["zotero_status"], zotero_rows)
    save_html(run_dir / "science_direct_summary.html", rows, args)
    print(f"Wrote ScienceDirect candidate package: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
