#!/usr/bin/env python3
"""Analyze GROMACS trajectories: RMSD, RMSF, Rg, and H-bonds."""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
from pathlib import Path


def which(name: str, required: bool = True) -> str:
    path = shutil.which(name)
    if not path and required:
        raise SystemExit(f"Required tool not found in PATH: {name}")
    return path or name


def run(cmd: list[str], log_file: Path, execute: bool, stdin: str | None = None) -> None:
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write("$ " + " ".join(cmd) + "\n")
        if not execute:
            return
        proc = subprocess.run(cmd, input=stdin, text=True, stdout=handle, stderr=subprocess.STDOUT, check=False)
    if execute and proc.returncode != 0:
        raise SystemExit(f"Command failed; see log: {log_file}")


def parse_xvg(path: Path) -> list[list[float]]:
    rows: list[list[float]] = []
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line or line.startswith(("#", "@")):
            continue
        parts = line.split()
        try:
            rows.append([float(part) for part in parts])
        except ValueError:
            continue
    return rows


def write_csv(rows: list[list[float]], output: Path, headers: list[str]) -> None:
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(headers)
        writer.writerows(rows)


def plot_xy(csv_file: Path, png_file: Path, title: str, xlabel: str, ylabel: str) -> None:
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
    except ImportError:
        return
    if not csv_file.exists():
        return
    data = pd.read_csv(csv_file)
    if data.shape[1] < 2:
        return
    plt.figure(figsize=(6, 4), dpi=160)
    plt.plot(data.iloc[:, 0], data.iloc[:, 1], lw=1.5)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(png_file, dpi=300)
    plt.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tpr", required=True, type=Path)
    parser.add_argument("--xtc", required=True, type=Path)
    parser.add_argument("--index", required=True, type=Path)
    parser.add_argument("--outdir", default="md_analysis", type=Path)
    parser.add_argument("--rmsd-ref-group", default="Backbone")
    parser.add_argument("--rmsd-fit-group", default="Backbone")
    parser.add_argument("--rmsf-group", default="Protein")
    parser.add_argument("--rg-group", default="Protein")
    parser.add_argument("--hbond-group-a", default="Protein")
    parser.add_argument("--hbond-group-b", default="LIG")
    parser.add_argument("--execute", action="store_true", help="Run GROMACS analysis commands. Without this, write command plan only.")
    args = parser.parse_args()

    gmx = which("gmx", required=args.execute)
    args.outdir.mkdir(parents=True, exist_ok=True)
    log_file = args.outdir / "analyze_md.log"
    if log_file.exists():
        log_file.unlink()

    rmsd_xvg = args.outdir / "rmsd.xvg"
    rmsf_xvg = args.outdir / "rmsf.xvg"
    rg_xvg = args.outdir / "radius_gyration.xvg"
    hb_xvg = args.outdir / "hbonds.xvg"

    run([gmx, "rms", "-s", str(args.tpr), "-f", str(args.xtc), "-n", str(args.index), "-o", str(rmsd_xvg), "-tu", "ns"], log_file, args.execute, stdin=f"{args.rmsd_ref_group}\n{args.rmsd_fit_group}\n")
    run([gmx, "rmsf", "-s", str(args.tpr), "-f", str(args.xtc), "-n", str(args.index), "-o", str(rmsf_xvg), "-res"], log_file, args.execute, stdin=f"{args.rmsf_group}\n")
    run([gmx, "gyrate", "-s", str(args.tpr), "-f", str(args.xtc), "-n", str(args.index), "-o", str(rg_xvg)], log_file, args.execute, stdin=f"{args.rg_group}\n")
    run([gmx, "hbond", "-s", str(args.tpr), "-f", str(args.xtc), "-n", str(args.index), "-num", str(hb_xvg)], log_file, args.execute, stdin=f"{args.hbond_group_a}\n{args.hbond_group_b}\n")

    outputs = [
        (rmsd_xvg, args.outdir / "rmsd.csv", ["time_ns", "rmsd_nm"], args.outdir / "rmsd.png", "Backbone RMSD", "Time (ns)", "RMSD (nm)"),
        (rmsf_xvg, args.outdir / "rmsf.csv", ["residue", "rmsf_nm"], args.outdir / "rmsf.png", "Residue RMSF", "Residue", "RMSF (nm)"),
        (rg_xvg, args.outdir / "radius_gyration.csv", ["time_ps", "rg_nm"], args.outdir / "radius_gyration.png", "Radius of Gyration", "Time", "Rg (nm)"),
        (hb_xvg, args.outdir / "hbonds.csv", ["time_ps", "hbonds"], args.outdir / "hbonds.png", "Protein-Ligand H-bonds", "Time", "H-bonds"),
    ]
    for xvg, csv_path, headers, png, title, xlabel, ylabel in outputs:
        rows = parse_xvg(xvg)
        if rows:
            write_csv(rows, csv_path, headers[: len(rows[0])])
            plot_xy(csv_path, png, title, xlabel, ylabel)

    print(f"Analysis output: {args.outdir}")
    print(f"Execution mode: {'execute' if args.execute else 'plan only'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
