# Getting Started

Choose the narrowest public skill that matches the work in front of you. The five ScholarFlow Core skills are standalone. `scholarflow-manuscript-studio` is one integrated Manuscript Studio package; install that single folder when you need end-to-end writing or revision support.

## 1. Plan an analysis

Use `bioinformatics-workbench` before starting an omics or sequencing pipeline.

Provide the biological question, assay, organism or system, available files, sample groups, expected comparison, and required deliverable. The result separates missing prerequisites from analysis steps and makes QC decisions explicit.

## 2. Choose a journal

Use `journal-selection-advisor` when the target venue is uncertain or the manuscript may be over- or under-positioned.

Provide a title and abstract when available. Add your field, article type, institutional rules, desired JCR/CAS tier, deadline, budget, and any journals to avoid. The output distinguishes stretch options from safer targets.

## 3. Prepare a submission

Use `journal-submission-normalizer` after a target journal is selected.

Provide the manuscript and journal name. The skill retrieves current official instructions, creates a rule matrix, normalizes only verified requirements, and flags requirements that still need a human decision.

## 4. Improve a figure

Use `polish-sci-figures` with source data or the plotting script whenever possible.

State whether the output is for a manuscript, presentation, or public showcase. Public showcases are checked at 1200 px wide, omit panel letters by default, and keep captions and provenance outside the image.

## 5. Build or revise a manuscript

Use `scholarflow-manuscript-studio` for an end-to-end manuscript package. Provide the manuscript or materials folder, target journal, source references, and the required outcome: a new draft, a revision, a translation package, or a final audit. The skill selects its internal stages without requiring separate module installation.

Use `scholarflow-literature-search` for a focused evidence search or citation verification. Use `scholarflow-citation-review` when the evidence exists but the reference list or claim support needs an audit.

## 6. Audit research integrity

Use `research-integrity-guardrail` before a major revision, submission, defence, or public release.

Provide the manuscript plus tables, figures, reference list, and raw calculations when available. The skill returns findings first; it does not conceal uncertainty or rewrite unsupported claims into smoother language.

For the full workflow inventory, see [SKILL_INDEX.md](SKILL_INDEX.md).

## Maintenance checks

Repository checks require Python 3.10 or newer:

```powershell
python scripts/release_check.py
```

If `python` points to an older interpreter, run the same script with a Python
3.10+ executable from your agent runtime or development environment.
