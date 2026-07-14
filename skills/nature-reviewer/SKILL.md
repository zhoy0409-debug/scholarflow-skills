---
name: nature-reviewer
description: >-
  Act as a referee and judge the science: novelty, significance, evidence chain, technical
  soundness, and whether the claims are actually supported. Returns reviewer reports and an accept
  / revise / reject verdict. Not for: mechanical errors — numbers that disagree between abstract
  and tables, broken figure cross-references, references cited but not listed →
  research-integrity-guardrail. Not for: writing a reply to reviewers who already reviewed you →
  nature-response. 触发：模拟审稿、审稿人视角、预审、投稿前看看有什么问题、创新性够吗、能发子刊吗、证据链站得住吗。 Triggers: mock peer review,
  referee report, review my manuscript, novelty assessment, is this defensible.
---

# Referee Simulation — Router

**Do not answer from memory, and do not answer from this file.**
The actual logic lives in `references/`. Load what the request needs before you start.

## Routing protocol

### 1. Pick the references this request needs

- `references/editorial criteria and processes.md`
- `references/qa-checklist.md`
- `references/report-structure.md`
- `references/review-axes.md`
- `references/reviewer-workflow.md`
- `references/role-boundaries.md`
- `references/source-basis.md`

Read the ones that apply. Read all of them only if the request is genuinely broad.

### 2. Do the work

Ask only the questions that would otherwise send you down the wrong route.
If required input is missing, write a placeholder and list it under
`Assumptions or missing inputs:` — **do not invent it.**

### 3. Check before delivering

Say what you assumed, what you could not verify, and what is still open.

## Gates — BLOCK, not advice

These are not suggestions. If a gate fails, **fix it and re-run; do not deliver.**

- Read `../_shared/core/integrity-gates.md` — 数据来源红旗（mock 文件名、零缺失）+ 原始实验数据自洽红旗
- Read `../_shared/core/narrative-advance.md` — 冗余矩阵：每一页/每一段只准推进一步

The repo ships an executable version of these checks:

```bash
python3 gates/gate_checks.py claims    --claims c.csv --evidence e.csv --manuscript draft.md
python3 gates/gate_checks.py data      --file raw.xlsx
python3 gates/gate_checks.py narrative --matrix slides.csv
```

Exit code 2 means a BLOCK fired. Run them when the artefacts exist.
