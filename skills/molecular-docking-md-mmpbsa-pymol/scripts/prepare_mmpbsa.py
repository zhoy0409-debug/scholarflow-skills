#!/usr/bin/env python3
"""Prepare gmx_MMPBSA inputs and command lines without guessing groups."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
ASSET_BY_MODE = {
    "gb": "mmpbsa_gb.in",
    "pb": "mmpbsa_pb.in",
    "decomp": "mmpbsa_decomp.in",
}


def parse_index_groups(index_file: Path) -> list[str]:
    groups: list[str] = []
    for line in index_file.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            groups.append(stripped.strip("[]").strip())
    return groups


def require_file(path: Path, label: str) -> None:
    if not path.exists():
        raise SystemExit(f"Missing {label}: {path}")


def choose_group(label: str, provided: str | None, groups: list[str]) -> str | None:
    if provided:
        return provided
    print(f"\nAvailable GROMACS index groups for {label}:")
    for i, group in enumerate(groups):
        print(f"  {i}: {group}")
    if sys.stdin.isatty():
        value = input(f"Select {label} group by name or number: ").strip()
        return value or None
    return None


def build_command(args: argparse.Namespace, input_file: Path, output_dir: Path) -> list[str]:
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
        str(output_dir / "FINAL_RESULTS_MMPBSA.dat"),
        "-eo",
        str(output_dir / "summary_mmpbsa.csv"),
    ]
    if args.mode == "decomp":
        cmd.extend(
            [
                "-do",
                str(output_dir / "FINAL_DECOMP_MMPBSA.dat"),
                "-deo",
                str(output_dir / "FINAL_DECOMP_MMPBSA.csv"),
            ]
        )
    return cmd


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=["gb", "pb", "decomp"], default="gb")
    parser.add_argument("--tpr", required=True, type=Path)
    parser.add_argument("--xtc", required=True, type=Path)
    parser.add_argument("--topol", required=True, type=Path)
    parser.add_argument("--index", required=True, type=Path)
    parser.add_argument("--outdir", default="mmpbsa", type=Path)
    parser.add_argument("--input", type=Path, help="Custom gmx_MMPBSA input file.")
    parser.add_argument("--receptor-group")
    parser.add_argument("--ligand-group")
    args = parser.parse_args()

    for label, path in [("TPR", args.tpr), ("trajectory", args.xtc), ("topology", args.topol), ("index", args.index)]:
        require_file(path, label)
    args.tpr = args.tpr.resolve()
    args.xtc = args.xtc.resolve()
    args.topol = args.topol.resolve()
    args.index = args.index.resolve()
    if args.input:
        args.input = args.input.resolve()
    groups = parse_index_groups(args.index)
    args.receptor_group = choose_group("receptor", args.receptor_group, groups)
    args.ligand_group = choose_group("ligand", args.ligand_group, groups)
    if not args.receptor_group or not args.ligand_group:
        print("\nReceptor/ligand groups are required. This script will not guess them.")
        print("Rerun with: --receptor-group <GROUP_OR_INDEX> --ligand-group <GROUP_OR_INDEX>")
        return 2

    args.outdir.mkdir(parents=True, exist_ok=True)
    groups_file = args.outdir / "index_groups.txt"
    groups_file.write_text("\n".join(f"{i}\t{name}" for i, name in enumerate(groups)) + "\n", encoding="utf-8")

    if args.input:
        input_file = args.input
    else:
        src = SKILL_DIR / "assets" / ASSET_BY_MODE[args.mode]
        input_file = args.outdir / ASSET_BY_MODE[args.mode]
        shutil.copy2(src, input_file)

    cmd = build_command(args, input_file, args.outdir)
    command_file = args.outdir / "gmx_MMPBSA_command.txt"
    command_file.write_text(" ".join(cmd) + "\n", encoding="utf-8")
    print(f"Groups listed in: {groups_file}")
    print(f"MMPBSA input: {input_file}")
    print(f"Command written: {command_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
