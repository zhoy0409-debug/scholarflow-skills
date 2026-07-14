---
name: scholarflow-manuscript-studio
description: Use when a researcher needs an end-to-end manuscript workflow, from materials or an existing draft through evidence planning, revision, translation, formatting, and final integrity review.
---

# ScholarFlow Manuscript Studio

ScholarFlow Manuscript Studio is one integrated research-writing workflow. It
turns a draft or research materials into a traceable manuscript package without
inventing evidence, citations, data, results, or publication claims.

Install this directory as one skill. The folders in `modules/` are internal
workflow components, not separately installed skills and not competing routing
entries.

## Start With the Right Route

Choose the shortest route that fits the request:

| Need | Internal component |
|---|---|
| Establish the project, target venue, constraints, and evidence map | `modules/intake/README.md` |
| Use the optional local intake interface | `modules/ui/README.md` |
| Research a target venue, exemplars, and evidence landscape | `modules/research/README.md` |
| Build or verify a citation-support bank | `modules/citation/README.md` |
| Revise an existing manuscript | `modules/rewrite/README.md` |
| Build a manuscript from research materials | `modules/build/README.md` |
| Improve prose while preserving the scientific record | `modules/humanize/README.md` |
| Work with a LaTeX source package | `modules/latex/README.md` |
| Create or review a translation package | `modules/translate/README.md` |
| Perform the final evidence, artifact, and submission audit | `modules/audit/README.md` |

## Operating Rules

1. Begin with the user's actual task, materials, target venue, and constraints.
   When essential details are missing, use the intake component to establish
   them before drafting.
2. Treat user-provided files as the authority for results. External sources may
   inform context, structure, and citation support, but never substitute for
   missing evidence.
3. Create a source map and an explicit evidence boundary before substantial
   drafting or rewriting.
4. Confirm the controlling research motivation before expanding a full paper.
   Do not turn a narrow contribution into unsupported claims.
5. Maintain a distinction between verified facts, user decisions, inference,
   and unresolved items. Surface unresolved items rather than concealing them.
6. Run the final audit before calling a manuscript package ready for delivery.

## Command Rule

All executable utilities live in this skill's `scripts/` directory. Run a
utility from the Manuscript Studio root, for example:

```powershell
python scripts/intake_wizard.py
python scripts/revision_audit.py --help
```

The module guides explain when to use a utility and what its output means; they
are not separate installation targets.

## Delivery Standard

Return the manuscript or revision package together with the important decisions,
evidence limits, unresolved risks, and the results of the relevant final checks.
Do not represent a formatted file as submission-ready unless its target-journal
requirements and final audit have been completed.
