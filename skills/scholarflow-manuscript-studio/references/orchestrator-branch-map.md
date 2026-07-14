# Orchestrator Branch Map

ScholarFlow Manuscript Studio is a main-orchestrator workflow plus branch skills. The orchestrator
does not perform every operation itself; it calls branch skills in a fixed
order, verifies their artifacts, and routes back when a required artifact is
weak or missing.

## Branch Order

1. `manuscript-studio-ui`: open a real terminal UI window when configuration is
   missing or incomplete.
2. `manuscript-studio-intake`: write `scholarflow_manuscript_config.json` and
   `scholarflow_manuscript_config.md`.
3. `manuscript-studio-research`: ingest local references, collect official
   requirements, learn target examples/SOTA, and propose motivation options.
4. `manuscript-studio-citation`: build `citation_support_bank.md` for literature
   statements in Introduction/Discussion/background.
5. User confirmation: write `confirmed_motivation.md` only after the user
   chooses or revises the motivation.
6. `manuscript-studio-rewrite` or `manuscript-studio-build`: produce logic maps, evidence
   banks, section blueprints, and `writing_rationale_matrix.md`.
7. `manuscript-studio-latex`: assemble final LaTeX, optional PDF, and optional Word.
8. `manuscript-studio-audit`: check artifacts, rationale depth, citation bank,
   unsupported claims, translation coverage, LaTeX, and Word output.

## Loop Rule

If a branch output fails audit, route back to that branch. Do not patch the final
paper directly when the missing artifact should have been created earlier.

Examples:

- Missing local source paths: return to `manuscript-studio-research`.
- Too few citation candidates: return to `manuscript-studio-citation`.
- Shallow writing matrix: return to `manuscript-studio-rewrite` or
  `manuscript-studio-build`.
- Broken labels/citations in LaTeX: return to `manuscript-studio-latex`.
