#!/usr/bin/env python3
"""Create final tables, methods text, legends, and run report for a small-molecule protein project."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
from pathlib import Path


def copy_or_header(src: Path, dst: Path, header: list[str]) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.exists():
        shutil.copy2(src, dst)
        return
    with dst.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)


def merge_interactions(project_dir: Path, output: Path) -> None:
    candidates = [
        project_dir / "interactions" / "2d_diagram" / "ligand_interaction_2d.csv",
        project_dir / "interactions" / "prolif" / "prolif_interactions.csv",
    ]
    rows: list[dict[str, str]] = []
    fields: list[str] = []
    for candidate in candidates:
        if not candidate.exists():
            continue
        with candidate.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames:
                for name in reader.fieldnames:
                    if name not in fields:
                        fields.append(name)
            rows.extend(dict(row) for row in reader)
    if not fields:
        fields = ["residue", "interaction_type", "distance", "source"]
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_methods(project_dir: Path, project_name: str) -> None:
    methods = project_dir / "methods"
    methods.mkdir(parents=True, exist_ok=True)
    docking_box = project_dir / "docking" / "docking_box.json"
    ligand_meta = project_dir / "prepared" / "ligand_metadata.json"
    receptor_meta = project_dir / "prepared" / "receptor_metadata.json"
    docking_text = [
        f"Project: {project_name}",
        "Default system: small molecule-target protein docking.",
        "Receptor was treated as one or more protein chains. Ordinary crystallographic waters were removed unless explicitly kept.",
        "Ligand was treated as an organic small molecule. Input 3D conformation, stereochemistry, tautomer, and protonation were preserved where possible.",
        "AutoDock Vina docking was performed with recorded box coordinates, exhaustiveness, number of modes, energy range, and seed.",
        "The lowest Vina affinity pose was selected as the default best pose, but interaction plausibility should be inspected.",
    ]
    for label, path in [("Docking box", docking_box), ("Ligand metadata", ligand_meta), ("Receptor metadata", receptor_meta)]:
        if path.exists():
            docking_text.append(f"{label}: {path}")
    (methods / "methods_docking.txt").write_text("\n".join(docking_text) + "\n", encoding="utf-8")

    md_text = [
        f"Project: {project_name}",
        "Default MD system: protein-small-molecule complex.",
        "GROMACS is the default MD engine. Protein force fields should be AMBER compatible.",
        "Small-molecule ligand parameters are generated with AmberTools/ACPYPE/GAFF by default.",
        "gmx_MMPBSA is the default MM-PBSA/MM-GBSA engine.",
        "MM-PBSA/MM-GBSA values are approximate relative binding-stability estimates and residue-contribution support; they are not true absolute experimental binding free energies.",
        "Report force field, ligand charge method, water model, ion concentration, simulation length, frame range, PB/GB settings, and residue decomposition settings.",
    ]
    (methods / "methods_md_mmpbsa.txt").write_text("\n".join(md_text) + "\n", encoding="utf-8")

    legend = [
        "2D ligand interaction diagram: Maestro-like open-source rendering centered on the small-molecule 2D structure, with interacting target-protein residues shown as colored bubbles by residue class. This figure should not be described as Schrodinger/Maestro output unless a licensed Schrodinger workflow was actually used.",
        "3D PyMOL figure: target protein is shown as cartoon, ligand as sticks, residues within 5 A as sticks, and polar contacts are shown with distance labels.",
    ]
    (methods / "figure_legend_2d_3d.txt").write_text("\n".join(legend) + "\n", encoding="utf-8")


def write_run_report(project_dir: Path, project_name: str) -> None:
    report = [
        f"# Run Report: {project_name}",
        "",
        "Default application: small molecule-target protein docking / MD / MM-PBSA / visualization.",
        "",
        "## Key outputs",
        "",
        "- `tables/docking_summary.csv`",
        "- `tables/interaction_summary.csv`",
        "- `tables/mmpbsa_summary.csv`",
        "- `tables/key_residue_decomposition.csv`",
        "- `pymol_3d/publication_3d.png`",
        "- `pymol_3d/publication_3d.pse`",
        "- `pymol_3d/scene.pml`",
        "- `interactions/2d_diagram/ligand_interaction_2d.png`",
        "- `interactions/2d_diagram/ligand_interaction_2d.svg`",
        "",
        "## Interpretation cautions",
        "",
        "- Vina scores are docking scores, not measured binding affinities.",
        "- The default best pose is the lowest-affinity Vina pose, but interaction plausibility should be checked.",
        "- MM-PBSA/MM-GBSA results are approximate relative stability and residue-contribution estimates, not true absolute binding free energies.",
        "- Ligands with metals, covalent warheads, boronic acids, complex glycosides, high charge, or unusual elements need manual parameter validation.",
    ]
    (project_dir / "run_report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-dir", required=True, type=Path)
    parser.add_argument("--project-name", default="project")
    args = parser.parse_args()

    project_dir = args.project_dir
    tables = project_dir / "tables"
    tables.mkdir(parents=True, exist_ok=True)
    copy_or_header(project_dir / "docking" / "docking_scores.csv", tables / "docking_summary.csv", ["pose", "affinity_kcal_mol", "rmsd_lb", "rmsd_ub", "selection_note"])
    merge_interactions(project_dir, tables / "interaction_summary.csv")
    copy_or_header(project_dir / "mmpbsa" / "summary_mmpbsa.csv", tables / "mmpbsa_summary.csv", ["section", "component", "value_kcal_mol", "std_kcal_mol"])
    copy_or_header(project_dir / "mmpbsa" / "per_residue_decomposition.csv", tables / "key_residue_decomposition.csv", ["residue", "total"])
    write_methods(project_dir, args.project_name)
    write_run_report(project_dir, args.project_name)
    print(f"Final report: {project_dir / 'run_report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
