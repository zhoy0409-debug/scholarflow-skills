---
name: polish-sci-figures
description: Use when a researcher needs scientific figures created, redrawn, arranged, audited, or exported with readable typography, high-contrast color, non-overlapping legends, and publication-ready files.
---

# Polish Scientific Figures

Make the figure useful before making it beautiful. Establish the claim, use authoritative data, compose a deliberate layout, inspect the rendered result at its real viewing size, and only then deliver it.

## Choose the delivery mode first

Infer the mode when it is obvious; otherwise ask one question before drawing.

| Mode | Use when | Required behavior |
| --- | --- | --- |
| `manuscript` | A paper, supplement, or journal submission | Follow the target journal and manuscript conventions. Use panel labels only when the journal or manuscript needs them. Keep the figure legend outside the image. |
| `presentation` | A talk, poster, or slide deck | Follow the deck's visual system and inspect the figure after placement on its intended slide. |
| `showcase` | A GitHub gallery, product page, or standalone public image | Do not add panel letters or figure numbering by default. Keep captions, provenance, and interpretation outside the image. Optimize for immediate reading at 1200 px wide. |

Do not run manuscript or slide checks for a standalone showcase. Do not force a showcase design into a journal template.

## Establish the figure contract

Before changing code or pixels, identify the core claim, authoritative input, target mode and dimensions, intended reader, palette semantics, export formats, and whether the deliverable must be editable. Trace the file that is actually delivered or embedded; do not polish an obsolete intermediate.

Use the best available source in this order: plotting code plus data, native vector asset, then high-resolution raster. Reuse the project's existing plotting backend and visual system unless the user asks for a redesign. Default to matplotlib only when no project backend is established.

## Preserve scientific and public integrity

- Verify groups, units, sample sizes, biological versus technical replicates, statistics, and label-to-data mapping before styling.
- Never invent observations, effects, significance, labels, or missing data. Correct a scientific error from source data rather than preserving it cosmetically.
- Keep raw microscopy, blots, and structural images faithful. Preserve required scale bars and disclose meaningful image processing.
- A public "published-figure reproduction" must use a permission-clear article with accessible source data or code. Package the article citation, DOI, exact figure/panel, licence, source-data or code URL, local input copy or retrieval instruction, and reproduction command.
- Do not present an imitation of a published figure as a reproduction. Synthetic data may be used only for internal examples, with an explicit simulation label, seed, generator, and command; it does not enter the public showcase gallery.

## Visual rules that cannot be traded away

- Essential text must be readable at the final size. For a public showcase, start at 9 pt or larger in the source figure; reduce tick density or simplify the layout before shrinking text.
- Use a purposeful, high-contrast palette with stable semantic meaning. Avoid pale, low-contrast defaults when the task calls for a visually strong result. Retain a non-colour cue when colour carries critical meaning.
- Build the panel grid before plotting: aligned outer edges, equal gutters, balanced visual weight, and intentional whitespace only. Do not leave unexplained voids or cram panels into a banner.
- Keep legends in a reserved lane or outside the axes. They must never cover data, uncertainty bands, ticks, titles, or other legends. Put captions outside the image unless the user explicitly requests an in-figure caption.
- Keep text, annotations, arrows, and colorbars within a visible safety margin. Do not rely on `bbox_inches="tight"` as a generic cure for layout; it can create inconsistent crops.
- Add panel labels only where the selected mode and target convention require them. When labels are required, use `scripts/panel_labels.py` and `audit_label_alignment()`.
- Prefer the visual form that matches the claim: points plus distributions for distributions, slopes for paired samples, lollipops/forest plots for effects, heatmaps or dot plots for many features, and lines with uncertainty for time series. Do not use chart novelty as decoration.

## Produce and inspect

1. Generate from the authoritative source and export PNG plus an editable master when the source supports it.
2. Open every final image. For multiple outputs, use `scripts/make_montage.py` to inspect cross-figure typography, margins, palette, and panel rhythm.
3. Run `scripts/figure_gate.py` before delivery when a final export exists. Use `--width-mm` for the actual inserted width, `--line-art` for line drawings, `--claim-editable` when editability is promised, and `--panels` when panel-label coordinates are available.
4. Create a 1200-px-wide preview for every public showcase and inspect it. Fix unreadable text, clipping, collisions, and accidental blank space before delivery.
5. For `manuscript`, inspect at the target column width and render the real page only after the figure is embedded. For `presentation`, inspect the rendered intended slide. Use `scripts/render_doc_pages.py` when a DOCX, PPTX, or PDF exists.
6. For SVG output, run `scripts/check_svg_editability.py` when a quick editability-only check is enough; describe raster-only or partially editable output honestly.

## Acceptance gate

Do not deliver a figure with clipped content, tiny required text, legend/data overlap, caption/plot collision, inconsistent panel geometry, unsupported glyphs, accidental blank space, unverified scientific labels, or an untruthful editability claim.

For `showcase`, also block delivery unless the 1200-px preview is readable and, for a public reproduction, the provenance package is complete. For `manuscript` and `presentation`, also block delivery until the actual target placement has been checked when that container exists.

## Bundled resources

- `assets/sci_style.mplstyle`: strong readable matplotlib baseline. Override it only for a verified target requirement.
- `scripts/panel_labels.py`: use only when panel labels are required.
- `scripts/figure_gate.py`: blocks low final DPI, likely clipped raster content, fake editable SVGs, tiny SVG text, and misaligned panel-label grids.
- `scripts/make_montage.py`: use for multi-asset visual QA.
- `scripts/render_doc_pages.py`: use only after a document or slide deck exists.
- `scripts/check_svg_editability.py`: use before calling SVG output editable.
- `references/journal_specs.md`: scope and verification rules for journal-specific figure requirements.

Keep delivery folders clean: final exports, source code and data, then QA previews. Keep failed variants and debug files outside the delivery folder. Return final files first and state only material scientific, source, or editability limitations.
