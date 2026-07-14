---
name: support-to-repro-pack
description: Convert support materials into a reproducibility package with organized files, metadata, methods notes, environment details, redaction checks, and reviewer-friendly structure.
---

# Support To Repro Pack — Router

把支持材料整理成一个可复现的交付包

**Do not answer from memory, and do not answer from this file.**
The actual logic lives in the files below. This router only decides which to load.
Loading them is not optional.

## 1. Load what this request needs

**References** —— 按需读，不要一次全读：

- `references/pii-redaction-rules.md`
- `references/reproduction-checklist.md`
- `references/severity-matrix.md`

**Assets / templates**：

- `templates/customer_reply.md`
- `templates/engineering_issue.md`
- `templates/internal_escalation.md`

## 2. Do the work

先说清你**选了哪条路**、**用了哪些文件** —— 一行就够，让用户能便宜地纠正你。

缺必要输入时，写占位符并列在 `Assumptions or missing inputs:` 下面 —— **不要编。**

## 3. Check before delivering

说清你假设了什么、什么没能核实、什么还开着。
