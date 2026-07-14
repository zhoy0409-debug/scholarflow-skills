---
name: nature-academic-search
description: Run traceable academic literature searches across scholarly sources, screen evidence conservatively, and return findings that a researcher can verify.
---

# ScholarFlow Literature Search

Use this skill when the user needs scholarly evidence, not a broad web summary.

## Start With The Question

Before searching, establish the smallest useful brief:

- research question or claim to support;
- field, population, system, or intervention;
- publication window and allowed evidence types;
- whether the user needs discovery, verification, a systematic search strategy, or a citation file.

If a missing item would materially change the result, ask one focused question. Otherwise state the assumption and proceed.

## Load The Right Guidance

Read [manifest.yaml](manifest.yaml), then load every item under `always_load`.
Choose the matching `workflow` entry:

- `multi-source-search` for discovery across databases;
- `citation-verification` for checking a known paper or DOI;
- `mesh-strategy` for a reproducible PubMed-style query;
- `citation-file-mgmt` or `reference-mgmt` for a clean reference handoff.

Read only the corresponding files in `static/`. Use `references/` only when the selected workflow needs deeper source-specific guidance.

## Evidence Rules

- Prefer original studies, official databases, and publisher metadata over snippets or aggregators.
- Record a stable identifier for every included item: DOI, PMID, accession, or publisher URL.
- Separate direct evidence, background context, and unverified leads.
- Never invent a citation, bibliographic field, result, sample size, or conclusion.
- Say when an abstract-only record, paywall, date limit, or database coverage limits confidence.

## Return A Search Record

Return concise sections in this order:

1. **Search scope**: question, sources, dates, and eligibility rules.
2. **Search strategy**: exact query strings or a reproducible query template.
3. **Included evidence**: citation, identifier, why it is relevant, and evidence role.
4. **Excluded or uncertain leads**: only when it helps prevent a mistaken conclusion.
5. **Coverage limits**: what the search cannot establish.
6. **Next action**: the smallest useful follow-up, such as full-text screening or citation export.

Do not present a literature search as exhaustive unless the databases, dates, screening criteria, and stopping rule are explicit.
