"""figure 门禁的测试。

重点不是「代码能跑」，是「歪的图真的会被拦下」。
每个 test 对应一种 matplotlib **不会报错**、但图是废的情况。
"""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gate_checks import Result
from figure_gate import check_figure, DPI_MIN, PT_MIN

F = Path(__file__).resolve().parents[1] / "fixtures"


def run(**kw):
    r = Result()
    check_figure(kw.get("file"), kw.get("width_mm", 180.0), kw.get("line_art", False),
                 kw.get("claim_editable", False), kw.get("panels"), r)
    return r


def blocks(r):
    return [g for g, _ in r.blocks]


# ── DPI ────────────────────────────────────────────────
def test_low_dpi_blocks():
    """800px 宽插进 180mm 双栏 = 113 dpi。送印才发现就晚了。"""
    r = run(file=F / "fig_lowdpi.png")
    assert "dpi_at_final_size" in blocks(r)


def test_sufficient_dpi_passes():
    r = run(file=F / "fig_ok.png")
    assert not r.failed, r.blocks


def test_line_art_needs_600dpi():
    """线条图门槛更高 —— 300 dpi 的线条图印出来会有锯齿。"""
    ok_at_300 = run(file=F / "fig_ok.png", line_art=False)
    assert not ok_at_300.failed
    strict = run(file=F / "fig_ok.png", line_art=True)
    assert "dpi_at_final_size" in blocks(strict)


# ── 裁切 ───────────────────────────────────────────────
def test_clipped_content_blocks():
    """tight_layout 失败时，内容会画到画布边缘 —— 而 matplotlib 不报错。"""
    r = run(file=F / "fig_clipped.png")
    assert "content_not_clipped" in blocks(r)


# ── 可编辑性诚信 ───────────────────────────────────────
def test_png_wrapped_in_svg_is_not_editable():
    """把 PNG 套进 SVG 壳，然后当「可编辑源文件」交出去 —— 这是谎话。"""
    r = run(file=F / "fig_fake_editable.svg", claim_editable=True)
    assert "text_is_real_text" in blocks(r)


def test_real_svg_with_text_passes():
    r = run(file=F / "fig_editable.svg", claim_editable=True)
    assert not r.failed, r.blocks


def test_raster_claimed_editable_blocks():
    """位图就是位图。声称可编辑 → BLOCK。"""
    r = run(file=F / "fig_ok.png", claim_editable=True)
    assert "text_is_real_text" in blocks(r)


# ── 字号 ───────────────────────────────────────────────
def test_tiny_text_blocks():
    """在最终插入尺寸下算出来只有 3pt —— 印出来读不了。"""
    r = run(file=F / "fig_tinytext.svg")
    assert "min_text_size" in blocks(r)
    msg = dict(r.blocks)["min_text_size"]
    assert "pt" in msg and str(PT_MIN) in msg


def test_text_size_depends_on_final_width():
    """同一张 SVG，插进单栏（85mm）比插进双栏（180mm）更危险。"""
    wide = run(file=F / "fig_editable.svg", width_mm=180)
    narrow = run(file=F / "fig_editable.svg", width_mm=40)   # 极窄
    assert not wide.failed
    assert "min_text_size" in blocks(narrow)


# ── panel 标号网格 ─────────────────────────────────────
def test_misaligned_panel_labels_block():
    """同一行的标号 y 不一致 = 肉眼可见的错位 = 审稿人第一眼看到的东西。"""
    r = run(panels=F / "panels_off.csv")
    assert "panel_labels_grid" in blocks(r)
    msgs = " ".join(m for g, m in r.blocks)
    assert "panel b" in msgs and "panel d" in msgs


def test_aligned_panel_labels_pass():
    r = run(panels=F / "panels_ok.csv")
    assert not r.failed, r.blocks


# ── 组合 ───────────────────────────────────────────────
def test_file_and_panels_together():
    r = run(file=F / "fig_lowdpi.png", panels=F / "panels_off.csv")
    b = blocks(r)
    assert "dpi_at_final_size" in b and "panel_labels_grid" in b
