#!/usr/bin/env python3
"""Prepare target-protein receptor PDB/PDBQT for small-molecule docking."""

from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
from pathlib import Path


WATER_RESNAMES = {"HOH", "WAT", "H2O", "TIP", "TIP3", "SOL"}
METAL_RESNAMES = {
    "LI",
    "NA",
    "K",
    "RB",
    "CS",
    "MG",
    "CA",
    "MN",
    "FE",
    "CO",
    "NI",
    "CU",
    "ZN",
    "CD",
    "HG",
    "AL",
}


def ensure_tool(name: str, required: bool = True) -> str:
    path = shutil.which(name)
    if not path and required:
        raise SystemExit(f"Required tool not found in PATH: {name}")
    return path or name


def run_command(cmd: list[str], log_file: Path, dry_run: bool = False) -> None:
    log_file.write_text(" ".join(cmd) + "\n", encoding="utf-8")
    if dry_run:
        return
    with log_file.open("a", encoding="utf-8") as handle:
        proc = subprocess.run(cmd, text=True, stdout=handle, stderr=subprocess.STDOUT, check=False)
    if proc.returncode != 0:
        raise SystemExit(f"Command failed; see log: {log_file}")


def parse_water_ids(items: list[str]) -> set[tuple[str, str, str]]:
    parsed: set[tuple[str, str, str]] = set()
    for item in items:
        parts = item.replace(":", "_").replace("-", "_").split("_")
        if len(parts) == 1:
            parsed.add(("", "HOH", parts[0]))
        elif len(parts) == 2:
            parsed.add((parts[0], "HOH", parts[1]))
        else:
            parsed.add((parts[0], parts[1].upper(), parts[2]))
    return parsed


def parse_xyz(values: list[float] | None) -> tuple[float, float, float] | None:
    if not values:
        return None
    return (float(values[0]), float(values[1]), float(values[2]))


def distance(atom_xyz: tuple[float, float, float], center: tuple[float, float, float]) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(atom_xyz, center)))


def missing_residue_warnings(receptor: Path, pocket_center: tuple[float, float, float] | None, pocket_radius: float) -> list[str]:
    warnings: list[str] = []
    missing: list[str] = []
    for line in receptor.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("REMARK 465") and len(line.split()) >= 5:
            missing.append(" ".join(line.split()[2:]))
    if missing:
        warnings.append(f"Input PDB reports missing residues: {'; '.join(missing[:12])}" + (" ..." if len(missing) > 12 else ""))
    if pocket_center and missing:
        warnings.append(
            "Missing residues are reported in the structure. This script cannot reliably locate them; "
            f"inspect whether any are within about {pocket_radius:.1f} A of the binding pocket."
        )
    return warnings


def clean_receptor(
    receptor: Path,
    output: Path,
    keep_water: bool,
    keep_water_ids: set[tuple[str, str, str]],
    keep_hetero: bool,
    keep_resnames: set[str],
    keep_metals: bool,
    chain: str | None,
    pocket_center: tuple[float, float, float] | None,
    pocket_radius: float,
) -> dict[str, object]:
    kept_resnames: set[str] = set()
    removed_waters = 0
    kept_waters = 0
    removed_hetero: set[str] = set()
    with receptor.open("r", encoding="utf-8", errors="ignore") as src, output.open("w", encoding="utf-8") as dst:
        for line in src:
            record = line[:6].strip()
            if record not in {"ATOM", "HETATM", "TER"}:
                continue
            if record == "TER":
                dst.write(line)
                continue
            resname = line[17:20].strip().upper()
            line_chain = line[21].strip()
            resnum = line[22:26].strip()
            if chain and line_chain != chain:
                continue
            key = (line_chain, resname, resnum)
            keep_this_water = keep_water or key in keep_water_ids or (line_chain, "HOH", resnum) in keep_water_ids
            if resname in WATER_RESNAMES:
                if keep_this_water:
                    kept_waters += 1
                else:
                    removed_waters += 1
                    continue
            if record == "HETATM" and resname not in WATER_RESNAMES:
                is_metal = resname in METAL_RESNAMES or line[76:78].strip().upper() in METAL_RESNAMES
                should_keep = keep_hetero or resname in keep_resnames or (keep_metals and is_metal)
                if not should_keep:
                    removed_hetero.add(resname)
                    continue
            if pocket_center:
                try:
                    xyz = (float(line[30:38]), float(line[38:46]), float(line[46:54]))
                    if distance(xyz, pocket_center) <= pocket_radius:
                        kept_resnames.add(f"{line_chain}:{resname}{resnum}")
                except ValueError:
                    pass
            if len(line) > 16 and line[16] not in {" ", "A"}:
                continue
            if len(line) > 16 and line[16] == "A":
                line = line[:16] + " " + line[17:]
            dst.write(line)
        dst.write("END\n")
    return {
        "removed_waters": removed_waters,
        "kept_waters": kept_waters,
        "removed_hetero_resnames": sorted(removed_hetero),
        "pocket_nearby_residues": sorted(kept_resnames),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receptor", required=True, type=Path, help="Input target-protein PDB.")
    parser.add_argument("--outdir", default="prepared", type=Path)
    parser.add_argument("--prefix", default="receptor")
    parser.add_argument("--chain", help="Optional chain filter. By default all protein chains are preserved.")
    parser.add_argument("--keep-water", action="store_true", help="Keep all crystallographic waters.")
    parser.add_argument("--keep-water-id", action="append", default=[], help="Keep a key water, e.g. A_HOH_501 or A:501.")
    parser.add_argument("--keep-hetero", action="store_true", help="Keep all non-water HETATM records.")
    parser.add_argument("--keep-resname", action="append", default=[], help="Cofactor/residue name to keep as HETATM.")
    parser.add_argument("--keep-metals", action="store_true", help="Keep common metal ions.")
    parser.add_argument("--pocket-center", nargs=3, type=float, metavar=("X", "Y", "Z"), help="Optional binding-pocket center for warnings.")
    parser.add_argument("--pocket-radius", type=float, default=6.0)
    parser.add_argument("--dry-run", action="store_true", help="Write commands without executing Meeko.")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    cleaned = args.outdir / f"{args.prefix}_clean.pdb"
    pdbqt = args.outdir / f"{args.prefix}.pdbqt"
    keep_resnames = {item.upper() for item in args.keep_resname}
    keep_water_ids = parse_water_ids(args.keep_water_id)
    pocket_center = parse_xyz(args.pocket_center)
    warnings = missing_residue_warnings(args.receptor, pocket_center, args.pocket_radius)

    stats = clean_receptor(
        args.receptor,
        cleaned,
        args.keep_water,
        keep_water_ids,
        args.keep_hetero,
        keep_resnames,
        args.keep_metals,
        args.chain,
        pocket_center,
        args.pocket_radius,
    )

    meeko = ensure_tool("mk_prepare_receptor.py", required=not args.dry_run)
    prefix = args.outdir / args.prefix
    cmd = [meeko, "-i", str(cleaned), "-o", str(prefix), "-p"]
    run_command(cmd, args.outdir / "prepare_receptor.log", args.dry_run)

    if not args.dry_run and not pdbqt.exists():
        candidates = sorted(args.outdir.glob(f"{args.prefix}*.pdbqt"))
        if candidates:
            candidates[0].replace(pdbqt)
    metadata = {
        "input": str(args.receptor),
        "default_system": "small molecule-target protein",
        "chains": "all preserved" if not args.chain else args.chain,
        "ordinary_crystallographic_waters": "removed unless explicitly kept",
        "hydrogen_handling": "Meeko receptor preparation requested; verify protonation for catalytic residues manually",
        "missing_atom_handling": "external modeling/checking recommended if missing atoms/residues affect pocket",
        "kept_resnames": sorted(keep_resnames),
        "keep_metals": args.keep_metals,
        "warnings": warnings,
        **stats,
    }
    (args.outdir / "receptor_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (args.outdir / "receptor_warnings.txt").write_text("\n".join(warnings) + ("\n" if warnings else ""), encoding="utf-8")
    print(f"Clean receptor: {cleaned}")
    print(f"Receptor PDBQT: {pdbqt}")
    print(f"Metadata: {args.outdir / 'receptor_metadata.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
