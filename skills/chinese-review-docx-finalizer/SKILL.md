---
name: chinese-review-docx-finalizer
description: Finalize Chinese-language review manuscripts in DOCX by checking structure, headings, citations, references, formatting, figure/table callouts, acknowledgements, declarations, and final delivery readiness. Use when a review article needs a pre-submission finishing pass.
---

# Chinese Review Docx Finalizer — Router

中文综述 DOCX 的定稿检查

**Do not answer from memory, and do not answer from this file.**
The actual logic lives in the files below. This router only decides which to load.
Loading them is not optional.

## 1. Load what this request needs

**Scripts** —— 这些是真的要跑的，不是拿来读的：

- `scripts/docx_review_qa.py`

## 2. Do the work

先说清你**选了哪条路**、**用了哪些文件** —— 一行就够，让用户能便宜地纠正你。

缺必要输入时，写占位符并列在 `Assumptions or missing inputs:` 下面 —— **不要编。**

## 3. Check before delivering

说清你假设了什么、什么没能核实、什么还开着。
