---
name: scholarflow-citation-review
description: Use when a researcher needs citations or a reference list audited for source verification, metadata consistency, journal style, or evidence-to-claim alignment.
---

# ScholarFlow Citation Review

Use this skill to check citations already attached to a manuscript or to build a verified citation plan before drafting.

## Establish The Review Scope

Identify the manuscript language, required journal style, source format, and whether the user needs:

- a reference-list audit;
- verification of specific records;
- claim-to-evidence checking;
- formatted references for a target journal; or
- a citation plan for an unfinished section.

Ask only for information that changes the result. Do not infer a journal style from a publisher name alone.

## Load The Working Guidance

Read [manifest.yaml](manifest.yaml), then load every item under `always_load`.
Use the relevant `references.on_demand` item only when the request requires it. Do not load the entire reference library for a short audit.

## Audit In This Order

1. **Existence**: resolve DOI, PMID, publisher record, or another stable identifier.
2. **Metadata**: compare author list, title, journal, year, volume, pages, and identifier with the authoritative record.
3. **Claim support**: label each citation as direct support, contextual support, methodological precedent, or insufficient support.
4. **Placement**: make sure a reader can tell which statement the citation supports.
5. **Style**: apply the target journal's verified author instructions only after metadata is correct.

Never convert a weak, indirect, or inaccessible source into a strong claim. Flag it instead.

## Return Findings First

Use four groups:

- **Blocked**: nonexistent, unverifiable, or materially incorrect citations.
- **Needs verification**: incomplete metadata, unresolved identifiers, or inaccessible full text.
- **Evidence mismatch**: citations that do not support the surrounding claim.
- **Ready**: records that pass the requested check.

For every non-ready item, give the exact field or claim that needs attention and the conservative next action. Keep a compact evidence ledger with the source URL or identifier so the user can re-check it.
