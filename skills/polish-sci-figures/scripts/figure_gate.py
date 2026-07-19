#!/usr/bin/env python3
"""Mechanical figure delivery gates for ScholarFlow figure work.

These checks catch failures that plotting libraries usually treat as successful
exports: low final DPI, clipped raster content, fake editable SVGs, tiny SVG
text, and misaligned panel labels.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

MM_PER_INCH = 25.4
DPI_MIN = 300
DPI_MIN_LINE_ART = 600
PT_MIN = 5.0
GRID_TOL_PX = 3


@dataclass
class Result:
    blocks: list[tuple[str, str]] = field(default_factory=list)
    warns: list[tuple[str, str]] = field(default_factory=list)
    passes: list[str] = field(default_factory=list)

    def block(self, gate: str, msg: str) -> None:
        self.blocks.append((gate, msg))

    def warn(self, gate: str, msg: str) -> None:
        self.warns.append((gate, msg))

    def ok(self, gate: str) -> None:
        self.passes.append(gate)

    @property
    def failed(self) -> bool:
        return bool(self.blocks)

    def report(self) -> None:
        for gate in self.passes:
            print(f"PASS  {gate}")
        for gate, msg in self.warns:
            print(f"WARN  {gate}: {msg}")
        for gate, msg in self.blocks:
            print(f"BLOCK {gate}: {msg}")


def _ink_on_border(img, border: int = 2, thresh: int = 250) -> int:
    px = img.convert("RGBA")
    w, h = px.size
    data = px.load()

    def inked(x: int, y: int) -> bool:
        r, g, b, a = data[x, y]
        return a >= 8 and min(r, g, b) < thresh

    hits = 0
    for y in list(range(border)) + list(range(h - border, h)):
        for x in range(w):
            hits += int(inked(x, y))
    for x in list(range(border)) + list(range(w - border, w)):
        for y in range(border, h - border):
            hits += int(inked(x, y))
    return hits


def check_raster(path: Path, width_mm: float, line_art: bool, result: Result) -> None:
    try:
        from PIL import Image
    except ImportError:
        result.warn("dpi_at_final_size", "Pillow is not installed; raster checks skipped.")
        return

    img = Image.open(path)
    w, h = img.size
    need = DPI_MIN_LINE_ART if line_art else DPI_MIN
    dpi = w / (width_mm / MM_PER_INCH)
    if dpi < need:
        result.block(
            "dpi_at_final_size",
            f"{w}x{h}px at {width_mm:g}mm final width is {dpi:.0f} dpi; needs {need}+ dpi.",
        )
    else:
        result.ok("dpi_at_final_size")

    hits = _ink_on_border(img)
    if hits > max(8, (w + h) * 0.01):
        result.block("content_not_clipped", f"{hits} inked border pixels suggest clipped content.")
    else:
        result.ok("content_not_clipped")


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _svg_width_units(root) -> float | None:
    view_box = root.get("viewBox")
    if view_box:
        try:
            return float(view_box.split()[2])
        except (IndexError, ValueError):
            pass
    match = re.match(r"([\d.]+)", root.get("width") or "")
    return float(match.group(1)) if match else None


def _font_size_pt(text_node, pt_per_unit: float) -> float | None:
    raw = text_node.get("font-size") or ""
    style = text_node.get("style") or ""
    match = re.match(r"([\d.]+)", raw) or re.search(r"font-size:\s*([\d.]+)", style)
    return float(match.group(1)) * pt_per_unit if match else None


def check_svg(path: Path, width_mm: float, claim_editable: bool, result: Result) -> None:
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as exc:
        result.block("svg_parses", f"SVG parse failed: {exc}")
        return

    nodes = list(root.iter())
    texts = [node for node in nodes if _local_name(node.tag) == "text"]
    images = [node for node in nodes if _local_name(node.tag) == "image"]
    paths = [node for node in nodes if _local_name(node.tag) == "path"]

    if claim_editable:
        if not texts:
            result.block(
                "text_is_real_text",
                f"Editable output claimed, but SVG has 0 text elements ({len(images)} images, {len(paths)} paths).",
            )
        elif images and len(paths) < 5:
            result.block(
                "text_is_real_text",
                f"Editable output claimed, but SVG is mostly {len(images)} embedded image(s).",
            )
        else:
            result.ok("text_is_real_text")
    elif images and not texts:
        result.warn("text_is_real_text", "SVG appears raster-only; do not describe it as fully editable.")

    canvas_w = _svg_width_units(root)
    if canvas_w and texts:
        pt_per_unit = (width_mm / MM_PER_INCH * 72) / canvas_w
        sizes = [
            (size, ("".join(node.itertext()) or "")[:24])
            for node in texts
            for size in [_font_size_pt(node, pt_per_unit)]
            if size is not None
        ]
        if not sizes:
            result.warn("min_text_size", "No SVG font-size values found; final text size was not checked.")
        else:
            smallest, label = min(sizes, key=lambda item: item[0])
            if smallest < PT_MIN:
                result.block(
                    "min_text_size",
                    f"Smallest text is {smallest:.1f}pt at {width_mm:g}mm final width; minimum is {PT_MIN:g}pt. Text: {label}",
                )
            else:
                result.ok("min_text_size")


def check_panels(path: Path, result: Result) -> None:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    required = {"panel", "row", "col", "label_x", "label_y"}
    if not rows:
        result.block("panel_labels_grid", "Panel label CSV is empty.")
        return
    if not required <= set(rows[0]):
        result.block("panel_labels_grid", f"Panel CSV needs columns: {sorted(required)}.")
        return

    by_row: dict[str, list[tuple[str, float]]] = {}
    by_col: dict[str, list[tuple[str, float]]] = {}
    for row in rows:
        by_row.setdefault(row["row"], []).append((row["panel"], float(row["label_y"])))
        by_col.setdefault(row["col"], []).append((row["panel"], float(row["label_x"])))

    for row_id, items in by_row.items():
        values = [value for _, value in items]
        if max(values) - min(values) > GRID_TOL_PX:
            result.block("panel_labels_grid", f"Row {row_id} label y positions differ by {max(values) - min(values):.0f}px.")
    for col_id, items in by_col.items():
        values = [value for _, value in items]
        if max(values) - min(values) > GRID_TOL_PX:
            result.block("panel_labels_grid", f"Column {col_id} label x positions differ by {max(values) - min(values):.0f}px.")

    if not any(gate == "panel_labels_grid" for gate, _ in result.blocks):
        result.ok("panel_labels_grid")


def check_figure(
    file: Path | None,
    width_mm: float,
    line_art: bool,
    claim_editable: bool,
    panels: Path | None,
    result: Result,
) -> None:
    if panels:
        check_panels(panels, result)
    if not file:
        return
    suffix = file.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".tif", ".tiff"}:
        check_raster(file, width_mm, line_art, result)
        if claim_editable:
            result.block("text_is_real_text", f"{suffix} is raster-only; it cannot be claimed as editable.")
    elif suffix == ".svg":
        check_svg(file, width_mm, claim_editable, result)
    else:
        result.warn("unknown_format", f"No mechanical figure gate for {suffix}.")


def self_check() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        fake_svg = root / "fake.svg"
        fake_svg.write_text(
            '<svg width="100" viewBox="0 0 100 100"><image href="data:image/png;base64,AA=="/></svg>',
            encoding="utf-8",
        )
        tiny_svg = root / "tiny.svg"
        tiny_svg.write_text(
            '<svg width="100" viewBox="0 0 100 100"><text x="1" y="10" font-size="2">tiny</text></svg>',
            encoding="utf-8",
        )
        panels = root / "panels.csv"
        panels.write_text(
            "panel,row,col,label_x,label_y\n"
            "a,1,1,40,40\nb,1,2,540,57\nc,2,1,40,540\nd,2,2,563,540\n",
            encoding="utf-8",
        )
        result = Result()
        check_figure(fake_svg, 180, False, True, panels, result)
        check_figure(tiny_svg, 40, False, False, None, result)
        blocked = {gate for gate, _ in result.blocks}
        assert {"text_is_real_text", "panel_labels_grid", "min_text_size"} <= blocked, result.blocks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run mechanical gates on exported scientific figures.")
    parser.add_argument("--file", type=Path, help="Figure file: PNG, JPG, TIFF, or SVG.")
    parser.add_argument("--width-mm", type=float, default=180.0, help="Final inserted width in millimeters.")
    parser.add_argument("--line-art", action="store_true", help="Require 600 dpi for line-art raster output.")
    parser.add_argument("--claim-editable", action="store_true", help="Block outputs that are not genuinely editable.")
    parser.add_argument("--panels", type=Path, help="CSV with panel,row,col,label_x,label_y columns.")
    parser.add_argument("--self-check", action="store_true", help="Run the bundled smoke check.")
    args = parser.parse_args(argv)

    if args.self_check:
        self_check()
        print("self-check passed")
        return 0
    if not args.file and not args.panels:
        parser.error("provide --file, --panels, or --self-check")

    result = Result()
    check_figure(args.file, args.width_mm, args.line_art, args.claim_editable, args.panels, result)
    result.report()
    return 2 if result.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
