# 证据门禁 —— 没有证据地图，不许开写

> 来源：`evidence-driven-writing`（已并入本 skill）。
> 它和 `_shared/core/claim-ledger.md` 是同一个思想：**先立台账，再生成句子。**

## 适用

Introduction、Related Work、背景、文献综述 —— 任何**每一句都需要文献支撑**的章节。

## 硬门禁（BLOCK）

**证据地图和段落蓝图不存在之前，一个字都不许写。**

必须先有：

1. **证据地图** —— 一张表，每行一条文献：它说了什么、支持哪个论点、强度如何。
2. **段落蓝图** —— 每一段：这段要推进哪一步？用哪几条证据？

## 为什么

反过来的顺序（先写句子，再回头找引用）**天然产生无源之句**：
写得很顺、读着很像那么回事，但没人能说清它凭什么。

审稿人和查重系统盯的正是这些句子。

而且这个顺序还会产生一种更隐蔽的错误：**先有了想说的话，再去找支持它的文献** ——
这是选择性引用，是学术不端的温和版本。

## 检查

```bash
python3 gates/gate_checks.py claims --claims claims.csv --evidence evidence.csv --manuscript draft.md
```

`claims_have_sources`（无出处的断言）和 `evidence_joinable`（证据外键悬空）会 BLOCK。
