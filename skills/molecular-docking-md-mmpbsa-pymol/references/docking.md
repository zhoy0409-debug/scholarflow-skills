# Docking Reference

Use this file for small molecule-target protein AutoDock Vina docking, Meeko preparation, docking boxes, and PLIP/ProLIF interaction analysis.

## Inputs

- Protein receptor: one or more target-protein chains. Do not switch to protein-protein, peptide, nucleic-acid, covalent, metal-enzyme, or membrane/lipid workflows unless explicitly requested.
- Ligand: organic small molecule in SDF, MOL2, PDB, PDBQT, SMILES, or docking-pose format.
- Docking box: prefer reference ligand/docking pose, then active-site residues, then user-provided coordinates. If none are available, stop and ask; do not guess.

## Preparation

- Receptor PDBQT: remove ordinary waters by default, keep specified waters/cofactors/metals, preserve chains, then use Meeko `mk_prepare_receptor.py`.
- Ligand PDBQT: preserve supplied 3D structure where possible; generate 3D only from SMILES or explicit request. Add hydrogens, preserve chirality where possible, then use Meeko `mk_prepare_ligand.py`.
- Record ligand charge, protonation, tautomer assumptions, chiral centers, unusual chemistry warnings, and docking box coordinates.

## Vina

Default exhaustiveness is 16, default modes is 20, default energy range is 3, and seed is recorded. Save all poses and parse `REMARK VINA RESULT` lines into `docking_scores.csv`. Treat Vina scores as approximate docking scores, not measured affinities.

## PLIP

Run PLIP on a protein-ligand complex PDB after docking pose selection. Export XML/TXT if available and preserve raw output for manual checking.

## Report

Report software versions, receptor source, ligand source, preparation steps, box center and size, exhaustiveness, random seed, number of modes, and selected pose rationale.
