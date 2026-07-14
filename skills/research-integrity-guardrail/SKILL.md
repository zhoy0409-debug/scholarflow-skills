---
name: research-integrity-guardrail
description: Use when a researcher needs manuscripts, reports, or study materials audited for unsupported claims, inconsistent numbers, citation gaps, reproducibility omissions, or overstatement.
---

# Research Integrity Guardrail

Protect the evidence chain before polishing language. This skill audits a research artifact; it does not invent evidence, conceal uncertainty, or make unsupported work sound more convincing.

## Establish the audit boundary

Identify the artifact, its audience, the claimed contribution, and the materials available for verification: manuscript, figures, tables, reference list, raw calculations, methods, code, protocol, or supplementary files. Mark any missing material as unverified rather than inferring it.

## Build an evidence ledger

For each consequential claim or result, record:

| Claim or result | Evidence location | Verification status | Required action |
| --- | --- | --- | --- |
|  | Table, figure, source, calculation, method, or code | Supported / unclear / inconsistent / unsupported |  |

Do not treat a citation as verification unless it actually supports the claim being made.

## Audit in this order

1. **Numbers and cross-references**: reconcile repeated counts, percentages, ratios, *P* values, figure labels, table values, and appendix references.
2. **Claims and citations**: locate each major claim's support; flag orphaned citations, unused references, missing close comparators, and statements stronger than their evidence.
3. **Methods and reproducibility**: check that datasets, preprocessing, exclusions, controls, parameters, statistics, code, and evaluation splits are sufficiently described for the stated result.
4. **Interpretation**: distinguish observed findings from mechanism, causality, clinical meaning, novelty, and generalization. Require limitations where they materially affect interpretation.
5. **Presentation integrity**: identify selective reporting, missing negative cases, unexplained visual choices, and claims that do not trace to a figure, table, calculation, or source.

## Return findings before revisions

Lead with material risks, ordered by severity. Separate facts from judgment:

- **Blocked**: demonstrably inconsistent, unsupported, or missing evidence.
- **Needs verification**: cannot be checked from the supplied materials.
- **Conservative rewrite needed**: evidence exists but the wording overstates it.
- **Editorial**: clarity or structure issue with no integrity implication.

Use this format:

```markdown
## Integrity Findings
1. [Blocked] Location - issue - evidence - required fix

## Evidence Ledger
| Claim or result | Evidence location | Verification status | Required action |
| --- | --- | --- | --- |

## Release Decision
- Ready items:
- Blocking items:
- Items requiring author confirmation:
```

Only after the user resolves the material risks should this skill help revise wording. For journal formatting, use `journal-submission-normalizer`; for manuscript-journal fit, use `journal-selection-advisor`; for figure QA, use `polish-sci-figures`.
