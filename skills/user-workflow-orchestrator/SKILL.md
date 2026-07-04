---
name: user-workflow-orchestrator
description: Use when the user asks Codex to decide what skill/workflow they need, summarize recurring needs, handle ambiguous or cross-domain work, recover from previously poor results, plan academic/research/writing/slides/PDF/bioinformatics/code tasks, or turn a messy goal into a verified deliverable. Especially use for requests about reviewing past work, summarizing needs, choosing a personalized workflow, fixing poor results, unresolved blockers, installing skills, paper writing, Nature-style manuscripts, PPT, PDF, bioinformatics, grants, LaTeX, figures, or deliverables.
---

# User Workflow Orchestrator

Use this skill as a lightweight operating layer before choosing domain skills. Its job is to infer the user's real desired outcome, select the smallest useful workflow, preserve the user's preferences, and finish with evidence rather than vibes.

## Fast Triage

Classify the request into one primary lane:

- **Research paper lane**: literature search, Nature-style writing, citation, response letters, LaTeX, paper restructuring. Prefer `nature-*`, `paper-spine-*`, `reference-checker`, and `research-integrity-guardrail`.
- **Scientific data lane**: bioinformatics, sequencing, genome annotation, VCF/BAM/FASTQ, microbiome, phylogeny. Prefer the most specific `bio-*`, `biopython-*`, `samtools-*`, `bcftools-*`, or workflow skill.
- **Deliverable lane**: slides, PDF, Word/docs, spreadsheets, figures, handouts. Prefer plugin-backed `presentations`, `pdf`, `documents`, `spreadsheets`, `nature-figure`.
- **Product/code lane**: code changes, frontend, debugging, tests, reviews. Prefer local repo inspection, focused verification, and `impeccable` for UI.
- **Meta-work lane**: choose skills, install/update skills, make reusable workflows, summarize lessons. Prefer `skill-creator`, `skill-installer`, and this skill.

If two lanes compete, pick the lane tied to the final artifact the user will actually use. A paper-ready figure is deliverable lane plus research constraints; a biology analysis that ends in a figure is scientific data lane plus deliverable validation.

## User Profile

When the request asks for personalization, or when the right workflow is unclear, read `references/profile.md`.

Use the profile to decide:

- how much autonomy to take;
- whether to ask a clarifying question or make a conservative assumption;
- what quality bar to apply;
- which previous failure patterns to guard against.

## Operating Rules

Start by naming the likely final artifact in one sentence. Examples: "The useful output here is a reusable skill", "The useful output here is a manuscript section", "The useful output here is a corrected PPTX".

Prefer action over abstract planning. If the user asks Codex to make, fix, install, or deliver something, do the work unless a missing choice would materially change the result.

Use narrow skill stacks. Two or three skills usually beat ten. Use broad orchestrators only to route, then switch to the specific skill that owns the fragile details.

Keep a failure ledger while working:

- unresolved blocker;
- workaround used;
- quality compromise;
- validation still missing.

Before final response, convert the ledger into a short, honest status: done, verified, remaining risk.

## Common Failure Guards

For academic work:

- Verify current facts and citations with primary sources when accuracy could have changed or when exact attribution matters.
- Separate claim strength from writing polish. Do not make prose more confident than the evidence.
- Preserve the target venue's style only after understanding the scientific argument.

For slides and documents:

- Render or inspect the output when possible. Do not rely only on generated file existence.
- Check layout, text overflow, fonts, image placement, and page/slide count.
- Put user-facing deliverables in the active thread's `outputs` folder when working in a projectless Codex workspace.

For code and UI:

- Read the existing project before editing.
- Run the narrowest meaningful tests, then broader checks if shared behavior changed.
- For frontend, use browser inspection/screenshot when a local target is available.

For bioinformatics/data workflows:

- Identify input format, reference build/database, sample pairing, and expected output before running tools.
- Prefer established tools and explicit commands over ad hoc parsing.
- Record versions, parameters, and any database/date assumptions.

For skill creation:

- Use `skill-creator`.
- Initialize with the official script when creating a new skill.
- Validate with `quick_validate.py`.
- Keep `SKILL.md` concise; move personal or detailed heuristics to references.

## Final Response Shape

Be concise and concrete:

- what was chosen or built;
- where it lives, if a file was created;
- what was verified;
- what to watch next.

When summarizing the user's needs, be candid but kind. Name patterns, not flaws.
