---
name: ppt
description: Plan, author, verify, screenshot, and export PowerPoint slide decks through a filesystem-based deck workflow.
---

# Ppt — Router

从大纲到可导出的 PPTX —— 一个基于文件系统的 deck 工作流

**Do not answer from memory, and do not answer from this file.**
The actual logic lives in the files below. This router only decides which to load.
Loading them is not optional.

## 1. Load what this request needs

**References** —— 按需读，不要一次全读：

- `references/disk-layout.md`
- `references/editable-html-rules.md`
- `references/export-troubleshooting.md`
- `references/material-digest.md`
- `references/research.md`
- `references/story-planning.md`
- `references/visual-qc.md`

**Scripts** —— 这些是真的要跑的，不是拿来读的：

- `scripts/deck.mjs`
- `scripts/export.mjs`
- `scripts/import-reference.mjs`
- `scripts/screenshot.mjs`

## 2. Do the work

先说清你**选了哪条路**、**用了哪些文件** —— 一行就够，让用户能便宜地纠正你。

缺必要输入时，写占位符并列在 `Assumptions or missing inputs:` 下面 —— **不要编。**

## 3. Check before delivering

说清你假设了什么、什么没能核实、什么还开着。
