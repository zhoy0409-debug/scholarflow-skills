# 2D Interaction Diagram Reference

Use this file when the user asks for a 2D interaction diagram, Schrodinger-style diagram, Maestro-style diagram, ligand-residue 2D map, or a figure similar to `AKT-2D.png`.

## Purpose

Generate a Maestro-like 2D small molecule-protein ligand interaction diagram without claiming that Schrodinger/Maestro produced the figure unless a licensed Schrodinger installation is actually used by the user.

## Default Inputs

- Best target-protein small-molecule complex PDB from docking or an MD representative frame.
- Small-molecule ligand SDF/MOL2/PDB/SMILES when available; this gives better RDKit bonding and 2D coordinates than extracting ligand from a PDB complex.
- PLIP XML/TXT or ProLIF CSV when available.

## Style

- Center the 2D ligand structure.
- Use conventional atom colors: oxygen red, nitrogen blue, sulfur yellow, halogens green.
- Draw residue bubbles around the ligand.
- Color residue bubbles by residue class:
  - Hydrophobic: light green.
  - Polar: light blue.
  - Acidic: orange.
  - Basic: blue-purple.
- Use dashed or arrowed lines for hydrogen bonds.
- Use distinct colors and line styles for pi-pi, pi-cation, hydrophobic contacts, salt bridges, halogen bonds, water bridges, and metal contacts.
- Optionally draw a pale pocket contour or hydrophobic envelope around the ligand.

## Tool Priority

1. Read PLIP XML/TXT if provided.
2. Read ProLIF CSV/JSON if provided.
3. Try ProLIF directly from a complex PDB when ProLIF and MDAnalysis are installed.
4. Fall back to residue-distance contacts from the complex PDB.

## Outputs

Always write:

- `ligand_interaction_2d.png`
- `ligand_interaction_2d.svg`
- `ligand_interaction_2d.csv`
- `ligand_interaction_2d.json`

## Reporting

State the interaction source: PLIP, ProLIF, or geometric fallback. If the figure is only Maestro-like, say so directly and do not imply commercial Schrodinger output.
