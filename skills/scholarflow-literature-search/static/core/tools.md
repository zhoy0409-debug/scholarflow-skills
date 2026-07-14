# Tool Availability and Shared Guidance

The default workflow does not depend on MCP. Use browser or web tools and public
source records when they are available. Never assume that a named MCP tool is
installed merely because it is described below.

## Default Source Route

Use public Crossref, PubMed, and arXiv records where appropriate. Capture the
source URL, identifier, query, search date, and any coverage limitation. Treat
abstract-only records as leads, not confirmation of detailed scientific claims.

## Optional Local MCP Tools

After the bundled optional MCP server has been installed and its tools are
visible in the active environment, these tools may be used:

| Tool | Source | Best for |
|---|---|---|
| `search_papers` | ScholarFlow local MCP | Concurrent Crossref, PubMed, and arXiv discovery |
| `get_paper_by_id` | ScholarFlow local MCP | DOI, PMID, or arXiv record lookup |
| `get_citation` | ScholarFlow local MCP | DOI-based formatted citation |
| `lookup_mesh` | ScholarFlow local MCP | MeSH term exploration |

Scopus and ScienceDirect capabilities are optional extensions of the local MCP
server. Use them only when the user has supplied authorized credentials and the
tools are visible. Do not imply that their coverage, citation counts, or access
are available without those credentials.

## Local Utility Scripts

The `scripts/` directory contains optional helpers for local conversion and
preflight work. Check their `--help` output and local dependencies before
running them. They do not register MCP tools by themselves.

## Shared Guidance

| Resource | Purpose |
|---|---|
| [Deduplication](../../references/dedup-engine.md) | Consolidate records without erasing source provenance |
| [Citation parsing](../../references/citation-parser.md) | Extract citations from supplied documents |
| [Search strategy](../../references/search-strategy.md) | Build queries, choose sources, and rank leads |
| [RIS and BibTeX](../../references/ris-bibtex-format.md) | Understand field mappings and exchange formats |
| [Format converter](../../scripts/format-converter.py) | Review the optional local converter before use |
