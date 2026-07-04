# Ligand Parameterization Reference

Use this file for organic small-molecule topology generation for GROMACS target-protein ligand MD.

## Default

- Use AmberTools `antechamber` and `parmchk2` with GAFF/GAFF2.
- Use ACPYPE to convert Amber ligand parameters into GROMACS include topology and coordinates.
- Prefer AM1-BCC charges for routine organic ligands when supported. Record any fallback to Gasteiger or user-supplied charges.
- If the ligand contains metal atoms, covalent chemistry, boronic acids, complex glycosides, high/multiple charges, or unusual elements, warn that GAFF/ACPYPE may be unreliable and manual validation is needed.

## Checks

- Verify formal charge, protonation state, stereochemistry, atom names, and ligand residue name.
- Do not silently change tautomer or protonation state.
- Inspect missing parameters reported by `parmchk2`.
- Confirm the ligand `.itp` is included in `topol.top`.
- Confirm `[ molecules ]` contains the ligand with the correct count.
- Keep the original ligand file, intermediate mol2, frcmod, ACPYPE output, and logs.

## Reporting

Report ligand input format, residue name, net charge, charge method, GAFF version if known, AmberTools version, ACPYPE version, and manual fixes.
