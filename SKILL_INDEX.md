# ScholarFlow Skill Index

ScholarFlow v2.2 contains 16 public skills. Each folder below is a complete,
installable public entry point.

## ScholarFlow Core

| Skill | Primary use | Key output |
| --- | --- | --- |
| [`bioinformatics-workbench`](skills/bioinformatics-workbench/) | Reproducible omics analysis planning | Workflow contract, QC gates, analysis plan, and methods outline |
| [`journal-selection-advisor`](skills/journal-selection-advisor/) | Journal fit, tier calibration, institutional constraints, and submission strategy | Tiered journal shortlist with rationale and next steps |
| [`journal-submission-normalizer`](skills/journal-submission-normalizer/) | Official author-instruction retrieval and submission-format normalization | Rule matrix, normalized files where possible, and a compliance report |
| [`polish-sci-figures`](skills/polish-sci-figures/) | Scientific figure creation, redrawing, layout, and QA | Publication, presentation, or showcase-ready figure package |
| [`research-integrity-guardrail`](skills/research-integrity-guardrail/) | Evidence, numeric, citation, and reproducibility audit | Prioritized integrity findings and an evidence ledger |

## Evidence and Manuscripts

| Skill | Primary use |
| --- | --- |
| [`scholarflow-literature-search`](skills/scholarflow-literature-search/) | Traceable literature searches, evidence screening, and citation verification |
| [`scholarflow-literature-monitor`](skills/scholarflow-literature-monitor/) | Bounded recurring monitoring, screening, synthesis, and gap tracking |
| [`scholarflow-citation-review`](skills/scholarflow-citation-review/) | Citation metadata, claim support, and reference-list review |
| [`scholarflow-manuscript-studio`](skills/scholarflow-manuscript-studio/) | One integrated workflow for manuscript intake, evidence, drafting, revision, translation, and final audit |
| [`scholarflow-experiment-log`](skills/scholarflow-experiment-log/) | Structured experiment records, anomaly tracking, and handoff notes |
| [`scholarflow-proposal-writer`](skills/scholarflow-proposal-writer/) | Research proposal structure, rationale, and evaluation readiness |
| [`scholarflow-review-response`](skills/scholarflow-review-response/) | Point-by-point reviewer response with evidence-aware revision tracking |

## Delivery and Rendering

| Skill | Primary use |
| --- | --- |
| [`scholarflow-delivery-qa`](skills/scholarflow-delivery-qa/) | Stage, render, and inspect final artifacts before delivery |
| [`scholarflow-report-pdf`](skills/scholarflow-report-pdf/) | Build Markdown and Mermaid reports as verified PDFs |
| [`scholarflow-pdf-qa`](skills/scholarflow-pdf-qa/) | Create, inspect, and visually validate PDFs |
| [`scholarflow-research-slides`](skills/scholarflow-research-slides/) | Design editable research presentation slides |

`scholarflow-manuscript-studio` includes internal components in `modules/`.
They are workflow stages, not separately installed public skills.
