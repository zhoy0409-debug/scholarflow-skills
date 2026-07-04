# Rebuild Recipes

Use these recipes when designing or reworking a multi-panel SCI figure.

## Figure Blueprint

Create this compact plan before arranging panels:

```text
Conclusion:
Hero panel:
Panel groups:
Reading order:
Grid:
Shared legend/color rules:
Export target:
Known risks:
```

## Common Archetypes

### Mechanism Figure

Use when the claim is a pathway, model, or causal sequence.

Layout:

- Put a clean mechanism schematic at left or top, but keep it smaller than the strongest evidence unless the mechanism itself is the result.
- Group validation panels by step in the mechanism.
- Use arrows sparingly and consistently.
- Keep pathway colors tied to the same colors in plots.

### Phenotype Plus Mechanism

Use when the figure moves from observed effect to explanation.

Layout:

- Start with the phenotype or clinical/biological effect as the hero.
- Place molecular or cellular mechanism panels next.
- End with rescue, validation, or external cohort evidence.
- Avoid making the mechanistic schematic dominate if the quantitative phenotype is the main discovery.

### Multi-omics Summary

Use for heatmaps, volcano plots, enrichment, networks, UMAP/tSNE, and validation.

Layout:

- Put global structure first: UMAP, clustering, heatmap, or overview.
- Put differential evidence next: volcano, pathway enrichment, gene set score.
- Put validation last: qPCR, western blot, IHC, independent cohort.
- Keep color scales compact and aligned; do not repeat a color bar for every heatmap if one shared scale is valid.

### Imaging Figure

Use for microscopy, histology, immunofluorescence, or pathology panels.

Layout:

- Use image grids with matched crops and equal physical scale.
- Put quantification adjacent to the image group, not far away.
- Keep scale bars consistent and readable.
- Use row/column labels outside the image field to reduce overlay clutter.

### Method or Workflow Figure

Use when the figure explains a pipeline, screen, cohort, or experimental design.

Layout:

- Make the workflow compact and directional.
- Reserve the largest space for result panels, unless the method is the contribution.
- Use one visual grammar: boxes, arrows, icons, and labels should not compete.
- Do not over-illustrate biological objects if a simple schematic is clearer.

## Grid Patterns

### Hero Left, Evidence Right

Use when one plot/image carries the main claim.

```text
A A | B C
A A | D E
```

### Overview Top, Details Below

Use when readers need context before detail.

```text
A A A
B C D
E F G
```

### Paired Image and Quantification

Use for microscopy plus measurement.

```text
A A | B
C C | D
```

Images stay wide; quantification panels stay close.

### Sequential Evidence Strip

Use for ordered experiments.

```text
A -> B -> C
D    E    F
```

Only use arrows when the panels represent a real sequence.

## Revision Moves

When a figure feels bad, try these in order:

1. Delete redundant panel titles and repeated legends.
2. Enlarge the hero panel by 20 to 50 percent.
3. Group related panels with whitespace instead of boxes.
4. Move quantification next to the image it explains.
5. Standardize axis ranges where comparison depends on them.
6. Collapse repeated color bars or legends into one shared guide.
7. Move low-value controls to supplement if they interrupt the story.
8. Split one overfull figure into a main figure plus supplemental figure.

## Export Targets

Common starting points:

- single-column figure: about 85 to 90 mm wide;
- double-column figure: about 170 to 180 mm wide;
- readable final text: usually no smaller than 6 to 8 pt after scaling;
- line art/vector: PDF or SVG source where accepted;
- raster/photo panels: TIFF or high-resolution embedded raster, commonly 300 dpi or higher depending on journal and content.

Always check the target journal's current instructions when exact export specs matter.
