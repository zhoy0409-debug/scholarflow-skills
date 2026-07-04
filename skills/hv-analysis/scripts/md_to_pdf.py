#!/usr/bin/env python3
"""Convert Markdown to a clean PDF using markdown + WeasyPrint."""

from __future__ import annotations

import argparse
import html
from pathlib import Path

import markdown


CSS_TEMPLATE = """
@page {
  size: A4;
  margin: 25mm 20mm 20mm 20mm;
  @top-center {
    content: "HEADER_TEXT";
    font-family: Arial, Helvetica, sans-serif;
    font-size: 8pt;
    color: #6b7280;
    border-bottom: 0.5pt solid #e5e7eb;
    padding-bottom: 3mm;
  }
  @bottom-center {
    content: "Page " counter(page) " of " counter(pages);
    font-family: Arial, Helvetica, sans-serif;
    font-size: 8pt;
    color: #6b7280;
    border-top: 0.6pt solid #1f4e79;
    padding-top: 2mm;
  }
}
@page :first {
  @top-center { content: none; }
  @bottom-center { content: none; }
}
body {
  font-family: Arial, Helvetica, sans-serif;
  font-size: 10.5pt;
  line-height: 1.65;
  color: #1f2937;
}
.cover {
  page-break-after: always;
  text-align: center;
  padding-top: 38%;
}
.cover h1 {
  font-size: 28pt;
  color: #1f4e79;
  margin-bottom: 8mm;
}
.cover .meta {
  font-size: 11pt;
  color: #6b7280;
  margin-bottom: 4mm;
}
h1 {
  font-size: 20pt;
  color: #1f4e79;
  margin-top: 14mm;
  margin-bottom: 6mm;
  padding-bottom: 3mm;
  border-bottom: 2pt solid #1f4e79;
  page-break-before: always;
}
h1:first-child { page-break-before: auto; }
h2 {
  font-size: 14pt;
  color: #166534;
  margin-top: 9mm;
  margin-bottom: 4mm;
}
h3 {
  font-size: 12pt;
  color: #1d4ed8;
  margin-top: 6mm;
  margin-bottom: 3mm;
}
p { margin: 1.5mm 0; orphans: 3; widows: 3; }
blockquote {
  margin: 4mm 0;
  padding: 4mm 4mm 4mm 8mm;
  background: #f9fafb;
  border-left: 3pt solid #1f4e79;
  color: #4b5563;
}
code {
  font-family: Consolas, "Courier New", monospace;
  background: #fff7ed;
  color: #9a3412;
  padding: 0.5mm 1.5mm;
  border-radius: 2pt;
  font-size: 9.5pt;
}
pre {
  background: #111827;
  color: #f9fafb;
  padding: 4mm;
  border-radius: 4pt;
  white-space: pre-wrap;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin: 5mm 0;
  font-size: 9.5pt;
}
th, td {
  border: 0.5pt solid #d1d5db;
  padding: 2mm 3mm;
}
th { background: #e5eef8; color: #111827; }
img { max-width: 100%; height: auto; }
"""


def build_html(markdown_text: str, title: str, author: str) -> str:
    body = markdown.markdown(
        markdown_text,
        extensions=["extra", "tables", "fenced_code", "toc", "sane_lists"],
        output_format="html5",
    )
    cover = ""
    if title:
        cover = (
            '<section class="cover">'
            f"<h1>{html.escape(title)}</h1>"
            f'<div class="meta">{html.escape(author)}</div>' if author else ""
        )
        cover += "</section>"
    return (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<title>{html.escape(title or 'Markdown Report')}</title>"
        f"<style>{CSS_TEMPLATE.replace('HEADER_TEXT', html.escape(title or 'Markdown Report'))}</style>"
        "</head><body>"
        f"{cover}{body}"
        "</body></html>"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title", default="")
    parser.add_argument("--author", default="")
    args = parser.parse_args()
    try:
        from weasyprint import HTML
    except Exception as exc:
        raise SystemExit(f"WeasyPrint is required to render PDF output: {exc}")
    text = args.input.read_text(encoding="utf-8")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    HTML(string=build_html(text, args.title, args.author), base_url=str(args.input.parent)).write_pdf(str(args.output))
    print(f"Wrote PDF: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
