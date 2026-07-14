---
name: storage-analyzer
description: Run read-only storage analysis on macOS or Windows, classify large disk usage into actionable cleanup tiers, and generate an interactive local HTML report with safe user-controlled actions.
---

# Storage Analyzer — Router

只读地分析磁盘占用，产出一份可操作的清理报告

**Do not answer from memory, and do not answer from this file.**
The actual logic lives in the files below. This router only decides which to load.
Loading them is not optional.

## 1. Load what this request needs

**References** —— 按需读，不要一次全读：

- `references/macos.md`
- `references/windows.md`

**Scripts** —— 这些是真的要跑的，不是拿来读的：

- `scripts/build_report.py`
- `scripts/scan.py`
- `scripts/server.py`

**Assets / templates**：

- `assets/report_template.html`

## 2. Do the work

先说清你**选了哪条路**、**用了哪些文件** —— 一行就够，让用户能便宜地纠正你。

缺必要输入时，写占位符并列在 `Assumptions or missing inputs:` 下面 —— **不要编。**

## 3. Check before delivering

说清你假设了什么、什么没能核实、什么还开着。
