---
name: nature-citation
description: Audit citations and reference lists for scholarly manuscripts, including source verification, metadata consistency, journal-style formatting, and evidence-to-claim alignment.
---

# Citation Attachment — Router

**Do not answer from memory, and do not answer from this file.**
The actual logic lives in `static/` and `references/`. This file only decides
which fragments to load for the request in front of you. Loading them is not optional.

## Routing protocol

### 1. Load the core layer

Read [manifest.yaml](manifest.yaml). Then Read **every** file it lists under `always_load`:

- `static/core/principles.md`
- `static/core/chinese-mode.md`
- `static/core/workflow.md`

These carry the default stance, workflow, and output format for every job in this skill.

### 2. Do the work

This skill has no axes. Apply the core layer directly.
If required input is missing, write a placeholder and list it under
`Assumptions or missing inputs:` — **do not invent it.**

### 3. Open `references/` only on demand

`references/` is a deep library, not a default. Opening all of it wastes the context
you need for the actual work.

The manifest's `references.on_demand` table says which file answers which question.
Consult it, then Read only that file.

## Gates — BLOCK, not advice

These are not suggestions. If a gate fails, **fix it and re-run; do not deliver.**

- Read `../_shared/core/claim-ledger.md` — 无出处的断言不许进正文；certainty 必须是受控枚举

The repo ships an executable version of these checks:

```bash
python3 gates/gate_checks.py claims    --claims c.csv --evidence e.csv --manuscript draft.md
python3 gates/gate_checks.py data      --file raw.xlsx
python3 gates/gate_checks.py narrative --matrix slides.csv
```

Exit code 2 means a BLOCK fired. Run them when the artefacts exist.
