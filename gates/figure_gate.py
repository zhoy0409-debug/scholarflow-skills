#!/usr/bin/env python3
"""
figure 门禁 —— 「代码跑通」不等于「图做好了」。

matplotlib 不会因为
  · 标签被画布裁掉
  · panel 标号错位
  · 字小到印出来看不清
  · 你把一张位图套进 SVG 然后说它「可编辑」
而报错。**代码零报错，图是废的。**

所以这些必须由门禁来拦。每一条都是**机械可查**的 —— 不需要模型判断，
不需要人肉看图。

  python3 gates/gate_checks.py figure --file fig1.png --width-mm 180
  python3 gates/gate_checks.py figure --file fig1.svg --claim-editable
  python3 gates/gate_checks.py figure --panels panels.csv

## 各检查在拦什么

  dpi_at_final_size   一张 800×600 的 PNG 插进双栏 180mm 宽的版面，
                      实际是 113 dpi —— 印出来是糊的。期刊要 ≥300（线条图 ≥600）。
                      **这是最常见、也最晚被发现的错**（送印才发现）。

  content_not_clipped 画布最外圈有墨 → 内容被裁掉了。
                      matplotlib 的 tight_layout 失败时正是这个样子，而它不报错。

  text_is_real_text   声称「可编辑」的 SVG/PDF 里必须有真的 <text> 元素。
                      **把 PNG 套进 SVG 不会让底层图元可编辑** —— 这是谎话，
                      而且会在期刊要求提供可编辑源文件时暴雷。

  min_text_size       SVG 里的 font-size 换算到最终尺寸后 < 5pt → 印出来读不了。

  panel_labels_grid   同一行的 panel 标号必须同一个 y，同一列必须同一个 x。
                      「差不多对齐」在审稿人眼里就是没对齐。
"""
from __future__ import annotations

import csv
import re
import xml.etree.ElementTree as ET
from pathlib import Path

MM_PER_INCH = 25.4

# 期刊的最低要求。线条图（纯矢量元素栅格化）要求更高。
DPI_MIN = 300
DPI_MIN_LINE_ART = 600
# 最终尺寸下的最小字号（pt）。低于这个印出来读不了。
PT_MIN = 5.0
# panel 标号对齐容差（px）。超过这个就是肉眼可见的错位。
GRID_TOL_PX = 3


def _ink_on_border(img, border=2, thresh=250):
    """最外圈 border 像素里有没有「墨」（非白/非透明）。有 → 内容被裁了。"""
    px = img.convert("RGBA")
    w, h = px.size
    data = px.load()

    def inked(x, y):
        r, g, b, a = data[x, y]
        if a < 8:                      # 透明 = 没墨
            return False
        return min(r, g, b) < thresh   # 明显比白暗

    hits = 0
    for y in list(range(border)) + list(range(h - border, h)):
        for x in range(w):
            if inked(x, y):
                hits += 1
    for x in list(range(border)) + list(range(w - border, w)):
        for y in range(border, h - border):
            if inked(x, y):
                hits += 1
    return hits


def check_raster(path: Path, width_mm: float, line_art: bool, R):
    try:
        from PIL import Image
    except ImportError:
        R.warn("dpi_at_final_size", "没装 Pillow，跳过位图检查（pip install pillow）")
        return
    img = Image.open(path)
    w, h = img.size

    # ── DPI ──────────────────────────────────────────────
    need = DPI_MIN_LINE_ART if line_art else DPI_MIN
    dpi = w / (width_mm / MM_PER_INCH)
    if dpi < need:
        R.block("dpi_at_final_size",
                f"{w}×{h} px 插进 {width_mm:g}mm 宽 → 实际 {dpi:.0f} dpi，"
                f"低于 {need}。印出来是糊的。"
                f"需要至少 {int(need * width_mm / MM_PER_INCH)} px 宽")
    else:
        R.ok("dpi_at_final_size")

    # ── 裁切 ─────────────────────────────────────────────
    hits = _ink_on_border(img)
    if hits > max(8, (w + h) * 0.01):
        R.block("content_not_clipped",
                f"画布最外圈有 {hits} 个墨点 → 内容被裁掉了。"
                f"（tight_layout 失败时正是这样，而它不报错）")
    else:
        R.ok("content_not_clipped")


SVG_NS = "{http://www.w3.org/2000/svg}"


def check_svg(path: Path, width_mm: float, claim_editable: bool, R):
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        R.block("svg_parses", f"SVG 解析失败: {e}")
        return

    texts = root.iter(f"{SVG_NS}text")
    n_text = sum(1 for _ in texts)
    n_image = sum(1 for _ in root.iter(f"{SVG_NS}image"))
    n_path = sum(1 for _ in root.iter(f"{SVG_NS}path"))

    # ── 可编辑性诚信 ─────────────────────────────────────
    if claim_editable:
        if n_text == 0:
            R.block("text_is_real_text",
                    f"声称可编辑，但 SVG 里没有一个 <text> 元素"
                    f"（{n_image} 个 <image>，{n_path} 个 <path>）。"
                    f"**把 PNG 套进 SVG 不会让底层图元可编辑。**")
        elif n_image and n_path < 5:
            R.block("text_is_real_text",
                    f"声称可编辑，但内容基本是 {n_image} 张嵌入位图 "
                    f"（只有 {n_path} 个矢量 path、{n_text} 个 text）。"
                    f"原始像素不可编辑 —— 只能说「部分可编辑」")
        else:
            R.ok("text_is_real_text")
    elif n_text == 0 and n_image:
        R.warn("text_is_real_text",
               f"SVG 里只有嵌入位图、没有 <text> —— 交付时必须说明「原始像素不可编辑」")

    # ── 最小字号 ─────────────────────────────────────────
    # SVG 用户单位 → 最终 pt：需要知道画布宽度对应多少 mm
    vb = root.get("viewBox")
    canvas_w = None
    if vb:
        try:
            canvas_w = float(vb.split()[2])
        except (ValueError, IndexError):
            pass
    if canvas_w is None:
        m = re.match(r"([\d.]+)", root.get("width") or "")
        if m:
            canvas_w = float(m.group(1))

    if canvas_w and n_text:
        # 1 pt = 1/72 inch
        pt_per_unit = (width_mm / MM_PER_INCH * 72) / canvas_w
        smallest, where = None, ""
        for t in root.iter(f"{SVG_NS}text"):
            fs = t.get("font-size") or ""
            m = re.match(r"([\d.]+)", (fs or (t.get("style") or "")).replace("font-size:", ""))
            if not m and t.get("style"):
                m = re.search(r"font-size:\s*([\d.]+)", t.get("style"))
            if not m:
                continue
            pt = float(m.group(1)) * pt_per_unit
            if smallest is None or pt < smallest:
                smallest, where = pt, ("".join(t.itertext()) or "")[:24]
        if smallest is None:
            R.warn("min_text_size", "读不到 font-size，无法核算最终字号")
        elif smallest < PT_MIN:
            R.block("min_text_size",
                    f"最小文字在 {width_mm:g}mm 宽下只有 {smallest:.1f} pt "
                    f"（低于 {PT_MIN} pt）—— 印出来读不了。文字：“{where}”")
        else:
            R.ok("min_text_size")


def check_panels(path: Path, R):
    """panel 标号网格：同行同 y，同列同 x。

    输入 CSV：panel,row,col,label_x,label_y   （像素坐标）
    """
    with path.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        R.block("panel_labels_grid", "panel 表为空")
        return

    need = {"panel", "row", "col", "label_x", "label_y"}
    if not need <= set(rows[0]):
        R.block("panel_labels_grid",
                f"panel 表缺列，需要 {sorted(need)}，实际 {sorted(rows[0])}")
        return

    by_row, by_col = {}, {}
    for r in rows:
        by_row.setdefault(r["row"], []).append((r["panel"], float(r["label_y"])))
        by_col.setdefault(r["col"], []).append((r["panel"], float(r["label_x"])))

    bad = []
    for k, items in by_row.items():
        ys = [y for _, y in items]
        if max(ys) - min(ys) > GRID_TOL_PX:
            off = max(items, key=lambda t: abs(t[1] - min(ys)))
            bad.append(f"第 {k} 行的标号 y 不齐（跨度 {max(ys)-min(ys):.0f}px，"
                       f"容差 {GRID_TOL_PX}px）—— panel {off[0]} 偏得最多")
    for k, items in by_col.items():
        xs = [x for _, x in items]
        if max(xs) - min(xs) > GRID_TOL_PX:
            off = max(items, key=lambda t: abs(t[1] - min(xs)))
            bad.append(f"第 {k} 列的标号 x 不齐（跨度 {max(xs)-min(xs):.0f}px，"
                       f"容差 {GRID_TOL_PX}px）—— panel {off[0]} 偏得最多")

    if bad:
        for b in bad:
            R.block("panel_labels_grid", b)
    else:
        R.ok("panel_labels_grid")


def check_figure(file: Path | None, width_mm: float, line_art: bool,
                 claim_editable: bool, panels: Path | None, R):
    if panels:
        check_panels(panels, R)
    if not file:
        return
    ext = file.suffix.lower()
    if ext in (".png", ".jpg", ".jpeg", ".tif", ".tiff"):
        check_raster(file, width_mm, line_art, R)
        if claim_editable:
            R.block("text_is_real_text",
                    f"{ext} 是位图。**位图不可编辑。** 声称「可编辑产物」是谎话 —— "
                    f"要么交 SVG/PDF（含真 <text>），要么如实说「raster only」")
    elif ext == ".svg":
        check_svg(file, width_mm, claim_editable, R)
    elif ext == ".pdf":
        R.warn("pdf_check", "PDF 检查尚未实现 —— 先导 SVG 检查，或人工确认字体已嵌入")
    else:
        R.warn("unknown_format", f"不认识的格式 {ext}")
