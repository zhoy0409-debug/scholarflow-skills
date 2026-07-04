#!/usr/bin/env python3
"""Run GROMACS minimization, equilibration, production, and trajectory processing."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent


def which(name: str, required: bool = True) -> str:
    path = shutil.which(name)
    if not path and required:
        raise SystemExit(f"Required tool not found in PATH: {name}")
    return path or name


def run(cmd: list[str], log_file: Path, cwd: Path, execute: bool, stdin: str | None = None) -> None:
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write("$ " + " ".join(cmd) + "\n")
        if not execute:
            return
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            input=stdin,
            text=True,
            stdout=handle,
            stderr=subprocess.STDOUT,
            check=False,
        )
    if execute and proc.returncode != 0:
        raise SystemExit(f"Command failed; see log: {log_file}")


def copy_mdp_templates(workdir: Path) -> None:
    for name in ["mdp_minim.mdp", "mdp_nvt.mdp", "mdp_npt.mdp", "mdp_md.mdp"]:
        src = SKILL_DIR / "assets" / name
        dst = workdir / name
        if src.exists() and not dst.exists():
            shutil.copy2(src, dst)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workdir", default="md_setup", type=Path)
    parser.add_argument("--start-structure", default="solv_ions.gro")
    parser.add_argument("--topol", default="topol.top")
    parser.add_argument("--index", default="index.ndx")
    parser.add_argument("--maxwarn", type=int, default=1)
    parser.add_argument("--center-group", default="Protein")
    parser.add_argument("--output-group", default="System")
    parser.add_argument("--fit-group", default="Protein")
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()

    gmx = which("gmx", required=args.execute)
    args.workdir.mkdir(parents=True, exist_ok=True)
    copy_mdp_templates(args.workdir)
    log_file = args.workdir / "run_gromacs_md.log"
    if log_file.exists():
        log_file.unlink()

    if not (args.workdir / args.index).exists():
        run([gmx, "make_ndx", "-f", args.start_structure, "-o", args.index], log_file, args.workdir, args.execute, stdin="q\n")

    run(
        [gmx, "grompp", "-f", "mdp_minim.mdp", "-c", args.start_structure, "-p", args.topol, "-n", args.index, "-o", "em.tpr", "-maxwarn", str(args.maxwarn)],
        log_file,
        args.workdir,
        args.execute,
    )
    run([gmx, "mdrun", "-deffnm", "em"], log_file, args.workdir, args.execute)
    run(
        [gmx, "grompp", "-f", "mdp_nvt.mdp", "-c", "em.gro", "-r", "em.gro", "-p", args.topol, "-n", args.index, "-o", "nvt.tpr", "-maxwarn", str(args.maxwarn)],
        log_file,
        args.workdir,
        args.execute,
    )
    run([gmx, "mdrun", "-deffnm", "nvt"], log_file, args.workdir, args.execute)
    run(
        [gmx, "grompp", "-f", "mdp_npt.mdp", "-c", "nvt.gro", "-r", "nvt.gro", "-t", "nvt.cpt", "-p", args.topol, "-n", args.index, "-o", "npt.tpr", "-maxwarn", str(args.maxwarn)],
        log_file,
        args.workdir,
        args.execute,
    )
    run([gmx, "mdrun", "-deffnm", "npt"], log_file, args.workdir, args.execute)
    run(
        [gmx, "grompp", "-f", "mdp_md.mdp", "-c", "npt.gro", "-t", "npt.cpt", "-p", args.topol, "-n", args.index, "-o", "md.tpr", "-maxwarn", str(args.maxwarn)],
        log_file,
        args.workdir,
        args.execute,
    )
    run([gmx, "mdrun", "-deffnm", "md"], log_file, args.workdir, args.execute)
    run(
        [gmx, "trjconv", "-s", "md.tpr", "-f", "md.xtc", "-o", "centered.xtc", "-pbc", "mol", "-center", "-n", args.index],
        log_file,
        args.workdir,
        args.execute,
        stdin=f"{args.center_group}\n{args.output_group}\n",
    )
    run(
        [gmx, "trjconv", "-s", "md.tpr", "-f", "centered.xtc", "-o", "processed.xtc", "-fit", "rot+trans", "-n", args.index],
        log_file,
        args.workdir,
        args.execute,
        stdin=f"{args.fit_group}\n{args.output_group}\n",
    )
    if args.execute and (args.workdir / "md.tpr").exists():
        shutil.copy2(args.workdir / "md.tpr", args.workdir / "processed.tpr")

    print(f"MD workdir: {args.workdir}")
    print(f"Execution mode: {'execute' if args.execute else 'plan only'}")
    print(f"Log/command plan: {log_file}")
    print(f"Processed trajectory: {args.workdir / 'processed.xtc'}")
    print(f"Processed TPR: {args.workdir / 'processed.tpr'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
