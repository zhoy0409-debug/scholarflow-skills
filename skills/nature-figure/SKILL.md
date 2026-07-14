---
name: nature-figure
description: Plan, build, and quality-check scientific figures so panels, statistics, legends, visual hierarchy, and export settings support the manuscript argument.
---

# Manuscript Figures — Router

**Do not answer from memory, and do not answer from this file.**
The actual logic lives in `static/` and `references/`. This file only decides
which fragments to load for the request in front of you. Loading them is not optional.

## Routing protocol

### 1. Load the core layer

Read [manifest.yaml](manifest.yaml). Then Read **every** file it lists under `always_load`:

- `static/core/contract.md`
- `static/core/stance.md`

These carry the default stance, workflow, and output format for every job in this skill.

### 2. Detect the axes

The manifest declares these axes. Decide a value for each from the user's input:

- **`backend`** — `python` / `r`

State the detected values in one short line before you start, so the user can
correct you cheaply instead of after you have produced the wrong thing.
If an axis is genuinely ambiguous **and it changes the output**, ask. Otherwise pick the default.

### 3. Load only the matching fragments

For each axis value, Read the file the manifest maps it to.
**Do not read every file in `static/`** — load only what step 2 selected.

### 4. Do the work

Apply the loaded fragments. The `always_load` core wins on stance; the axis
fragments win on specifics. If required input is missing, write a placeholder and
list it under `Assumptions or missing inputs:` — **do not invent it.**

### 5. Open `references/` only on demand

`references/` is a deep library, not a default. Opening all of it wastes the context
you need for the actual work.

The manifest's `references.on_demand` table says which file answers which question.
Consult it, then Read only that file.

## Gates — BLOCK, not advice

These are not suggestions. If a gate fails, **fix it and re-run; do not deliver.**

- Read `../_shared/core/figure-qa.md` — 「代码跑通 ≠ 图做好了」：必须真的打开 PNG 看，必须按最终插入尺寸看
- Read `../_shared/core/visual-honesty.md` — AI 配图的科学正确性门禁

The repo ships an executable version of these checks:

```bash
python3 gates/gate_checks.py claims    --claims c.csv --evidence e.csv --manuscript draft.md
python3 gates/gate_checks.py data      --file raw.xlsx
python3 gates/gate_checks.py narrative --matrix slides.csv
```

Exit code 2 means a BLOCK fired. Run them when the artefacts exist.
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

