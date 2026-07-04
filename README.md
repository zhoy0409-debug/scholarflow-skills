# ScholarFlow Skills

ScholarFlow Skills is a research-focused Agent Skills collection created and maintained by Zhoy.

I built it because research work is often slowed down not by one impossible task, but by having to explain the same context, workflow, standards, and boundaries to AI again and again. Literature search, paper reading, manuscript writing, figures, bioinformatics, slides, PDFs, Word formatting, journal selection, and submission checks all contain small rules that decide whether the output is actually usable.

ScholarFlow Skills turns those repeated research workflows into reusable Agent Skills. It is not a loose prompt list. Each skill is designed to clarify the use case, required inputs, execution workflow, expected deliverable, and conservative boundaries.

This repository publishes Zhoy's own workflow design and curated implementations. External software, databases, journal platforms, and online services may be called from the user's environment, but they are not distributed as part of this product and are not claimed as ScholarFlow assets.

## Contents

- [Why this is not just another skill list](#why-this-is-not-just-another-skill-list)
- [Who this is for](#who-this-is-for)
- [Core workflows](#core-workflows)
- [Example prompts](#example-prompts)
- [Installation](#installation)
- [Repository layout](#repository-layout)
- [Boundaries](#boundaries)
- [License](#license)

## Why this is not just another skill list

There are already many general skill repositories, cross-agent formats, generators, installers, and validators. They are useful infrastructure.

ScholarFlow Skills focuses on a narrower problem: how research users can bring AI into literature review, manuscript writing, journal selection, submission formatting, scientific figures, bioinformatics, and research deliverables without re-explaining the workflow every time.

The value is not the number of entries. The value is whether a skill answers the questions that decide real research usability:

- Where does this task usually fail in an actual research workflow?
- What must the user provide so the AI does not invent missing facts?
- What output format can continue into a paper, presentation, submission package, or analysis report?
- Which boundaries must stay conservative: citations, statistics, copyright, file edits, journal rules, and external tools?

ScholarFlow Skills does not rebrand mature open-source software, databases, or journal platforms as its own capability. For example, bioinformatics workflows may call tools such as `fastp`, `samtools`, `bcftools`, `BLAST`, `KEGG`, or `NCBI` resources from the user's environment. ScholarFlow's value is the reusable research workflow around those tools: when to use them, how to structure inputs and outputs, how to inspect quality-control checkpoints, how to interpret results, and how to write them into a manuscript.

## Who this is for

ScholarFlow Skills is useful when your research work repeatedly runs into the same friction:

- You read many papers, but the information that should enter the Introduction, Discussion, or review section is not systematically captured.
- You want AI help with manuscript writing, but you worry about overclaiming, weak evidence chains, inaccurate citations, or generic academic tone.
- Scientific figures take too much time because panel logic, statistical annotation, color consistency, export settings, and journal expectations have to be restated every time.
- Bioinformatics analysis finishes, but QC, parameters, results, interpretation, and manuscript language do not naturally connect.
- Slides, PDFs, Word files, Markdown notes, references, and figure assets pile up at the final stage.
- Long AI sessions lose context, and a workflow that was already clarified has to be rebuilt in the next conversation.

The goal is simple: turn repeated explanation into stable reuse.

## Core workflows

| Workflow | Research pain point | Representative skills |
|---|---|---|
| Literature search and deep reading | Turn keywords, PDFs, and database results into usable evidence | `nature-academic-search`, `nature-literature-pipeline`, `nature-reader`, `zotero-lit-fetch` |
| Manuscript spine and academic writing | Build motivation, evidence chains, section functions, and conservative claims before drafting | `paper-spine`, `nature-writing`, `nature-polishing`, `manuscript-writing` |
| Journal selection, submission formatting, and integrity checks | Match the manuscript to realistic journals, verify author instructions, normalize formatting, and reduce submission risk | `journal-selection-advisor`, `journal-submission-normalizer`, `reference-checker`, `nature-citation`, `research-integrity-guardrail`, `paper-self-review` |
| Scientific figures and presentations | Make figures serve the argument before polishing panels, labels, visual style, and export formats | `nature-figure`, `sci-figure-composer`, `nature-paper2ppt`, `ppt` |
| Bioinformatics and omics workflows | Connect FASTQ, BAM, VCF, metagenomics, phylogeny, QC, and interpretation to manuscript-ready outputs | `bio-*`, `omics-analysis`, `samtools-bam-processing`, `bcftools-variant-manipulation` |
| Deliverable cleanup | Turn Markdown, PDF, PPT, DOCX, screenshots, citations, and figures into shareable deliverables | `pdf-guide`, `local-md-mermaid-pdf`, `chinese-docx-reference-unifier`, `screenshot-docs` |
| Agent workflow discipline | Keep long tasks, handoffs, file operations, security checks, and skill writing consistent | `planning-with-files`, `session-handoff`, `securityauditor`, `skill-writing-guide` |

See [SKILL_INDEX.md](SKILL_INDEX.md) for the full index, [GETTING_STARTED.md](GETTING_STARTED.md) for first use, and [QUALITY_STANDARD.md](QUALITY_STANDARD.md) for release standards.

## Example prompts

### Journal selection

```text
Use journal-selection-advisor to help me choose target journals. First assess the manuscript field and article type, then factor in my goals, institutional requirements, JCR/CAS targets, timeline, and APC limits. Return Reach/Target/Safe/Fallback tiers and a recommended submission sequence.
```

### Journal submission formatting

```text
Use journal-submission-normalizer to search the target journal's official author instructions, extract formatting rules, normalize the manuscript for font, font size, line spacing, headings, figures, tables, superscripts/subscripts, references, and declarations, then return a compliance report.
```

### Read a paper deeply

```text
Read this paper with the nature-reader workflow. Produce a bilingual deep-reading note that preserves figure logic, core contribution, methods, evidence chain, and reusable citation points.
```

### Pre-submission quality check

```text
Run a pre-submission quality check on this manuscript. Focus on citation reliability, overclaiming, result consistency, AI-writing traces, and likely reviewer risks.
```

### Turn results into a manuscript section

```text
Turn these results and figures into Results and Discussion sections. Build the argument first, then draft the text. Do not invent citations or overstate conclusions.
```

### Connect bioinformatics output to paper writing

```text
I have sequencing data and need variant analysis that can be written into a manuscript. Start with the complete workflow, QC checkpoints, key parameters, and interpretation framework.
```

## Installation

Copy the skill folders you need into your Agent skills directory.

Common locations:

```text
~/.codex/skills/
~/.claude/skills/
```

Each skill contains at least:

```text
skill-name/
+-- SKILL.md
+-- agents/
    +-- openai.yaml
```

More complex skills may also include:

```text
references/   deeper rules, templates, and checklists
scripts/      reusable scripts
assets/       images, templates, or static resources
```

## Repository layout

```text
scholarflow-skills/
+-- README.md             project overview
+-- GETTING_STARTED.md    first-use guide
+-- QUALITY_STANDARD.md   release and quality standard
+-- SKILL_INDEX.md        skill index
+-- LICENSE               open-source license
+-- skills/               installable skills
```

## Boundaries

ScholarFlow Skills is designed to improve research efficiency, not to replace research judgment.

- Literature downloading should only use content the user is authorized to access.
- Citations and factual claims must be marked as uncertain when they cannot be verified.
- Research results, statistical conclusions, and experimental data are grounded in user-provided materials.
- File deletion, overwrite, and external writes require user confirmation.
- External software, network scripts, and high-privilege operations should be reviewed with `securityauditor`.
- Statistical conclusions, mechanistic claims, clinical meaning, and journal-fit advice should stay conservative.

## License

ScholarFlow Skills' original instructions, workflow design, and documentation are released under the [MIT License](LICENSE). External software, databases, journal platforms, and services remain governed by their own licenses, terms, and access permissions.
