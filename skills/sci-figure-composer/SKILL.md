---
name: sci-figure-composer
description: >-
  Turn scattered panels that already exist into one submission-grade composite figure: layout
  grid, panel labels on a shared axis, consistent fonts and colors, and export. Input is existing
  panels (from any tool); output is one assembled figure. Not for: generating a plot from raw data
  → nature-figure. Not for: slides → nature-paper2ppt. 触发：拼版、组图、多面板图、把这几张图拼成一张、panel 标号对不齐、图注排版。
  Triggers: compose these panels, assemble a multi-panel figure, align panel labels.
---

# SCI Figure Composer

Use this skill to turn scattered panels into a readable, submission-grade manuscript figure. The figure must communicate one scientific conclusion before it looks decorative.

## Entry Contract

Before editing or proposing layout, identify:

- the figure's one-sentence conclusion;
- the target journal or format if known;
- the available panels and their file types;
- which panel is the hero evidence;
- final export needs: editable source, PDF/SVG, TIFF, DPI, or PPT.

If the user supplies an image/PDF/PPT, inspect or render it whenever possible. If the user supplies raw plots/data and asks to generate charts, route to `nature-figure` or the relevant plotting skill first, then return here for composition.

## Composition Workflow

1. **Build the evidence order.** Arrange panels in the order a reviewer should understand the claim, not in the order the experiments were performed.
2. **Assign panel hierarchy.** Choose one hero panel, two or three supporting panels, and any secondary/detail panels. Make the hero visibly larger or more central.
3. **Choose the grid.** Use a simple asymmetric grid when evidence weight differs; use an even grid only when panels are genuinely parallel.
4. **Normalize visual language.** Harmonize fonts, axis label sizes, line weights, scale bars, color roles, legends, and statistical marks.
5. **Reduce local clutter.** Remove repeated legends, redundant titles, oversized axis text, decorative borders, and unused whitespace.
6. **Add reader scaffolding.** Use panel letters, short in-panel labels, arrows/callouts, brackets, and group labels only where they reduce cognitive load.
7. **Check export reality.** Verify the figure at final print width and at screen review size. Ensure all text is legible, panels are not compressed, and raster images meet resolution needs.

## Load References

- Read `references/layout-audit.md` when critiquing an existing figure, screenshot, PDF, PPT slide, or Illustrator-like composition.
- Read `references/rebuild-recipes.md` when proposing or implementing a new arrangement from multiple panels.

## Hard Rules

- Do not make every panel equal size by default.
- Do not use large titles above each panel; prefer short in-panel labels and a strong figure legend.
- Do not let legends, color bars, or axis labels consume more attention than the data.
- Do not mix unrelated fonts, arbitrary line weights, or inconsistent panel letter placement.
- Do not shrink text below likely journal readability just to fit more panels.
- Do not crop microscopy/blot/image panels without preserving scale bars, group labels, and scientific meaning.
- Do not invent data, statistical significance, labels, or experimental group names.

## Quality Gates

Before final delivery or advice, report:

- the figure's conclusion and whether the layout supports it;
- the panel hierarchy;
- the main readability risks;
- the export or resolution risks;
- exact changes made or recommended.

If a rendered file can be produced, inspect it visually before saying the work is done.

## Gates — BLOCK, not advice

**代码跑通 ≠ 图做好了。** matplotlib 不会因为
标签被裁掉、panel 标号错位、字小到印不出、你把位图当「可编辑产物」交付
而报错。**代码零报错，图是废的。**

出图之后、交付之前，必须跑：

```bash
# 位图：DPI 够不够（按最终插入宽度算）、内容有没有被画布裁掉
python3 gates/gate_checks.py figure --file fig1.png --width-mm 180

# 线条图门槛更高（600 dpi）
python3 gates/gate_checks.py figure --file fig1.png --width-mm 180 --line-art

# 矢量：最终尺寸下最小字号够不够；若声称「可编辑」，必须有真的 <text>
python3 gates/gate_checks.py figure --file fig1.svg --width-mm 180 --claim-editable

# 多面板：同一行的标号必须同一个 y，同一列必须同一个 x
python3 gates/gate_checks.py figure --panels panels.csv
```

`--width-mm` 是**最终插进版面的宽度**，不是画布宽度。
单栏常见 85–90 mm，双栏 170–180 mm。**这个数填错，DPI 检查就没意义。**

退出码 2 = 有 BLOCK。**修完重跑，不许交付。**

深层规范见 `../_shared/core/figure-qa.md`（QA 环、release blockers、按结论选图形形式）
和 `../_shared/core/visual-honesty.md`（AI 配图的科学正确性）。
