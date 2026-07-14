---
name: scholarflow-review-response
description: Use when a researcher needs reviewer responses, rebuttals, revision plans, or response tables drafted and audited with evidence-backed replies and clear manuscript-change mapping.
---

# Reviewer Response — Router

**Do not answer from memory, and do not answer from this file.**
The actual logic lives in `static/` and `references/`. This file only decides
which fragments to load for the request in front of you. Loading them is not optional.

## Routing protocol

### 1. Load the core layer

Read [manifest.yaml](manifest.yaml). Then Read **every** file it lists under `always_load`:

- `static/core/stance.md`
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
