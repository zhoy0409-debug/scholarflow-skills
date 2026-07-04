---
name: sci-figure-composer
description: Use when the user asks to compose, redesign, audit, polish, resize, align, label, or export SCI/journal manuscript figures, especially large multi-panel figures made from plots, microscopy images, diagrams, western blots, heatmaps, UMAP/tSNE, volcano plots, survival curves, workflow schematics, or mixed evidence panels. Use for figure layout problems, panel hierarchy, journal-size fitting, typography, line weights, legends, annotations, color consistency, image resolution, Illustrator/PowerPoint/PDF/SVG/TIFF handoff, and reviewer-facing figure quality. Complements nature-figure: use nature-figure for generating plots in Python/R; use this skill for arranging and auditing the full manuscript figure.
---

# SCI Figure Composer

Use this skill to turn scattered panels into a readable, submission-grade manuscript figure. The figure must communicate one scientific conclusion before it looks decorative.

## Entry Contract

Before editing or proposing layout, identify:

- the figure's one-sentence conclusion;
- the target journal or format if known;
- the available panels and their file types;
- which panel is the hero evidence;
- final export needs: editable source, PDF/SVG, TIFF, DPI, or PPT.

If the user supplies an image/PDF/PPT, inspect or render it whenever possible. If the user supplies raw plots/data and asks to generate charts, route to `nature-figure` or the relevant plotting skill first, then return here for composition.

## Composition Workflow

1. **Build the evidence order.** Arrange panels in the order a reviewer should understand the claim, not in the order the experiments were performed.
2. **Assign panel hierarchy.** Choose one hero panel, two or three supporting panels, and any secondary/detail panels. Make the hero visibly larger or more central.
3. **Choose the grid.** Use a simple asymmetric grid when evidence weight differs; use an even grid only when panels are genuinely parallel.
4. **Normalize visual language.** Harmonize fonts, axis label sizes, line weights, scale bars, color roles, legends, and statistical marks.
5. **Reduce local clutter.** Remove repeated legends, redundant titles, oversized axis text, decorative borders, and unused whitespace.
6. **Add reader scaffolding.** Use panel letters, short in-panel labels, arrows/callouts, brackets, and group labels only where they reduce cognitive load.
7. **Check export reality.** Verify the figure at final print width and at screen review size. Ensure all text is legible, panels are not compressed, and raster images meet resolution needs.

## Load References

- Read `references/layout-audit.md` when critiquing an existing figure, screenshot, PDF, PPT slide, or Illustrator-like composition.
- Read `references/rebuild-recipes.md` when proposing or implementing a new arrangement from multiple panels.

## Hard Rules

- Do not make every panel equal size by default.
- Do not use large titles above each panel; prefer short in-panel labels and a strong figure legend.
- Do not let legends, color bars, or axis labels consume more attention than the data.
- Do not mix unrelated fonts, arbitrary line weights, or inconsistent panel letter placement.
- Do not shrink text below likely journal readability just to fit more panels.
- Do not crop microscopy/blot/image panels without preserving scale bars, group labels, and scientific meaning.
- Do not invent data, statistical significance, labels, or experimental group names.

## Quality Gates

Before final delivery or advice, report:

- the figure's conclusion and whether the layout supports it;
- the panel hierarchy;
- the main readability risks;
- the export or resolution risks;
- exact changes made or recommended.

If a rendered file can be produced, inspect it visually before saying the work is done.
