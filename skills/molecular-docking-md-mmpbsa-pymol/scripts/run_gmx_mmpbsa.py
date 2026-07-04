#!/usr/bin/env python3
"""Run gmx_MMPBSA in GB, PB, or per-residue decomposition mode."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSET_BY_MODE = {
    "gb": "mmpbsa_gb.in",
    "pb": "mmpbsa_pb.in",
    "decomp": "mmpbsa_decomp.in",
}


def require_file(path: Path, label: str) -> None:
    if not path.exists():
        raise SystemExit(f"Missing {label}: {path}")


def build_command(args: argparse.Namespace, input_file: Path) -> list[str]:
    cmd = [
        "gmx_MMPBSA",
        "-O",
        "-i",
        str(input_file),
        "-cs",
        str(args.tpr),
        "-ct",
        str(args.xtc),
        "-ci",
        str(args.index),
        "-cg",
        str(args.receptor_group),
        str(args.ligand_group),
        "-cp",
        str(args.topol),
        "-o",
        "FINAL_RESULTS_MMPBSA.dat",
        "-eo",
        "summary_mmpbsa.csv",
    ]
    if args.mode == "decomp":
        cmd.extend(["-do", "FINAL_DECOMP_MMPBSA.dat", "-deo", "FINAL_DECOMP_MMPBSA.csv"])
    return cmd


def parse_outputs(outdir: Path, mode: str) -> None:
    sys.path.insert(0, str(SCRIPT_DIR))
    try:
        import parse_mmpbsa_results
    except Exception as exc:
        print(f"Could not import parser: {exc}")
        return
    results = outdir / "FINAL_RESULTS_MMPBSA.dat"
    decomp = outdir / "FINAL_DECOMP_MMPBSA.csv"
    if not decomp.exists():
        decomp = outdir / "FINAL_DECOMP_MMPBSA.dat"
    parser_args = ["--results", str(results), "--outdir", str(outdir)]
    if mode == "decomp" and decomp.exists():
        parser_args.extend(["--decomp", str(decomp)])
    parse_mmpbsa_results.main(parser_args)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["gb", "pb", "decomp"], default="gb")
    parser.add_argument("--tpr", required=True, type=Path)
    parser.add_argument("--xtc", required=True, type=Path)
    parser.add_argument("--topol", required=True, type=Path)
    parser.add_argument("--index", required=True, type=Path)
    parser.add_argument("--receptor-group", required=True, help="Do not guess; pass name or index from index.ndx.")
    parser.add_argument("--ligand-group", required=True, help="Do not guess; pass name or index from index.ndx.")
    parser.add_argument("--outdir", default="mmpbsa", type=Path)
    parser.add_argument("--input", type=Path, help="Custom mmpbsa input file.")
    parser.add_argument("--no-parse", action="store_true")
    args = parser.parse_args(argv)

    for label, path in [("TPR", args.tpr), ("trajectory", args.xtc), ("topology", args.topol), ("index", args.index)]:
        require_file(path, label)
    args.tpr = args.tpr.resolve()
    args.xtc = args.xtc.resolve()
    args.topol = args.topol.resolve()
    args.index = args.index.resolve()
    if args.input:
        args.input = args.input.resolve()
    executable = shutil.which("gmx_MMPBSA")
    if not executable:
        raise SystemExit("Required tool not found in PATH: gmx_MMPBSA")

    args.outdir.mkdir(parents=True, exist_ok=True)
    if args.input:
        input_file = args.input
    else:
        input_file = args.outdir / ASSET_BY_MODE[args.mode]
        shutil.copy2(SKILL_DIR / "assets" / ASSET_BY_MODE[args.mode], input_file)

    cmd = build_command(args, input_file)
    cmd[0] = executable
    (args.outdir / "gmx_MMPBSA_command.txt").write_text(" ".join(cmd) + "\n", encoding="utf-8")
    log_file = args.outdir / "gmx_MMPBSA.log"
    with log_file.open("w", encoding="utf-8") as handle:
        handle.write("$ " + " ".join(cmd) + "\n")
        proc = subprocess.run(cmd, cwd=str(args.outdir), text=True, stdout=handle, stderr=subprocess.STDOUT, check=False)
    if proc.returncode != 0:
        print(f"gmx_MMPBSA failed; temporary files were preserved in {args.outdir}")
        print(f"See log: {log_file}")
        return proc.returncode
    if not args.no_parse:
        parse_outputs(args.outdir, args.mode)
    print(f"gmx_MMPBSA output: {args.outdir}")
    print(f"Raw results: {args.outdir / 'FINAL_RESULTS_MMPBSA.dat'}")
    print(f"Summary CSV: {args.outdir / 'summary_mmpbsa.csv'}")
    if args.mode == "decomp":
        print(f"Residue decomposition CSV: {args.outdir / 'per_residue_decomposition.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
