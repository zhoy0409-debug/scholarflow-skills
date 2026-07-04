# PyMOL Style Reference

Use this file for paper-ready 3D small molecule-target protein visualizations.

## Default Style

- White background.
- Protein cartoon in light gray or pale blue.
- Small-molecule ligand sticks in orange or magenta.
- Key residues within 5 A as sticks.
- Hydrogen bonds and polar contacts as dashed lines with distance labels.
- Distance labels with one or two decimals.
- PNG at 300-600 dpi, plus PSE and PML.

## Residue Highlighting

When MM-PBSA decomposition results are available, highlight top contributing residues by absolute contribution. Use a restrained color ramp and label only the most important residues to avoid clutter.

## Figure Hygiene

Use orthoscopic projection, antialiasing, consistent ligand orientation, and uncluttered labels. Save `publication_3d.png`, `publication_3d.pse`, and `scene.pml` for reproducibility.
