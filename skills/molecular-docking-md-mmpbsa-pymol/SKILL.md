---
name: molecular-docking-md-mmpbsa-pymol
description: Automate small molecule-target protein docking, MD, MM-PBSA/MM-GBSA, and visualization. Default system is one or more protein receptor chains plus an organic small-molecule ligand from SDF, MOL2, PDB, PDBQT, SMILES, or docking pose. Use for AutoDock Vina docking, Meeko/RDKit/OpenBabel preparation, PLIP/ProLIF interaction analysis, Maestro-like 2D ligand interaction diagrams, PyMOL 3D publication figures, GROMACS protein-ligand MD, AmberTools/ACPYPE/GAFF ligand parameterization, gmx_MMPBSA binding-energy summaries, residue decomposition, and paper-ready CSV/PNG/SVG/PSE/PML/methods reports. Do not use by default for protein-protein, peptide, nucleic-acid, covalent docking, metal-enzyme coordination, or membrane/lipid systems unless explicitly requested.
---

# Small Molecule-Target Protein Docking, MD, MMPBSA, and Visualization

Use this skill for small molecule-target protein systems: a receptor made of one or more protein chains and an organic small-molecule ligand. The main goal is to predict, analyze, or present how the small molecule binds the target protein.

## Scope

Assume by default:

- Receptor: one or more protein chains.
- Ligand: organic small molecule in SDF, MOL2, PDB, PDBQT, SMILES, or docking-pose format.
- Main tasks: docking, interaction analysis, PyMOL 3D visualization, Maestro-like 2D ligand interaction diagrams, GROMACS MD, and gmx_MMPBSA MM-PBSA/MM-GBSA.

Do not handle by default unless the user explicitly asks and provides method-specific details:

- Protein-protein docking.
- Peptide docking.
- Nucleic-acid docking.
- Covalent docking.
- Metal-enzyme complex coordination.
- Membrane protein-lipid systems.

Warn the user when the ligand contains metals, covalent warheads, boronic acids, complex glycosides, high/multiple charges, or unusual elements. Treat routine docking and GAFF/ACPYPE parameterization as potentially unreliable for these cases.

## Operating Rules

- Use AutoDock Vina for small-molecule docking and Meeko for PDBQT preparation.
- Use RDKit/OpenBabel for ligand conversion, hydrogen addition, 3D generation from SMILES, and chemistry checks.
- Preserve user-provided ligand 3D geometry, stereochemistry, tautomer, and protonation state where possible. Generate 3D only for SMILES or when explicitly requested.
- Do not casually change tautomer or protonation states. If uncertain, flag this in metadata and the report.
- Remove ordinary crystallographic waters by default. Keep key waters, cofactors, or metal ions only when the user specifies them.
- Preserve protein chains by default. Filter chains only when the user asks.
- Use PLIP and/or ProLIF for small molecule-protein interaction detection.
- Use `scripts/render_2d_interaction_diagram.py` when the user asks for "2D interaction diagram", "Schrodinger-style figure", "Maestro-style figure", "ligand-residue 2D map", or a figure similar to `AKT-2D.png`.
- Generate Maestro-like 2D diagrams with open-source tools by default. Do not claim Schrodinger/Maestro generated the figure unless a licensed Schrodinger workflow was actually used.
- Use PyMOL open-source for 3D figures: ligand sticks, protein cartoon, residues within 5 A as sticks, hydrogen-bond distance labels, and outputs `publication_3d.png`, `publication_3d.pse`, and `scene.pml`.
- If the user asks for MM-PBSA or MM-GBSA, default to GROMACS + gmx_MMPBSA.
- Treat OpenMM only as an optional short MD or quick-test engine, not the MM-PBSA mainline.
- Parameterize small molecules with AmberTools/ACPYPE/GAFF by default. Prefer AM1-BCC charges when AmberTools supports them; document any fallback.
- Use AMBER-compatible protein force fields for MD intended for gmx_MMPBSA.
- Never describe MM-PBSA/MM-GBSA as true absolute binding free energy. Report it as approximate relative binding stability and residue-contribution support.
- Always report software versions, force field, ligand parameterization method, charge method, water model, ion concentration, simulation length, frame range, PB/GB settings, and residue decomposition settings.

## Docking Box Rules

Use this priority order:

1. If a co-crystal/reference ligand or docking pose is provided, define the box from that ligand.
2. If active-site residues are provided, define the box from residue coordinates.
3. If coordinates are provided, use those coordinates.
4. If none are provided, stop and ask for a reference ligand, pocket residues, or coordinates. Do not guess.

P2Rank/fpocket can be suggested as separate pocket-prediction aids, but predicted pockets are only hypotheses and must be reviewed.

## Default Project Layout

Each workflow run should write:

```text
results/project_name/
├── input/
├── prepared/
├── docking/
├── interactions/
│   ├── plip/
│   ├── prolif/
│   └── 2d_diagram/
├── pymol_3d/
├── gromacs_md/
├── mmpbsa/
├── figures/
├── tables/
├── logs/
└── methods/
```

## Workflow

1. Check environment:
   `python scripts/check_env.py`
2. Run the project workflow:
   `python scripts/workflow.py --project-name my_project --protein receptor.pdb --ligand ligand.sdf --reference-ligand ref_ligand.sdf --run-docking --execute`
3. Or define the docking box by residues:
   `python scripts/workflow.py --project-name my_project --protein receptor.pdb --ligand ligand.sdf --pocket-residue A:LYS179 --pocket-residue A:ASP292 --run-docking --execute`
4. Or define the docking box by coordinates:
   `python scripts/workflow.py --project-name my_project --protein receptor.pdb --ligand ligand.sdf --center X Y Z --size SX SY SZ --run-docking --execute`

After docking, `workflow.py` runs PLIP, renders the PyMOL 3D figure, renders the Maestro-like 2D interaction diagram, copies key figures to `figures/`, and generates final report files.

## Individual Commands

Prepare ligand:

`python scripts/prepare_ligand.py --ligand ligand.sdf --outdir results/project_name/prepared --resname LIG`

Prepare receptor:

`python scripts/prepare_receptor.py --receptor receptor.pdb --outdir results/project_name/prepared --keep-water-id A_HOH_501 --keep-resname HEM --keep-metals`

Run Vina:

`python scripts/run_vina.py --receptor-pdbqt prepared/receptor.pdbqt --ligand-pdbqt prepared/ligand.pdbqt --reference-ligand ref_ligand.sdf --receptor-pdb prepared/receptor_clean.pdb --outdir docking`

Render 2D diagram:

`python scripts/render_2d_interaction_diagram.py --complex docking/best_complex.pdb --ligand prepared/ligand.sdf --ligand-resname LIG --plip-dir interactions/plip --outdir interactions/2d_diagram`

Render 3D PyMOL figure:

`python scripts/render_pymol.py --complex docking/best_complex.pdb --ligand-selection "resn LIG" --outdir pymol_3d`

Prepare GROMACS complex:

`python scripts/prepare_gromacs_complex.py --protein receptor.pdb --ligand prepared/ligand.mol2 --complex docking/best_complex.pdb --outdir gromacs_md --execute`

Run GROMACS MD:

`python scripts/run_gromacs_md.py --workdir gromacs_md --execute`

Run MM-GBSA/MM-PBSA:

`python scripts/run_gmx_mmpbsa.py --mode gb --tpr gromacs_md/processed.tpr --xtc gromacs_md/processed.xtc --topol gromacs_md/topol.top --index gromacs_md/index.ndx --receptor-group Protein --ligand-group LIG --outdir mmpbsa`

## Default Outputs

Final report files:

- `tables/docking_summary.csv`
- `tables/interaction_summary.csv`
- `tables/mmpbsa_summary.csv`
- `tables/key_residue_decomposition.csv`
- `methods/methods_docking.txt`
- `methods/methods_md_mmpbsa.txt`
- `methods/figure_legend_2d_3d.txt`
- `run_report.md`

Docking outputs:

- `prepared/ligand.sdf`
- `prepared/ligand.mol2`
- `prepared/ligand.pdbqt`
- `prepared/ligand_metadata.json`
- `prepared/receptor_clean.pdb`
- `prepared/receptor.pdbqt`
- `docking/vina_poses.pdbqt`
- `docking/docking_scores.csv`
- `docking/best_complex.pdb`

Figure outputs:

- `interactions/2d_diagram/ligand_interaction_2d.png`
- `interactions/2d_diagram/ligand_interaction_2d.svg`
- `interactions/2d_diagram/ligand_interaction_2d.csv`
- `interactions/2d_diagram/ligand_interaction_2d.json`
- `pymol_3d/publication_3d.png`
- `pymol_3d/publication_3d.pse`
- `pymol_3d/scene.pml`

## GROMACS and MMPBSA

For MD and MMPBSA, assume a protein-small-molecule complex:

1. Clean target protein.
2. Prepare ligand SDF/MOL2 with hydrogens.
3. Generate ligand GAFF topology with AmberTools/ACPYPE.
4. Merge protein and ligand complex.
5. Generate `complex.gro`, `topol.top`, and `index.ndx`.
6. Run minimization, NVT, NPT, and production MD.
7. Remove PBC, center, and fit trajectory.
8. Output `processed.xtc` and `processed.tpr`.
9. Analyze RMSD, RMSF, Rg, and protein-ligand H-bonds.
10. Run gmx_MMPBSA GB, PB, or decomposition mode.
11. Output `delta G bind`, energy components, and residue decomposition.

If ligand parameterization fails, keep logs and report the exact failure point. Do not silently patch parameters.

## References

Read the reference file matching the current task:

- `references/docking.md` for small-molecule Vina docking, receptor/ligand preparation, box selection, and PLIP.
- `references/2d-interaction-diagram.md` for Maestro-like 2D ligand interaction diagrams and Schrodinger attribution rules.
- `references/gromacs-md.md` for GROMACS protein-small-molecule setup, equilibration, production, and trajectory processing.
- `references/ligand-parameterization.md` for AmberTools, ACPYPE, GAFF, charges, and topology checks.
- `references/mmpbsa.md` for gmx_MMPBSA modes, receptor/ligand groups, PB/GB settings, and interpretation limits.
- `references/pymol-style.md` for PyMOL 3D small-molecule interaction styling.
