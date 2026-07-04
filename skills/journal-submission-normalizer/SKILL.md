---
name: journal-submission-normalizer
description: Find official Chinese or English journal author instructions, extract submission and formatting requirements, and normalize manuscripts before submission. Use when the user asks to prepare a paper for a target journal, check journal formatting, adapt a manuscript to author guidelines, standardize font/size/line spacing/headings/tables/figures/references/declarations, or do a pre-submission academic format compliance pass for DOCX, LaTeX, Markdown, or PDF-derived manuscripts.
---

# Journal Submission Normalizer

Normalize a manuscript against the target journal's current official author instructions.

This skill does not rely on remembered journal rules. Always search the web first, extract the live requirements into a rule matrix, then edit and verify the manuscript against that matrix.

## Source Rule

Use this source hierarchy:

1. Target journal's official "Instructions for Authors", "Guide for Authors", "Submission Guidelines", "Author Guidelines", or "投稿须知/稿约".
2. Publisher-level official guide when the journal page delegates details there.
3. Discipline standard explicitly required by the journal, such as ICMJE, Vancouver, APA, AMA, IEEE, ACS, CSE, CONSORT, PRISMA, ARRIVE, STROBE, CHEERS, or GB/T 7714.
4. Recent published articles only for style clues that are not specified in official instructions. Mark these as inferred, not authoritative.

Never use blogs, templates, examples, or memory as the primary authority when official guidance is available.

## Required References

Read only the needed reference file:

- `references/official-source-playbook.md` when searching for official journal requirements.
- `references/rule-matrix-template.md` when extracting requirements and preparing the compliance report.

## Workflow

### 1. Identify the target

Collect:

- journal name, publisher, ISSN if available, language, and target article type;
- manuscript file type: DOCX, LaTeX, Markdown, PDF, or mixed files;
- target stage: initial submission, revision, final accepted manuscript, or camera-ready/proof;
- whether references are managed by Zotero, EndNote, Mendeley, BibTeX, CSL, or plain text.

If the target journal or article type is ambiguous, ask a short clarification before editing.

### 2. Search official requirements

Search in both English and Chinese when relevant. Prefer queries like:

```text
"<journal name>" "Guide for Authors"
"<journal name>" "Instructions for Authors"
"<journal name>" "submission guidelines"
"<journal name>" 投稿须知
"<journal name>" 稿约
"<journal name>" 参考文献 格式
```

Capture every official source used with URL, publisher/site owner, access date, and whether it is journal-specific or publisher-level.

### 3. Build the rule matrix

Extract rules into a matrix before editing. Include at least:

- article type and word/page limits;
- file type and upload package requirements;
- font family, font size, line spacing, margins, page size, line numbers, page numbers;
- title page, authors, affiliations, ORCID, correspondence, equal contribution;
- abstract type, abstract word limit, keywords, highlights, graphical abstract;
- heading levels and section order;
- tables, figures, figure legends, resolution, color mode, file naming, supplementary files;
- equations, units, gene/protein/species nomenclature, italics, superscripts/subscripts;
- in-text citation style, reference list order, author truncation, journal title abbreviations, DOI/URL rules;
- declarations: ethics approval, consent, competing interests, funding, author contributions, data/code availability, AI disclosure;
- Chinese-specific rules when applicable: Chinese/English title and abstract, keywords, 中图分类号, 基金项目, 作者简介, 通信作者, GB/T 7714 reference style.

Label every rule as one of:

- `explicit`: directly stated by an official source;
- `delegated`: required by an official source through another standard;
- `inferred`: inferred from published examples because no official rule was found;
- `unknown`: not found and not safe to assume.

### 4. Normalize the manuscript

Choose the edit path by file type:

- DOCX: use document editing tools. Apply styles rather than one-off formatting when possible. Preserve scientific meaning. Render/inspect if a DOCX visual QA tool is available.
- LaTeX: adjust class/template, packages, bibliography style, sectioning, figure/table environments, and front/back matter. Compile if toolchain is available.
- Markdown: normalize headings, captions, citations, declarations, and export metadata. Convert only when the user asks.
- PDF-only input: extract text and structure first; create a normalized DOCX/Markdown draft only if the user accepts possible OCR/layout limitations.

Make mechanical changes automatically when they are unambiguous: spacing, font, margins, heading order, title-page layout, declarations, reference punctuation, superscripts/subscripts, figure/table caption placement.

Do not silently rewrite scientific claims, statistics, methods, or results. If a rule requires content the manuscript lacks, insert a clearly marked placeholder or produce a blocking item for the user.

### 5. Verify compliance

Produce a submission compliance report:

- `pass`: already compliant or fixed;
- `fixed`: changed during normalization;
- `needs author`: requires missing factual content from the user;
- `unknown`: rule was not found in official sources;
- `not applicable`: rule does not apply to this article type.

Before final delivery, check:

- all official sources are cited in the report;
- every matrix rule has a status;
- reference style and in-text citation style agree;
- figure/table files and legends agree with the journal's file rules;
- declarations are present or explicitly marked as needing author input;
- no EndNote/Zotero field codes are removed unless the target journal requires plain text and the user approves.

## Output Package

Return:

- normalized manuscript file or patched project;
- submission compliance report;
- source log with official URLs and access date;
- remaining author-action checklist.

If no reliable official requirements are found, do not pretend. Provide a conservative generic formatting pass only after telling the user what could not be verified.

## Guardrails

- Do not bypass paywalls, login systems, CAPTCHAs, or journal submission portals.
- Do not invent requirements that are not found.
- Do not claim acceptance readiness; only claim formatting and submission-rule compliance.
- Do not use third-party templates or proprietary style files unless their license permits reuse.
- For high-impact or strict journals, prefer over-reporting uncertainties to making hidden assumptions.
