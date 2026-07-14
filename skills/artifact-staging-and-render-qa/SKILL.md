---
name: artifact-staging-and-render-qa
description: Stage external files into a writable workspace, normalize fragile paths, check local toolchain readiness, and render-verify deliverables before handoff. Use when users provide files on F:/Downloads/Desktop or other non-workspace paths, when Chinese or shell-fragile paths may break scripts, or when document/figure/data tasks require safe mirrored copies plus output QA.
---

# Artifact Staging And Render QA

1. Inventory every input artifact.
   Classify each item as source original, working copy, generated output, or reference-only material.

2. Preserve originals.
   Copy editable inputs into the current writable workspace before any modification.

3. Create an ASCII-safe alias when the original path is likely to break tools.
   Do this for non-ASCII paths, shell-fragile names, or mixed toolchains that already showed encoding issues.

4. Record path mapping.
   Keep track of original path, staged working path, and final output path.

5. Check the minimum viable toolchain early.
   Confirm the exact editor, runtime, or CLI needed for the task before substantive edits.

6. Perform all edits and analysis on the staged copy only.

7. Render-verify before handoff.
   Prefer reopened files, PDF export, screenshots, or other rendered checks over trusting raw edits.

8. Report separately:
   - content changes
   - staging or toolchain workarounds
   - unresolved path, permission, or render limits

## Guardrails

- Never overwrite an external original unless the user explicitly asks.
- Prefer reversible copies over in-place edits.
- Treat encoding failures as path or toolchain problems first.
- If render QA fails, state that explicitly and do not imply the output is submission-ready.

## Verification

- Confirm every edited artifact opens from the final path.
- Confirm critical formatting, references, figure/table placement, and page flow on rendered output when relevant.
- Confirm the final response names the exact deliverable paths and whether originals were left untouched.
