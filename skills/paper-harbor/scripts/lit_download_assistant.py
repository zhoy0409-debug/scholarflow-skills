#!/usr/bin/env python3
"""Create and maintain a metadata-only literature screening directory."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


SITES = {
    "sciencedirect": {
        "name": "ScienceDirect",
        "port": 9225,
        "url": "https://www.sciencedirect.com/search",
        "profile": "sciencedirect",
    },
    "cnki": {
        "name": "English text/CNKI",
        "port": 9226,
        "url": "https://www.cnki.net/",
        "profile": "cnki",
    },
}

HARD_RECORD_LIMIT = 50

ALIASES = {
    "science-direct": "sciencedirect",
    "science_direct": "sciencedirect",
    "sciencedirect": "sciencedirect",
    "elsevier": "sciencedirect",
    "English text": "cnki",
    "English text": "cnki",
    "cnki": "cnki",
}

CSV_HEADERS = {
    "English text.csv": [
        "record_id",
        "source",
        "title",
        "url",
        "doi",
        "publication_year",
        "journal",
        "discovered_at",
        "status",
    ],
    "English text.csv": [
        "priority",
        "title",
        "authors",
        "journal",
        "publication_year",
        "impact_factor",
        "metric_year",
        "metric_source",
        "doi",
        "source",
        "url",
        "abstract",
        "access_status",
        "zotero_status",
        "zotero_item_key",
        "next_action",
        "notes",
    ],
    "English text.csv": [
        "title",
        "authors",
        "journal",
        "publication_year",
        "impact_factor",
        "metric_year",
        "metric_source",
        "doi",
        "source",
        "url",
        "access_status",
        "zotero_status",
        "zotero_item_key",
        "next_action",
        "notes",
    ],
    "English text.csv": [
        "title",
        "authors",
        "journal",
        "publication_year",
        "impact_factor",
        "metric_year",
        "metric_source",
        "doi",
        "source",
        "url",
        "access_status",
        "zotero_status",
        "zotero_item_key",
        "next_action",
        "notes",
    ],
    "English text.csv": [
        "title",
        "authors",
        "journal",
        "publication_year",
        "impact_factor",
        "metric_year",
        "metric_source",
        "doi",
        "source",
        "url",
        "access_status",
        "zotero_status",
        "zotero_item_key",
        "next_action",
        "notes",
    ],
    "English textZoteroEnglish text.csv": [
        "record_id",
        "title",
        "doi",
        "source",
        "url",
        "journal",
        "publication_year",
        "zotero_item_key",
        "zotero_status",
        "saved_at",
        "access_status",
        "notes",
    ],
    "English text.csv": [
        "title",
        "doi",
        "source",
        "url",
        "reason",
        "next_action",
        "priority",
    ],
}


def normalize_site(value: str | None) -> str | None:
    if not value:
        return None
    key = value.strip().lower().replace(" ", "")
    return ALIASES.get(key)


def parse_prompt(prompt: str) -> dict[str, Any]:
    text = prompt.strip()
    compact = text.lower().replace(" ", "")
    result: dict[str, Any] = {}

    for alias, site in ALIASES.items():
        if alias.lower() in compact or alias in text:
            result["site"] = site
            break

    quoted = re.findall(r"[\""](.+?)[\""]", text)
    site_words = {
        "science direct",
        "sciencedirect",
        "elsevier",
        "English text",
        "English text",
        "cnki",
    }
    if quoted:
        for item in quoted:
            normalized_item = item.strip().lower().replace(" ", "")
            if item.strip().lower() in site_words or normalized_item in site_words:
                continue
            if re.search(r"[\\/]:?|^[A-Za-z]:", item) or item.strip().startswith("."):
                continue
            if re.search(r"(?:19|20)\d{2}|English text|English text|English text|English text|English text", item):
                continue
            result["keywords"] = item.strip()
            break
    else:
        keyword_match = re.search(r"(?:English text|English text|English text|English text)\s*[:: ]?\s*([^, ,. ; ;\n]+)", text)
        if keyword_match:
            result["keywords"] = keyword_match.group(1).strip()

    limit_match = re.search(r"(?:English text|English text|English text)?\s*(\d{1,4})\s*(?:English text|English text|English text)", text)
    if limit_match:
        result["limit"] = int(limit_match.group(1))

    range_match = re.search(r"((?:19|20)\d{2})\s*[-~-English text]\s*((?:19|20)\d{2})", text)
    if range_match:
        result["year_from"] = int(range_match.group(1))
        result["year_to"] = int(range_match.group(2))
    else:
        since_match = re.search(r"((?:19|20)\d{2})\s*(?:English text)?\s*(?:English text|English text|English text|English text)", text)
        if since_match:
            result["year_from"] = int(since_match.group(1))
            result["year_to"] = dt.date.today().year

    if_range = re.search(r"(?:English text|impact\s*factor|if)\s*[:: ]?\s*(\d+(?:\.\d+)?)\s*[-~-English text]\s*(\d+(?:\.\d+)?)", text, re.I)
    if if_range:
        result["if_min"] = float(if_range.group(1))
        result["if_max"] = float(if_range.group(2))
    else:
        if_min = re.search(r"(?:English text|impact\s*factor|if)\s*(?:English text|English text|>=|＞|>)\s*(\d+(?:\.\d+)?)", text, re.I)
        if if_min:
            result["if_min"] = float(if_min.group(1))
        if_max = re.search(r"(?:English text|impact\s*factor|if)\s*(?:English text|English text|<=|＜|<)\s*(\d+(?:\.\d+)?)", text, re.I)
        if if_max:
            result["if_max"] = float(if_max.group(1))

    zotero_collection = re.search(r"English text\s*Zotero\s*(?:English text|English text|collection)?\s*[\""]([^\""]+)[\""]", text, re.I)
    if zotero_collection:
        result["zotero_collection"] = zotero_collection.group(1).strip()

    out_match = re.search(r"(?:English text|English text)\s*[\""]?([^\""\n]+)[\""]?", text)
    if not out_match:
        out_match = re.search(r"English text(?!\s*Zotero)\s*[\""]?([^\""\n]+)[\""]?", text, re.I)
    if out_match:
        result["out"] = out_match.group(1).strip().rstrip(". ; ;,, ")

    return result


def slugify(value: str, max_len: int = 48) -> str:
    safe = re.sub(r"[^\w\u4e00-\u9fff.-]+", "_", value, flags=re.UNICODE).strip("_")
    return (safe or "literature")[:max_len]


def now_stamp() -> str:
    return dt.datetime.now().strftime("%Y%m%d_%H%M%S")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path: Path, headers: list[str]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)


def minimal_pdf_bytes(title: str) -> bytes:
    text = f"{title} - see HTML report for Chinese details."
    escaped = text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
    stream = f"BT /F1 14 Tf 72 720 Td ({escaped}) Tj ET\n".encode("ascii", errors="replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"endstream",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{index} 0 obj\n".encode("ascii")
        out += obj + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n".encode("ascii")
    for offset in offsets[1:]:
        out += f"{offset:010d} 00000 n \n".encode("ascii")
    out += f"trailer << /Root 1 0 R /Size {len(objects) + 1} >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii")
    return bytes(out)


def login_command(site_key: str) -> str:
    site = SITES[site_key]
    return f'.\\scripts\\open_lit_browser.ps1 -Site {site_key}'


def create_scaffold(args: argparse.Namespace) -> Path:
    prompt_text = args.prompt or ""
    if args.prompt_file:
        prompt_text = Path(args.prompt_file).expanduser().read_text(encoding="utf-8")
    prompt_values = parse_prompt(prompt_text)

    site_key = normalize_site(args.site) or prompt_values.get("site")
    if not site_key:
        raise SystemExit("Missing --site. Choose sciencedirect or cnki.")

    keywords = args.keywords or prompt_values.get("keywords")
    if not keywords:
        raise SystemExit("Missing --keywords, or provide a prompt containing keywords.")

    requested_limit = args.limit or prompt_values.get("limit") or 20
    limit = min(requested_limit, HARD_RECORD_LIMIT)
    limit_capped = requested_limit > HARD_RECORD_LIMIT
    year_from = args.year_from if args.year_from is not None else prompt_values.get("year_from")
    year_to = args.year_to if args.year_to is not None else prompt_values.get("year_to")
    if_min = args.if_min if args.if_min is not None else prompt_values.get("if_min")
    if_max = args.if_max if args.if_max is not None else prompt_values.get("if_max")

    site = SITES[site_key]
    default_collection = {
        "sciencedirect": "science direct",
        "cnki": "English text",
    }.get(site_key, site["name"])
    zotero_collection = args.zotero_collection or prompt_values.get("zotero_collection") or default_collection
    out_root = Path(args.out or prompt_values.get("out") or ".").expanduser().resolve()
    run_name = args.run_name or f"{now_stamp()}_{site_key}_{slugify(keywords)}"
    run_dir = out_root / run_name
    internal = run_dir / "English text_English text"
    internal.mkdir(parents=True, exist_ok=True)
    (internal / "logs").mkdir(exist_ok=True)
    (internal / "raw_exports").mkdir(exist_ok=True)

    config = {
        "site": site_key,
        "site_name": site["name"],
        "port": site["port"],
        "start_url": site["url"],
        "keywords": keywords,
        "target_qualified_records": limit,
        "requested_target_qualified_records": requested_limit,
        "hard_record_limit": HARD_RECORD_LIMIT,
        "limit_capped": limit_capped,
        "year_from": year_from,
        "year_to": year_to,
        "impact_factor_min": if_min,
        "impact_factor_max": if_max,
        "zotero_collection": zotero_collection,
        "created_at": dt.datetime.now().isoformat(timespec="seconds"),
        "login_command": login_command(site_key),
        "safety": {
            "scope": "Metadata-only literature screening and Zotero import. No full-text download.",
            "hard_rules": [
                f"Never exceed {HARD_RECORD_LIMIT} target qualifying records in one run.",
                "Do not download PDF/HTML/XML full text.",
                "Do not process records in parallel; import one Zotero metadata item at a time.",
                "Do not bypass paywalls, CAPTCHA, subscription checks, rate limits, browser warnings, hidden APIs, mirrors, or unofficial copies.",
                "If access is unclear or blocked, record the item as pending instead of trying to circumvent.",
            ],
        },
    }

    write_text(internal / "config.json", json.dumps(config, ensure_ascii=False, indent=2))
    write_text(internal / "zotero_import_state.json", json.dumps({"imported": [], "pending": []}, ensure_ascii=False, indent=2))
    write_text(
        internal / "journal_impact_factors.csv",
        "journal,issn,eissn,impact_factor,year,source,notes\n",
    )

    for filename, headers in CSV_HEADERS.items():
        write_csv(run_dir / filename, headers)

    year_text = "English text" if year_from is None and year_to is None else f"{year_from or ''}-{year_to or ''}".strip("-")
    if_text = "English text"
    if if_min is not None and if_max is not None:
        if_text = f"{if_min}-{if_max}"
    elif if_min is not None:
        if_text = f">= {if_min}"
    elif if_max is not None:
        if_text = f"<= {if_max}"

    readme = f"""# English text

English text Zotero English text. 

- English text: {site["name"]}
- English text: {site["port"]}
- English text: {keywords}
- English text: {year_text}
- English text: {if_text}
- English text: {limit}{"(English text 50 English text)" if limit_capped else ""}
- Zotero English text: {zotero_collection}

## English text

- English text 50 English text. 
- English text PDF, English text, English text PDF English text. 
- English text, English text Zotero English text. 
- English text, English text, English text, English text. 
- English text, English text, English text, English text, English text. 

## English text

English text PowerShell English text, English text, English text EasyScholar: 

```powershell
{login_command(site_key)}
```

English text, English text, English text EasyScholar English text IF English text, English text Codex English text Zotero English text. 

## English text

English text: 

1. Zotero Desktop
2. English text Zotero Connector
3. English text EasyScholar

English text Zotero English text/English text collection: `{zotero_collection}`. English text, EasyScholar English text IF, Paper Harbor English text; ScienceDirect English text. 

## English text

English text, DOI, English text, English text, English text Zotero, English text. English text, English text, English text, English text. 
"""
    write_text(run_dir / "README_English text.md", readme)

    plain_readme = f"""English text README_English text.md

English text: {site["name"]}
English text: {site["port"]}
English text: {keywords}
English text: {year_text}
English text: {if_text}
English text: {limit}
Zotero English text: {zotero_collection}

English text: English text; English text, English text. 
"""
    write_text(run_dir / "00_English text_English text.txt", plain_readme)

    plan = f"""# English text

## English text

- English text: {site["name"]} (`{site_key}`)
- English text: `{site["port"]}`
- English text: {site["url"]}
- English text: {keywords}
- English text: {year_text}
- English text: {if_text}
- English text: {limit}{"(English text " + str(requested_limit) + ", English text 50 English text)" if limit_capped else ""}
- Zotero English text: {zotero_collection}

## English text

1. English text 50 English text. 
2. English text PDF, English text, English text PDF English text. 
3. English text, English text Zotero English text. 
4. English text, English text, English text, English text, English text, English text. 
5. English text, English text, English text, English text, English text `English text.csv`. 

## English text

```powershell
{login_command(site_key)}
```

## English text

1. English text. 
2. English text EasyScholar, English text IF English text. 
3. Codex English text. 
4. Codex English text Zotero Desktop, Zotero Connector, EasyScholar English text Zotero collection. 
5. English text UI English text. 
6. English text, English text, DOI, English text, English text, English text, English text. 
7. English text EasyScholar IF English text, English text; English text, English text, English text EasyScholar English text. 
8. English text, English text, English text/English text/English text. 
9. English text, English text Zotero English text `{zotero_collection}`. 
10. English text/Download full issue, English text View PDF English text Download PDF. 
11. English text Zotero English text, English text, English text; English text IF English text IF English text, English text. 
12. English text CSV English text. 

## English text

English text, English text: 

`English text_English text/journal_impact_factors.csv`

English text, English text IF; English text IF English text. English text IF English text, English text IF English text. 
"""
    write_text(run_dir / "English text.md", plan)

    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>English text</title>
  <style>
    body {{ font-family: Arial, "Microsoft YaHei", sans-serif; margin: 32px; line-height: 1.6; }}
    table {{ border-collapse: collapse; width: 100%; max-width: 920px; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f3f5f7; }}
    code {{ background: #f6f8fa; padding: 2px 4px; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>English text</h1>
  <table>
    <tr><th>English text</th><td>{site["name"]}</td></tr>
    <tr><th>English text</th><td>{site["port"]}</td></tr>
    <tr><th>English text</th><td>{keywords}</td></tr>
    <tr><th>English text</th><td>{year_text}</td></tr>
    <tr><th>English text</th><td>{if_text}</td></tr>
    <tr><th>English text</th><td>{limit}{"(English text 50 English text)" if limit_capped else ""}</td></tr>
    <tr><th>Zotero English text</th><td>{zotero_collection}</td></tr>
    <tr><th>English text</th><td>English text, English text, English text Zotero English text. </td></tr>
  </table>
  <h2>English text</h2>
  <ul>
    <li>English text 50 English text. </li>
    <li>English text PDF, English text, English text PDF English text. </li>
    <li>English text, English text Zotero English text. </li>
    <li>English text, English text, English text, English text. </li>
    <li>English text. </li>
  </ul>
  <h2>English text</h2>
  <p>English text, English text Zotero Desktop English text; English text, English text Zotero, English text <code>English textZoteroEnglish text.csv</code>. </p>
</body>
</html>
"""
    write_text(run_dir / "English text.html", html)

    checksum = hashlib.sha256(json.dumps(config, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()
    write_text(internal / "run_checksum.sha256", checksum + "\n")
    write_text(
        internal / "mandatory_policy.json",
        json.dumps(
            {
                "hard_record_limit": HARD_RECORD_LIMIT,
                "serial_zotero_import_only": True,
                "metadata_only": True,
                "no_full_text_download": True,
                "no_bypass": True,
                "blocked_items_go_to_pending_csv": True,
                "zotero_collection": zotero_collection,
            },
            ensure_ascii=False,
            indent=2,
        ),
    )

    return run_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", help="Optional natural-language prompt to parse")
    parser.add_argument("--prompt-file", help="Read the natural-language prompt from a UTF-8 text file")
    parser.add_argument("--site", help="sciencedirect or cnki")
    parser.add_argument("--keywords", help="Literature keywords")
    parser.add_argument("--year-from", type=int, help="Start publication year")
    parser.add_argument("--year-to", type=int, help="End publication year")
    parser.add_argument("--if-min", type=float, help="Minimum impact factor")
    parser.add_argument("--if-max", type=float, help="Maximum impact factor")
    parser.add_argument("--limit", type=int, help="Target qualifying Zotero metadata records to save")
    parser.add_argument("--zotero-collection", help="Zotero collection name to save metadata into")
    parser.add_argument("--out", help="Output root directory")
    parser.add_argument("--run-name", help="Exact run folder name")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    run_dir = create_scaffold(args)
    print(f"Created literature metadata run directory:\n{run_dir}")
    print("\nNext step: open the default-browser command in README_English text.md, log in to the site and EasyScholar, then continue the search.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
