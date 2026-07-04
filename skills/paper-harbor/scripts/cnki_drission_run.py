#!/usr/bin/env python3
"""Search CNKI in an authenticated browser session and export metadata candidates."""

from __future__ import annotations

import argparse
import csv
import html
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

try:
    from DrissionPage import Chromium, ChromiumOptions
except Exception as exc:
    raise SystemExit(f"DrissionPage is required for the CNKI runner: {exc}")


HEADERS = [
    "record_id",
    "priority",
    "title",
    "authors",
    "journal",
    "publication_year",
    "source",
    "url",
    "access_status",
    "notes",
]


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in HEADERS})


def assert_cdp_port_ready(port: int) -> None:
    try:
        with urlopen(f"http://127.0.0.1:{port}/json/version", timeout=3) as response:
            response.read(256)
    except Exception as exc:
        raise RuntimeError(
            f"Browser CDP port {port} is not available. Start the literature browser, sign in to CNKI if needed, and rerun."
        ) from exc


def connect_browser(port: int):
    assert_cdp_port_ready(port)
    options = ChromiumOptions()
    options.set_local_port(port)
    try:
        return Chromium(options)
    except TypeError:
        return Chromium(addr_or_opts=options)


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


def search_url(query: str) -> str:
    return "https://kns.cnki.net/kns8s/defaultresult/index?korder=SU&kw=" + quote(query)


def collect_js() -> str:
    return r"""
const clean = (s) => (s || '').replace(/\s+/g, ' ').trim();
const rows = [...document.querySelectorAll('table.result-table-list tr')]
  .filter((tr) => tr.querySelector('a.fz14[href*="/kcms2/article/abstract"]'));
const items = [];
for (const tr of rows) {
  const titleAnchor = tr.querySelector('a.fz14[href*="/kcms2/article/abstract"]');
  const title = clean(titleAnchor ? titleAnchor.innerText || titleAnchor.textContent : '');
  if (!title) continue;
  const url = titleAnchor ? new URL(titleAnchor.getAttribute('href'), location.href).href : '';
  const cells = [...tr.querySelectorAll('td')].map((td) => clean(td.innerText || td.textContent));
  const authors = cells[2] || '';
  const journal = cells[3] || '';
  const year = (tr.innerText.match(/\b(19|20)\d{2}\b/) || [''])[0];
  items.push({ title, authors, journal, publication_year: year, url });
}
return JSON.stringify(items);
"""


def save_html(path: Path, rows: list[dict[str, str]], query: str) -> None:
    body = "\n".join(
        f"<tr><td>{html.escape(row['priority'])}</td><td>{html.escape(row['title'])}</td>"
        f"<td>{html.escape(row.get('journal',''))}</td><td>{html.escape(row.get('publication_year',''))}</td>"
        f"<td><a href=\"{html.escape(row.get('url',''))}\">open</a></td></tr>"
        for row in rows
    )
    path.write_text(
        f"<!doctype html><html lang=\"en\"><meta charset=\"utf-8\"><title>CNKI Metadata Candidates</title>"
        f"<body><h1>CNKI Metadata Candidates</h1><p>Query: {html.escape(query)}</p>"
        f"<table border=\"1\" cellspacing=\"0\" cellpadding=\"6\"><tr><th>Priority</th><th>Title</th><th>Journal</th><th>Year</th><th>URL</th></tr>{body}</table></body></html>",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--port", type=int, default=9225)
    parser.add_argument("--max-records", type=int, default=50)
    parser.add_argument("--output-dir", type=Path, default=Path("paper_harbor_runs"))
    args = parser.parse_args()
    run_dir = args.output_dir / datetime.now().strftime("cnki-%Y%m%d-%H%M%S")
    run_dir.mkdir(parents=True, exist_ok=True)
    browser = connect_browser(args.port)
    tab = open_tab(browser, search_url(args.query))
    tab.wait.doc_loaded()
    time.sleep(2.5)
    rows = json.loads(tab.run_js(collect_js()) or "[]")[: args.max_records]
    for idx, row in enumerate(rows, start=1):
        row["record_id"] = str(idx)
        row["priority"] = "review"
        row["source"] = "CNKI"
        row["access_status"] = "metadata only"
        row["notes"] = "Verify metadata and access rights before downloading or importing."
    write_csv(run_dir / "cnki_candidates.csv", rows)
    save_html(run_dir / "cnki_summary.html", rows, args.query)
    print(f"Wrote CNKI metadata package: {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
