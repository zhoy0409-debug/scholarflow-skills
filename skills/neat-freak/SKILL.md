---
name: neat-freak
description: Clean up project state at the end of a session by reconciling documentation, memory, open tasks, file changes, and handoff notes so future work does not rot.
---

# Neat Freak — Router

会话结束时收尾：对齐文档、内存、待办、文件改动

**Do not answer from memory, and do not answer from this file.**
The actual logic lives in the files below. This router only decides which to load.
Loading them is not optional.

## 1. Load what this request needs

**References** —— 按需读，不要一次全读：

- `references/agent-paths.md`
- `references/sync-matrix.md`

## 2. Do the work

先说清你**选了哪条路**、**用了哪些文件** —— 一行就够，让用户能便宜地纠正你。

缺必要输入时，写占位符并列在 `Assumptions or missing inputs:` 下面 —— **不要编。**

## 3. Check before delivering

说清你假设了什么、什么没能核实、什么还开着。
