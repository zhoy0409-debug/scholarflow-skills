---
name: bioinformatics-workbench
description: Use when a researcher needs to turn a biological question and available sequencing or omics data into a realistic, reproducible bioinformatics workflow with explicit QC gates and deliverables.
---

# ScholarFlow Bioinformatics Workbench

Use this skill when a researcher needs to decide what analysis is appropriate before running a pipeline, or needs a defensible plan for an existing dataset.

## Route By Experience

For a new researcher, collect only the essentials: biological question, organism or system, assay, available files, sample groups, expected comparison, and required deliverable. Explain any missing prerequisite in plain language.

For an experienced user, accept a study design, file inventory, reference version, tool constraints, and desired endpoint directly. Do not repeat introductory questions they have already answered.

## Identify The Analysis Lane

Choose one primary lane and name any secondary lane:

- raw reads and variants;
- bulk RNA-seq or single-cell transcriptomics;
- microbial community or metagenomics;
- genome assembly, annotation, or comparative genomics;
- epigenomic or other multi-omic profiling;
- targeted validation, statistics, or visualization.

Do not treat an assay label as sufficient evidence that the requested analysis is valid. Check replicate structure, controls, metadata, reference resources, and confounding risks first.

## Produce A Workflow Contract

Return the following in order:

1. **Decision**: the analysis lane and why it matches the question.
2. **Input inventory**: available files, required metadata, missing assets, and file-level checks.
3. **Pipeline**: ordered stages, canonical tools or methods, expected input and output for each stage, and where versions must be recorded.
4. **QC gates**: thresholds or review decisions that determine whether to continue, re-run, or stop.
5. **Statistical plan**: comparison, unit of replication, multiple-testing approach, and assumptions that need confirmation.
6. **Deliverables**: tables, figures, reproducible environment record, and a concise methods outline.
7. **Risks and next action**: the smallest action that reduces uncertainty before compute time is spent.

## Non-Negotiable Boundaries

- Never fabricate QC results, differential features, annotations, pathways, or biological conclusions.
- Never recommend a pipeline as validated without the relevant controls and input checks.
- Keep exploratory and confirmatory analyses separate.
- State when the correct next step is experimental design, more metadata, or a domain statistician rather than another command.

This skill plans and audits workflows. Execute commands only after the user supplies data, an approved environment, and the required references.
