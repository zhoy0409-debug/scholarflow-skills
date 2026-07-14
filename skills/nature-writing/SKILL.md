---
name: nature-writing
description: Draft and revise research manuscripts by building section function, evidence chains, conservative claims, citation support, and journal-appropriate academic prose.
---

# Manuscript Drafting — Router

**Do not answer from memory, and do not answer from this file.**
The actual logic lives in `static/` and `references/`. This file only decides
which fragments to load for the request in front of you. Loading them is not optional.

## Routing protocol

### 1. Load the core layer

Read [manifest.yaml](manifest.yaml). Then Read **every** file it lists under `always_load`:

- `../_shared/core/reader-workflow.md`
- `../_shared/core/paper-type-taxonomy.md`
- `../_shared/core/ethics.md`
- `../_shared/core/terminology-ledger.md`
- `static/core/stance.md`
- `static/core/workflow.md`
- `static/core/output-format.md`

These carry the default stance, workflow, and output format for every job in this skill.

### 2. Detect the axes

The manifest declares these axes. Decide a value for each from the user's input:

- **`paper_type`** — `research` / `methods` / `hypothesis` / `algorithmic` / `review` · default `research`
- **`section`** — `abstract` / `intro` / `related-work` / `method` / `experiments` / `discussion` / `conclusion` / `title`
- **`language`** — `en` / `zh-to-en` · default `en`
- **`journal`** — `nature` / `nat-comms` / `generic` · default `generic`

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

- Read `../_shared/core/claim-ledger.md` — 无出处的断言不许进正文；certainty 必须是受控枚举
- Read `../_shared/core/integrity-gates.md` — 数据来源红旗（mock 文件名、零缺失）+ 原始实验数据自洽红旗
- Read `../_shared/core/narrative-advance.md` — 冗余矩阵：每一页/每一段只准推进一步

The repo ships an executable version of these checks:

```bash
python3 gates/gate_checks.py claims    --claims c.csv --evidence e.csv --manuscript draft.md
python3 gates/gate_checks.py data      --file raw.xlsx
python3 gates/gate_checks.py narrative --matrix slides.csv
```

Exit code 2 means a BLOCK fired. Run them when the artefacts exist.
