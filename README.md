# ScholarFlow Skills

**Research workflows for the moments when AI should not guess.**

Research often stalls after the experiment: the right journal is unclear, author instructions are scattered, a figure is hard to read at real size, a citation only appears to support a claim, or an analysis plan outruns the data. ScholarFlow is Zhoy's practical toolkit for getting those decisions into a defensible, usable state.

## Start Here

These five standalone entry points cover the most common research bottlenecks.

| Need | Skill | What it delivers |
| --- | --- | --- |
| I have data but no trustworthy analysis route. | [`bioinformatics-workbench`](skills/bioinformatics-workbench/) | A reproducible analysis plan, QC gates, data requirements, statistics plan, and deliverables. |
| I do not know where my paper should go. | [`journal-selection-advisor`](skills/journal-selection-advisor/) | A guided or advanced journal-fit assessment, tiered candidates, constraints, and a defensible submission sequence. |
| My target journal's requirements are scattered everywhere. | [`journal-submission-normalizer`](skills/journal-submission-normalizer/) | A verified rule matrix, normalized files where possible, and a compliance report separating confirmed from unresolved requirements. |
| My scientific figure is technically finished but still does not persuade. | [`polish-sci-figures`](skills/polish-sci-figures/) | A readable figure for a manuscript, presentation, or public showcase, with source integrity and final-size QA. |
| I need a hard look at whether the manuscript is defensible. | [`research-integrity-guardrail`](skills/research-integrity-guardrail/) | An evidence ledger and prioritized audit of claims, numbers, citations, reproducibility, and overstatement. |

## More Than A Menu

The maintained workflow library adds 21 focused modules across the rest of the research cycle.

| Workflow | Entry point | Coverage |
| --- | --- | --- |
| Literature evidence | [`nature-academic-search`](skills/nature-academic-search/), [`nature-citation`](skills/nature-citation/), [`nature-literature-pipeline`](skills/nature-literature-pipeline/) | Search strategy, source verification, citation review, and recurring literature monitoring. |
| Manuscript Studio | [`paper-spine`](skills/paper-spine/) | Intake, evidence research, citation support, drafting, rewriting, LaTeX, translation, style review, and final audit. |
| Research lifecycle | [`nature-experiment-log`](skills/nature-experiment-log/), [`nature-proposal-writer`](skills/nature-proposal-writer/), [`nature-response`](skills/nature-response/) | Experiment records, proposal development, and point-by-point reviewer responses. |
| Research delivery | [`artifact-staging-and-render-qa`](skills/artifact-staging-and-render-qa/), [`local-md-mermaid-pdf`](skills/local-md-mermaid-pdf/), [`ppt-html-authoring`](skills/ppt-html-authoring/), [`pdf`](skills/pdf/) | Final artifact checks, diagram-to-PDF reports, presentations, and visual PDF review. |

The Manuscript Studio is an advanced bundle: install `paper-spine` together with every `paper-spine-*` directory. Its components are designed to work as one workflow, not as eleven unrelated prompts.

Experienced users can provide a manuscript, target journal, source data, or figure directly. Newer researchers are guided through only the missing context before a recommendation is made.

## Start Small

Copy a standalone skill folder into your agent's skills directory, for example `~/.codex/skills/` or `~/.claude/skills/`. For Manuscript Studio, copy the complete `paper-spine*` bundle.

Then use a plain request such as:

```text
I have paired-end RNA-seq from two treatment groups. Build a realistic analysis plan, tell me what metadata is missing, and define the QC decisions before proposing results.

Help me choose a realistic target journal for this abstract. My institution requires an original research article and I need a JCR Q2 or better journal.

Normalize this manuscript for [journal]. Use current official author instructions and give me a compliance report before changing the document.

Audit this manuscript for unsupported claims, mismatched numbers, citation gaps, and reproducibility risks. Do not rewrite the prose until the evidence problems are clear.
```

More detailed starting points are in [GETTING_STARTED.md](GETTING_STARTED.md), and every released module is listed in [SKILL_INDEX.md](SKILL_INDEX.md).

## What Good Looks Like

Public figure examples are not decorative mock data. The two images below are source-data re-renders of eLife TEA-seq Figure 3, split into readable standalone assets for online viewing.

<p align="center">
  <img src="showcase/elife-tea-seq-figure-3/figure3a-d-atlas-rerender.png" width="49%" alt="TEA-seq UMAP atlas re-render from published source data">
  <img src="showcase/elife-tea-seq-figure-3/figure3e-marker-heatmap-rerender.png" width="49%" alt="TEA-seq marker heatmap re-render from published source data">
</p>

The full provenance, licence, source-data links, and reproduction script are in [the showcase package](showcase/elife-tea-seq-figure-3/).

## Product Principles

- **Evidence before polish.** Facts, citations, statistics, journal requirements, and source data are never invented to make an output look complete.
- **A clear path for every level.** New researchers receive structured guidance; experienced researchers can start from their study design, manuscript, or analysis constraints.
- **Visible uncertainty.** Unverified rules, incomplete data, and unsupported claims are reported rather than silently filled in.
- **Public work must be attributable.** Published-figure reproductions require permission-clear sources, data or code access, and explicit attribution.
- **Maintained scope, not catalogue size.** Every public module is released and maintained as part of ScholarFlow. Referenced software, methods, and source data retain their own attribution and terms.

See [QUALITY_STANDARD.md](QUALITY_STANDARD.md) for the release bar.

## Licence

ScholarFlow workflow text and original implementation are released under the [MIT License](LICENSE). External research articles, data sources, and software remain subject to their own licences and access terms.
