# gmx_MMPBSA Reference

Use this file for MM-PBSA, MM-GBSA, and per-residue decomposition of target-protein small-molecule complexes with GROMACS trajectories.

## Required Inputs

- `-cs`: complex TPR, usually `processed.tpr`
- `-ct`: processed trajectory, usually `processed.xtc`
- `-ci`: GROMACS index file
- `-cg`: receptor and ligand groups, selected by the user or clearly identified from index group names
- `-cp`: GROMACS topology
- `-i`: GB, PB, or decomposition input file

Do not guess the ligand group. If group identity is unclear, list all index groups and ask the user.

## Modes

- GB quick screen: use `mmpbsa_gb.in`.
- PB formal calculation: use `mmpbsa_pb.in`.
- Decomposition: use `mmpbsa_decomp.in`, usually with GB first for speed.

## Interpretation

MM-PBSA/MM-GBSA values are approximate end-state estimates for protein-small-molecule complexes. They support relative binding-stability comparisons across similar systems and residue contribution hypotheses. They are not true absolute experimental binding free energies.

## Report

Report gmx_MMPBSA version, GROMACS version, trajectory frame range, interval, receptor/ligand groups, topology, PB/GB parameters, salt concentration, decomposition settings, and whether entropy was calculated.
