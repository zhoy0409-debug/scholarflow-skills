# ScholarFlow Skills

**Research workflows for the moments when AI should not guess.**

ScholarFlow is built by Zhoy from recurring research work: choosing a journal without overreaching, turning scattered author instructions into a usable submission checklist, making a figure readable at its real size, and checking whether a manuscript says more than its evidence supports.

This is deliberately a small collection. Each skill has a defined input, a conservative workflow, a concrete deliverable, and a boundary it will not cross.

## The Collection

| Need | Skill | What it delivers |
| --- | --- | --- |
| I do not know where my paper should go. | [`journal-selection-advisor`](skills/journal-selection-advisor/) | A guided or advanced journal-fit assessment, tiered candidates, constraints, and a defensible submission sequence. |
| I have a target journal but its requirements are scattered everywhere. | [`journal-submission-normalizer`](skills/journal-submission-normalizer/) | A verified rule matrix, normalized manuscript files where possible, and a compliance report that separates confirmed from unresolved requirements. |
| My scientific figure is technically finished but still does not look convincing. | [`polish-sci-figures`](skills/polish-sci-figures/) | A readable figure for a manuscript, presentation, or public showcase, with deliberate layout, source integrity, and final-size QA. |
| I need a hard look at whether the manuscript is internally defensible. | [`research-integrity-guardrail`](skills/research-integrity-guardrail/) | An evidence ledger and a prioritized audit of claims, numbers, citations, reproducibility, and overstatement. |

Experienced users can provide a manuscript, target journal, source data, or figure directly. Newer researchers are guided through the missing context before a recommendation is made.

## Start Small

Copy the one folder you need from [`skills/`](skills/) into your agent's skills directory, for example `~/.codex/skills/` or `~/.claude/skills/`.

Then use a plain request such as:

```text
Help me choose a realistic target journal for this abstract. My institution requires an original research article and I need a JCR Q2 or better journal.

Normalize this manuscript for [journal]. Use current official author instructions and give me a compliance report before changing the document.

Polish this figure for a public GitHub showcase. It must stay faithful to the source data, use large readable text, and keep all captions outside the image.

Audit this manuscript for unsupported claims, mismatched numbers, citation gaps, and reproducibility risks. Do not rewrite the prose until the evidence problems are clear.
```

More detailed examples are in [GETTING_STARTED.md](GETTING_STARTED.md).

## What Good Looks Like

Public figure examples are not decorative mock data. The two images below are source-data re-renders of eLife TEA-seq Figure 3, split into readable standalone assets for online viewing.

<p align="center">
  <img src="showcase/elife-tea-seq-figure-3/figure3a-d-atlas-rerender.png" width="49%" alt="TEA-seq UMAP atlas re-render from published source data">
  <img src="showcase/elife-tea-seq-figure-3/figure3e-marker-heatmap-rerender.png" width="49%" alt="TEA-seq marker heatmap re-render from published source data">
</p>

The full provenance, licence, source-data links, and reproduction script are in [the showcase package](showcase/elife-tea-seq-figure-3/).

## Product Principles

- **Evidence before polish.** Facts, citations, statistics, and source data are never invented to make an output look complete.
- **The smallest useful workflow.** A clear request should not be routed through a long questionnaire.
- **Visible uncertainty.** Unverified journal rules, incomplete data, and unsupported claims are reported rather than silently filled in.
- **Public work must be attributable.** Published-figure reproductions require permission-clear sources, data or code access, and explicit attribution.
- **No borrowed catalogue disguised as a product.** This repository contains only workflows Zhoy maintains as ScholarFlow.

See [SKILL_INDEX.md](SKILL_INDEX.md) for the complete release inventory and [QUALITY_STANDARD.md](QUALITY_STANDARD.md) for the release bar.

## Licence

ScholarFlow workflow text and original implementation are released under the [MIT License](LICENSE). External research articles, data sources, and software remain subject to their own licences and access terms.
