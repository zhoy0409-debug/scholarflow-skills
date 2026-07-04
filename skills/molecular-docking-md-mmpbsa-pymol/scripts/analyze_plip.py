#!/usr/bin/env python3
"""Run PLIP interaction analysis for a protein-ligand complex."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--complex", required=True, type=Path, help="Protein-ligand complex PDB.")
    parser.add_argument("--outdir", default="docking/plip", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    plip = shutil.which("plip") or "plip"
    if plip == "plip" and not args.dry_run:
        raise SystemExit("Required tool not found in PATH: plip")
    args.outdir.mkdir(parents=True, exist_ok=True)
    cmd = [plip, "-f", str(args.complex), "-o", str(args.outdir), "-x", "-t", "-y"]
    (args.outdir / "plip_command.txt").write_text(" ".join(cmd) + "\n", encoding="utf-8")
    if args.dry_run:
        print(f"PLIP command written: {args.outdir / 'plip_command.txt'}")
        return 0
    with (args.outdir / "plip.log").open("w", encoding="utf-8") as handle:
        proc = subprocess.run(cmd, text=True, stdout=handle, stderr=subprocess.STDOUT, check=False)
    if proc.returncode != 0:
        raise SystemExit(f"PLIP failed; see log: {args.outdir / 'plip.log'}")
    print(f"PLIP output: {args.outdir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
