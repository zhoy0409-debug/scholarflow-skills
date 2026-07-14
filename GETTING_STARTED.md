# Getting Started with ScholarFlow Skills

This guide helps new users choose, install, and invoke ScholarFlow Skills without reading the whole repository first.

## Install

Copy the skill folders you need into your Agent skills directory.

Common locations:

```text
~/.codex/skills/
~/.claude/skills/
```

Each skill is an independent folder with at least:

```text
skill-name/
  SKILL.md
  agents/openai.yaml
```

More complex skills may also include:

```text
references/
scripts/
assets/
```

## Choose a Skill

Start from the task, not from the full list.

| What you want to do | Start with |
|---|---|
| Search literature, build a review, or verify citations | `nature-academic-search`, `reference-checker` |
| Read papers deeply and preserve figure logic | `nature-reader` |
| Draft, revise, or polish a manuscript | `nature-writing`, `nature-polishing`, `paper-spine` |
| Select a journal or normalize submission formatting | `journal-selection-advisor`, `journal-submission-normalizer` |
| Pre-submission: **is the science defensible?** | `nature-reviewer` |
| Pre-submission: **do the numbers and cross-references hold up?** | `research-integrity-guardrail` + `gates/` |
| Build scientific figures | `nature-figure`, `sci-figure-composer` |
| Prepare journal club or research slides | `nature-paper2ppt`, `ppt` |
| Run bioinformatics or omics workflows | `bio-*` (130 skills), `samtools-bam-processing`, `bcftools-variant-manipulation` |
| Convert or clean PDF, DOCX, PPTX, XLSX, and Markdown deliverables | `pdf`, `local-md-mermaid-pdf`, `ppt`, `chinese-docx-reference-unifier` |
| Write or audit your own skill | `skill-writing-guide`, `securityauditor` |
| Keep long tasks from losing context | `planning-with-files`, `session-handoff` |

## Starter Prompts

### Journal Selection

```text
Use journal-selection-advisor to help me choose target journals. First assess my manuscript field and article type, then factor in my goals, institutional requirements, JCR/CAS targets, timeline, and APC limits. Return Reach/Target/Safe/Fallback tiers and a recommended submission sequence.
```

### Deep Paper Reading

```text
Use the nature-reader workflow to read this paper. Produce a structured deep-reading note that preserves figure logic, core contribution, methods, evidence chain, and reusable citation points.
```

### Manuscript Writing

```text
Turn these results and figures into Results and Discussion sections. Build the argument first, then draft the text.
```

### Pre-Submission Check

```text
Run a pre-submission quality check on this manuscript. Focus on citation reliability, overclaiming, result consistency, AI-writing traces, and likely reviewer risks.
```

### Journal Formatting

```text
Use journal-submission-normalizer to search the target journal's official author instructions, extract formatting rules, normalize the manuscript for font, font size, line spacing, headings, figures, tables, superscripts/subscripts, references, and declarations, then return a compliance report.
```

### Scientific Figure Building

```text
Use the nature-figure workflow for this figure. First confirm the core conclusion, evidence chain, panel structure, statistics, and export format, then start the implementation.
```

### Bioinformatics Analysis

```text
I have sequencing data and need variant analysis that can be written into a manuscript. Start with the complete workflow, QC checkpoints, key parameters, and interpretation framework.
```

### Slide Delivery

```text
Turn this paper into a journal-club slide deck. Preserve the research question, methods, key figures, main conclusions, and discussion questions.
```

## What a Good Result Looks Like

A mature skill should not only answer the request. It should also provide:

- stage assessment
- required inputs
- execution steps
- output files or reports
- quality checks
- risk boundaries
- next-step recommendations

For example, `reference-checker` should not merely say citations look fine. It should check titles, authors, journals, years, DOI, PubMed, Crossref, publisher records, and formatting consistency.

`nature-figure` should not merely draw a plot. It should first confirm the core conclusion, evidence logic, statistical annotations, panel structure, and export requirements.

`paper-spine` should not merely polish sentences. It should first build motivation, evidence, state of the art, section function, and citation support.

## How to Ask

The best requests include the goal, source materials, and desired deliverable.

```text
Goal: pre-submission check
Materials: main.docx and references.docx
Deliverable: issue list + priority levels + directly actionable revision suggestions
```

Another example:

```text
Goal: turn a paper into a 15-slide journal-club deck
Materials: paper.pdf
Deliverable: editable PPTX with speaker logic and key figures preserved
```

## Safety Boundaries

- Literature downloading should only use content the user is authorized to access.
- Citations and factual claims must be marked as uncertain when they cannot be verified.
- File deletion, overwrite, and external writes require user confirmation.
- External software, network scripts, and high-privilege operations should be reviewed with `securityauditor`.
- Research results, statistical conclusions, and experimental data are grounded in user-provided materials.
