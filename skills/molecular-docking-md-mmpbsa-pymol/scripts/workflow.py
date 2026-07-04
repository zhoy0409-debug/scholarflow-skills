#!/usr/bin/env python3
"""Workflow for small molecule-target protein docking, figures, MD, and gmx_MMPBSA."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def run_step(name: str, cmd: list[str], log_file: Path, execute: bool) -> None:
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(f"\n## {name}\n")
        handle.write("$ " + " ".join(cmd) + "\n")
        if not execute:
            return
        proc = subprocess.run(cmd, text=True, stdout=handle, stderr=subprocess.STDOUT, check=False)
    if execute and proc.returncode != 0:
        raise SystemExit(f"Step failed: {name}. See {log_file}")


def make_project_dirs(project_dir: Path) -> dict[str, Path]:
    dirs = {
        "project": project_dir,
        "input": project_dir / "input",
        "prepared": project_dir / "prepared",
        "docking": project_dir / "docking",
        "interactions": project_dir / "interactions",
        "plip": project_dir / "interactions" / "plip",
        "prolif": project_dir / "interactions" / "prolif",
        "diagram2d": project_dir / "interactions" / "2d_diagram",
        "pymol3d": project_dir / "pymol_3d",
        "gromacs": project_dir / "gromacs_md",
        "mmpbsa": project_dir / "mmpbsa",
        "figures": project_dir / "figures",
        "tables": project_dir / "tables",
        "logs": project_dir / "logs",
        "methods": project_dir / "methods",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    return dirs


def copy_input(path: Path | None, input_dir: Path) -> Path | None:
    if not path:
        return None
    if not path.exists():
        return path
    target = input_dir / path.name
    if path.resolve() != target.resolve():
        shutil.copy2(path, target)
    return target


def copy_if_exists(src: Path, dst_dir: Path) -> None:
    if src.exists():
        dst_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst_dir / src.name)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protein", type=Path, help="Target protein receptor PDB.")
    parser.add_argument("--ligand", type=Path, help="Organic small-molecule ligand: sdf, mol2, pdb, pdbqt, smiles, or docking pose.")
    parser.add_argument("--smiles", help="Organic small-molecule SMILES input.")
    parser.add_argument("--project-name", default="project_name")
    parser.add_argument("--results-root", default="results", type=Path)
    parser.add_argument("--center", nargs=3, type=float, metavar=("X", "Y", "Z"))
    parser.add_argument("--size", nargs=3, type=float, metavar=("SX", "SY", "SZ"))
    parser.add_argument("--reference-ligand", type=Path, help="Reference ligand/docking pose for box definition.")
    parser.add_argument("--pocket-residue", action="append", default=[], help="Active-site residue for box definition, e.g. A:LYS179.")
    parser.add_argument("--keep-water-id", action="append", default=[], help="Keep key water, e.g. A_HOH_501 or A:501.")
    parser.add_argument("--keep-resname", action="append", default=[], help="Keep cofactor/residue name in receptor preparation.")
    parser.add_argument("--keep-metals", action="store_true", help="Keep common metal ions in receptor preparation.")
    parser.add_argument("--resname", default="LIG")
    parser.add_argument("--run-docking", action="store_true")
    parser.add_argument("--skip-2d-diagram", action="store_true")
    parser.add_argument("--run-md-setup", action="store_true")
    parser.add_argument("--run-md", action="store_true")
    parser.add_argument("--run-mmpbsa", choices=["gb", "pb", "decomp"])
    parser.add_argument("--receptor-group", help="Required for --run-mmpbsa.")
    parser.add_argument("--ligand-group", help="Required for --run-mmpbsa.")
    parser.add_argument("--execute", action="store_true", help="Execute selected steps. Without this, write a command plan only.")
    args = parser.parse_args()

    project_dir = args.results_root / args.project_name
    dirs = make_project_dirs(project_dir)
    log_file = dirs["logs"] / "workflow.log"
    if log_file.exists():
        log_file.unlink()

    protein = copy_input(args.protein, dirs["input"])
    ligand = copy_input(args.ligand, dirs["input"])
    reference_ligand = copy_input(args.reference_ligand, dirs["input"])

    run_step("check environment", [sys.executable, str(SCRIPT_DIR / "check_env.py")], log_file, args.execute)

    if args.run_docking:
        if not protein or (not ligand and not args.smiles):
            raise SystemExit("--run-docking requires --protein and --ligand or --smiles.")
        receptor_cmd = [
            sys.executable,
            str(SCRIPT_DIR / "prepare_receptor.py"),
            "--receptor",
            str(protein),
            "--outdir",
            str(dirs["prepared"]),
        ]
        for water in args.keep_water_id:
            receptor_cmd.extend(["--keep-water-id", water])
        for resname in args.keep_resname:
            receptor_cmd.extend(["--keep-resname", resname])
        if args.keep_metals:
            receptor_cmd.append("--keep-metals")
        if args.center:
            receptor_cmd.extend(["--pocket-center", *(str(x) for x in args.center)])
        if not args.execute:
            receptor_cmd.append("--dry-run")
        run_step("prepare target protein receptor", receptor_cmd, log_file, True)

        ligand_cmd = [
            sys.executable,
            str(SCRIPT_DIR / "prepare_ligand.py"),
            "--outdir",
            str(dirs["prepared"]),
            "--resname",
            args.resname,
        ]
        if ligand:
            ligand_cmd.extend(["--ligand", str(ligand)])
        if args.smiles:
            ligand_cmd.extend(["--smiles", args.smiles])
        if not args.execute:
            ligand_cmd.append("--dry-run")
        run_step("prepare organic small-molecule ligand", ligand_cmd, log_file, True)

        vina_cmd = [
            sys.executable,
            str(SCRIPT_DIR / "run_vina.py"),
            "--receptor-pdbqt",
            str(dirs["prepared"] / "receptor.pdbqt"),
            "--ligand-pdbqt",
            str(dirs["prepared"] / "ligand.pdbqt"),
            "--receptor-pdb",
            str(dirs["prepared"] / "receptor_clean.pdb"),
            "--outdir",
            str(dirs["docking"]),
        ]
        if args.center:
            vina_cmd.extend(["--center", *(str(x) for x in args.center)])
        if args.size:
            vina_cmd.extend(["--size", *(str(x) for x in args.size)])
        if reference_ligand:
            vina_cmd.extend(["--reference-ligand", str(reference_ligand)])
        for residue in args.pocket_residue:
            vina_cmd.extend(["--pocket-residue", residue])
        if not args.execute:
            vina_cmd.append("--dry-run")
        run_step("run AutoDock Vina docking", vina_cmd, log_file, True)

        best_complex = dirs["docking"] / "best_complex.pdb"
        run_step("analyze protein-ligand interactions with PLIP", [sys.executable, str(SCRIPT_DIR / "analyze_plip.py"), "--complex", str(best_complex), "--outdir", str(dirs["plip"])] + ([] if args.execute else ["--dry-run"]), log_file, True)
        run_step(
            "render PyMOL 3D publication figure",
            [
                sys.executable,
                str(SCRIPT_DIR / "render_pymol.py"),
                "--complex",
                str(best_complex),
                "--ligand-selection",
                f"resn {args.resname}",
                "--outdir",
                str(dirs["pymol3d"]),
            ]
            + ([] if args.execute else ["--dry-run"]),
            log_file,
            True,
        )
        if not args.skip_2d_diagram:
            diagram_cmd = [
                sys.executable,
                str(SCRIPT_DIR / "render_2d_interaction_diagram.py"),
                "--complex",
                str(best_complex),
                "--ligand-resname",
                args.resname,
                "--plip-dir",
                str(dirs["plip"]),
                "--outdir",
                str(dirs["diagram2d"]),
            ]
            if ligand:
                diagram_cmd.extend(["--ligand", str(ligand)])
            run_step("render Maestro-like 2D small-molecule interaction diagram", diagram_cmd, log_file, args.execute)
        copy_if_exists(dirs["pymol3d"] / "publication_3d.png", dirs["figures"])
        copy_if_exists(dirs["diagram2d"] / "ligand_interaction_2d.png", dirs["figures"])
        copy_if_exists(dirs["diagram2d"] / "ligand_interaction_2d.svg", dirs["figures"])

    if args.run_md_setup:
        if not protein or (not ligand and not (dirs["prepared"] / "ligand.mol2").exists()):
            raise SystemExit("--run-md-setup requires --protein and a small-molecule ligand.")
        ligand_for_md = dirs["prepared"] / "ligand.mol2" if (dirs["prepared"] / "ligand.mol2").exists() else ligand
        complex_for_md = dirs["docking"] / "best_complex.pdb"
        md_cmd = [
            sys.executable,
            str(SCRIPT_DIR / "prepare_gromacs_complex.py"),
            "--protein",
            str(protein),
            "--ligand",
            str(ligand_for_md),
            "--outdir",
            str(dirs["gromacs"]),
            "--resname",
            args.resname,
        ]
        if complex_for_md.exists():
            md_cmd.extend(["--complex", str(complex_for_md)])
        if args.execute:
            md_cmd.append("--execute")
        run_step("prepare GROMACS protein-small-molecule complex", md_cmd, log_file, True)

    if args.run_md:
        run_step("run GROMACS MD", [sys.executable, str(SCRIPT_DIR / "run_gromacs_md.py"), "--workdir", str(dirs["gromacs"])] + (["--execute"] if args.execute else []), log_file, True)
        run_step(
            "analyze GROMACS MD trajectory",
            [
                sys.executable,
                str(SCRIPT_DIR / "analyze_md.py"),
                "--tpr",
                str(dirs["gromacs"] / "processed.tpr"),
                "--xtc",
                str(dirs["gromacs"] / "processed.xtc"),
                "--index",
                str(dirs["gromacs"] / "index.ndx"),
                "--outdir",
                str(dirs["gromacs"] / "analysis"),
            ]
            + (["--execute"] if args.execute else []),
            log_file,
            True,
        )

    if args.run_mmpbsa:
        if not args.receptor_group or not args.ligand_group:
            raise SystemExit("--run-mmpbsa requires --receptor-group and --ligand-group; ligand group is never guessed.")
        run_step(
            "run gmx_MMPBSA protein-small-molecule binding analysis",
            [
                sys.executable,
                str(SCRIPT_DIR / "run_gmx_mmpbsa.py"),
                "--mode",
                args.run_mmpbsa,
                "--tpr",
                str(dirs["gromacs"] / "processed.tpr"),
                "--xtc",
                str(dirs["gromacs"] / "processed.xtc"),
                "--topol",
                str(dirs["gromacs"] / "topol.top"),
                "--index",
                str(dirs["gromacs"] / "index.ndx"),
                "--receptor-group",
                args.receptor_group,
                "--ligand-group",
                args.ligand_group,
                "--outdir",
                str(dirs["mmpbsa"]),
            ],
            log_file,
            args.execute,
        )

    run_step(
        "finalize project tables and report",
        [
            sys.executable,
            str(SCRIPT_DIR / "finalize_project_report.py"),
            "--project-dir",
            str(project_dir),
            "--project-name",
            args.project_name,
        ],
        log_file,
        True,
    )

    print(f"Project directory: {project_dir}")
    print(f"Workflow log: {log_file}")
    print(f"Execution mode: {'execute' if args.execute else 'plan only'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
