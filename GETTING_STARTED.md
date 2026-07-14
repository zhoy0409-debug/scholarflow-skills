# Getting Started

Install only the skill that matches the work in front of you. Each directory in [`skills/`](skills/) is self-contained.

## 1. Choose a journal

Use `journal-selection-advisor` when the target venue is uncertain or when the manuscript may be over- or under-positioned.

Provide a title and abstract when available. Add your field, article type, institutional rules, desired JCR/CAS tier, deadline, budget, and any journals you must avoid. The output distinguishes realistic stretch options from safer targets.

## 2. Prepare a submission

Use `journal-submission-normalizer` after a target journal is selected.

Provide the manuscript and journal name. The skill retrieves current official instructions, creates a rule matrix, normalizes only verified requirements, and flags requirements that still need a human decision.

## 3. Improve a figure

Use `polish-sci-figures` with source data or the plotting script whenever possible.

State whether the output is for a manuscript, presentation, or public showcase. Public showcases are checked at 1200 px wide, omit panel letters by default, and keep captions and provenance outside the image.

## 4. Audit research integrity

Use `research-integrity-guardrail` before a major revision, submission, defence, or public release.

Provide the manuscript plus tables, figures, reference list, and raw calculations when they are available. The skill returns findings first; it does not conceal uncertainty or rewrite unsupported claims into smoother language.
