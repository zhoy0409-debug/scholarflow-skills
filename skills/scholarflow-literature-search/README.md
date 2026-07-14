# ScholarFlow Literature Search

ScholarFlow Literature Search is usable immediately in an agent environment
with browser or web access. It builds a traceable search record from public
sources and does not require an API key for its default workflow.

## Default Mode: No Installation Required

Use available browser or web tools to search public source records such as
Crossref, PubMed, and arXiv. Record stable identifiers, search dates, exact
queries, coverage limits, and any source-specific restrictions. This is the
supported fallback whenever a local MCP server is unavailable.

## Optional Local MCP for Claude Code

The bundled MCP server is optional. It is intended for Claude Code on macOS,
Linux, or Windows through WSL with Python 3 available. It adds local tools for
concurrent Crossref, PubMed, and arXiv search. It is not required for Codex or
for the default browser-based workflow.

From this directory, run:

```bash
bash install.sh your-email@example.org
```

The installer copies the local server to the user's data directory, installs
its Python dependencies, and registers it with the official Claude Code command
using user scope. It never changes a project `.mcp.json` file.

Verify the installation with:

```bash
claude mcp get scholarflow-literature-search
```

If a server with that name already exists, the installer leaves it untouched.
Remove or update it explicitly with the Claude Code MCP commands before running
the installer again.

## Optional Provider Credentials

Crossref, PubMed, and arXiv are the default public sources. Scopus and
ScienceDirect are optional and require credentials that the user is authorized
to use. Keep provider keys in local environment variables or the MCP server's
local configuration; do not commit them to a project or release archive.

The user's PubMed contact email is required by NCBI etiquette. An NCBI API key
is optional and can improve the rate limit for authorized use.

## Safety and Evidence Boundary

The MCP server retrieves metadata; it does not establish scientific truth.
Always verify key claims against the original source, report source coverage and
date limits, and distinguish abstract-only records from full-text assessment.
