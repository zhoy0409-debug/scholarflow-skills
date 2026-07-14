---
name: nature-paper-to-patent
description: Transform research-paper content into patent-oriented drafts, including invention extraction, claims thinking, embodiment structure, figures, novelty boundaries, and review checklists.
---

# Paper → Patent — Router

**Do not answer from memory, and do not answer from this file.**
The actual logic lives in `static/` and `references/`. This file only decides
which fragments to load for the request in front of you. Loading them is not optional.

## Routing protocol

### 1. Load the core layer

Read [manifest.yaml](manifest.yaml). Then Read **every** file it lists under `always_load`:

- `static/core/principles.md`
- `static/core/workflow.md`
- `static/core/output-contract.md`

These carry the default stance, workflow, and output format for every job in this skill.

### 2. Detect the axes

The manifest declares these axes. Decide a value for each from the user's input:

- **`source_format`** — `pdf-text` / `scanned-pdf` / `pasted-text` / `mixed-project` · default `pdf-text`
- **`task_mode`** — `full-draft` / `claim-set` / `disclosure-analysis` / `paper-patent-audit` · default `full-draft`
- **`invention_type`** — `algorithm-software` / `apparatus-system` / `process-material` / `mixed` · default `algorithm-software`

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
