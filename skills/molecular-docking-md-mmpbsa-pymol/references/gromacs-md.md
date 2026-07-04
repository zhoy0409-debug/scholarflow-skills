# GROMACS MD Reference

Use this file for GROMACS target-protein organic small-molecule complex preparation, equilibration, production, and trajectory processing.

## Default Flow

1. Clean protein PDB.
2. Parameterize the organic small-molecule ligand with AmberTools/ACPYPE/GAFF.
3. Generate protein topology with an AMBER-compatible force field.
4. Merge protein and ligand coordinates.
5. Define box, solvate, add ions.
6. Build index groups and verify receptor and ligand groups.
7. Run minimization, NVT, NPT, and production.
8. Process trajectory with PBC removal, centering, and fitting.
9. Analyze RMSD, RMSF, radius of gyration, and hydrogen bonds.

## Practical Notes

- Keep raw trajectories and logs.
- Do not overwrite user data unless the user explicitly asks.
- Use `-maxwarn` only when warnings are understood and documented.
- Check temperature, pressure, density, and potential energy before interpreting production MD.
- For gmx_MMPBSA, use processed trajectories that keep receptor and ligand whole and consistently centered.
- If ligand parameterization fails, preserve all logs and report the exact failing tool and likely chemistry issue. Do not silently patch parameters.

## Method Metadata

Report GROMACS version, force field, water model, ion concentration, box type and padding, minimization criteria, thermostat, barostat, constraints, time step, simulation length, and frame sampling interval.
