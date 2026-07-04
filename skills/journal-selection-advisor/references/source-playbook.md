# Source Playbook

Journal metrics and indexing status change. Always verify current information online.

## Discovery Sources

Use multiple sources because each has bias:

- Publisher journal finder tools: Elsevier Journal Finder, Springer Nature Journal and Funding Finder, Wiley Journal Finder, Taylor & Francis Journal Suggester, MDPI journal finder when relevant.
- Biomedical matching: JANE for PubMed/MEDLINE-heavy topics.
- Official journal pages: aims and scope, article types, author instructions, APC/OA, editorial policies.
- Indexing and quality: Web of Science Master Journal List, Scopus Source List, PubMed/MEDLINE/NLM Catalog, DOAJ, COPE, DOAJ seals where relevant.
- Metrics: Journal Citation Reports/JCR if accessible, CAS/中科院分区 if accessible, Scimago/SJR as supplementary context, journal official metrics pages.
- Chinese journals: journal official site, society publisher, CNKI journal page, Wanfang/VIP, CSSCI/CSCD/北大核心/科技核心 lists if available to the user.
- Risk checks: institutional warning lists, publisher policies, journal official contact/domain, retraction/ethics concerns, suspicious special issues.

## Search Queries

```text
"<manuscript keywords>" "<field>" journal
"<journal name>" aims and scope
"<journal name>" author guidelines
"<journal name>" article types
"<journal name>" APC open access
"<journal name>" Web of Science Master Journal List
"<journal name>" Scopus source
"<journal name>" PubMed NLM Catalog
"<journal name>" 中科院分区
"<journal name>" JCR Quartile
"<期刊名>" 投稿须知
"<期刊名>" 中科院分区
"<期刊名>" 预警
```

## Verification Labels

- `verified-official`: official journal/publisher/index source checked.
- `verified-database`: reputable index or directory checked.
- `user-provided`: user supplied institutional list or screenshot.
- `secondary-only`: only secondary sources found; use cautiously.
- `needs-access`: requires subscription or institutional access.
- `unknown`: not verified.

## Predatory or Poor-Fit Signals

Flag, do not automatically exclude unless evidence is strong:

- promises of unrealistically fast acceptance;
- mismatched scope or overly broad mega-special issue;
- unclear editorial board or contact domain;
- unclear indexing claims;
- fake or misleading impact factor;
- journal not found in claimed index;
- APC hidden until late stage;
- title similar to a reputable journal but different publisher;
- unit or school warning-list conflict.

## Notes on Metrics

- JCR quartile, impact factor, and CAS/中科院分区 are time-sensitive.
- If exact current values cannot be verified, say `needs verification` rather than guessing.
- For institutional decisions, the user's school/unit rule overrides generic prestige.
