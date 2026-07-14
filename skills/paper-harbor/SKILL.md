---
name: paper-harbor
description: >-
  Batch-scrape literature metadata from CNKI / ScienceDirect via browser automation
  (DrissionPage), then bridge it into Zotero-ready form. For bulk runs against databases you are
  logged into. Not for: saving a page you already have open via the Zotero Connector →
  zotero-lit-fetch. Not for: running a topic search → nature-academic-search.
  触发：批量抓知网、批量抓ScienceDirect、爬文献题录、把检索结果整批导出。 Triggers: batch scrape CNKI, bulk-export search
  results, scrape reference metadata.
---

# Paper Harbor — Router

从授权的数据库把文献元数据抓成 Zotero 可导入的格式

**Do not answer from memory, and do not answer from this file.**
The actual logic lives in the files below. This router only decides which to load.
Loading them is not optional.

## 1. Load what this request needs

**Scripts** —— 这些是真的要跑的，不是拿来读的：

- `scripts/browser_port_check.py`
- `scripts/cnki_drission_run.py`
- `scripts/lit_download_assistant.py`
- `scripts/open_lit_browser.ps1`
- `scripts/open_zotero_setup.ps1`
- `scripts/sciencedirect_drission_run.py`
- `scripts/zotero_bridge.py`

## 2. Do the work

先说清你**选了哪条路**、**用了哪些文件** —— 一行就够，让用户能便宜地纠正你。

缺必要输入时，写占位符并列在 `Assumptions or missing inputs:` 下面 —— **不要编。**

## 3. Check before delivering

说清你假设了什么、什么没能核实、什么还开着。
