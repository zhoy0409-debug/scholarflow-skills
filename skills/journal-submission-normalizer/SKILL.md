---
name: journal-submission-normalizer
description: Use when a researcher needs a manuscript checked and normalized against a target journal's official submission and formatting requirements, with a compliance report before submission.
---

# Journal Submission Normalizer

Normalize a manuscript to the official requirements of a target journal before submission.

This skill is designed for the detail work that often causes avoidable submission delays: formatting rules scattered across author instructions, PDF templates, style files, submission-system checklists, and publisher pages.

## Core Principle

Submission formatting should be evidence-based:

- use official journal sources first;
- extract rules into a visible matrix before editing;
- separate verified rules from uncertain or missing rules;
- preserve scientific meaning while changing formatting;
- return both the normalized manuscript and a compliance report.

## Reference

Load `references/official-source-playbook.md` when searching for author instructions, templates, journal policies, or submission-system requirements.

## Workflow

### 1. Confirm scope

Collect:

- target journal name and publisher;
- manuscript file format: DOCX, LaTeX, Markdown, PDF-derived text, or mixed files;
- article type: original research, review, case report, meta-analysis, short communication, letter, methods, protocol, etc.;
- submission stage: initial submission, revised submission, final production, or resubmission;
- required output format: edited DOCX, LaTeX patch, Markdown checklist, or compliance report only.

If the target journal is not confirmed, ask the user to choose one before applying journal-specific formatting.

### 2. Search official requirements

Use current online sources and prioritize:

1. official journal author instructions;
2. publisher submission guidelines;
3. official article templates, style files, or sample manuscripts;
4. submission-system checklists;
5. official reference-style examples;
6. official ethics, data, funding, conflict-of-interest, and AI-use policies.

Do not rely on third-party summaries unless official sources are unavailable, and label third-party information as unverified.

### 3. Extract a rule matrix

Before editing, build a rule matrix covering:

- article type and word limits;
- title page fields;
- abstract type, length, and structure;
- keywords;
- font, font size, line spacing, margins, page numbering;
- heading levels and numbering;
- figure size, resolution, file format, color mode, and caption rules;
- table formatting and footnotes;
- abbreviations, units, symbols, superscripts, and subscripts;
- reference style, citation style, DOI/PMID requirements, maximum references;
- ethics approval, consent, trial registration, data availability, funding, author contributions, competing interests, acknowledgements, and AI-use statement;
- cover letter, highlights, graphical abstract, supplementary files, file naming, and submission checklist.

Mark each item as:

- `verified`;
- `not specified`;
- `conflicting sources`;
- `needs user confirmation`.

### 4. Normalize the manuscript

Apply only changes that are supported by the rule matrix or by standard scholarly formatting norms when the journal is silent.

Typical operations:

- normalize title page order and required fields;
- adjust heading hierarchy;
- standardize abstract and keyword formatting;
- normalize font, spacing, paragraph style, and page numbering;
- standardize figure and table callouts;
- check captions and legends;
- fix obvious superscript/subscript formatting issues without changing scientific meaning;
- align reference and citation style as far as possible from available metadata;
- add or flag required declarations;
- prepare a submission file checklist.

For DOCX, preserve track changes only if the user asks. For LaTeX, prefer a patch or edited source files. For PDF-only input, state that formatting edits require a source file.

### 5. Produce a compliance report

Return a clear report with:

1. sources consulted;
2. extracted rule matrix;
3. changes made;
4. unresolved requirements;
5. user confirmations needed;
6. final submission checklist.

## Output Contract

Return one or more of:

- normalized manuscript file or patch;
- rule matrix;
- compliance report;
- unresolved issue list;
- final submission checklist.

## Guardrails

- Do not invent journal rules.
- Do not silently change scientific meaning, results, units, author list, affiliations, ethics statements, or references.
- Do not fabricate missing metadata such as DOI, funding number, ethics approval, trial registration, or author contribution.
- Do not claim the manuscript is accepted or guaranteed submission-ready; say it is formatted against the checked rules.
- If official requirements conflict, show the conflict and ask the user or use the most journal-specific current source.
