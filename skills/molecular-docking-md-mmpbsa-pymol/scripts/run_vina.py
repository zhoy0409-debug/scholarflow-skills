#!/usr/bin/env python3
"""Run AutoDock Vina for small-molecule target-protein docking and parse scores."""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import shutil
import subprocess
from pathlib import Path


SCORE_RE = re.compile(r"REMARK VINA RESULT:\s*([-+0-9.]+)\s+([-+0-9.]+)\s+([-+0-9.]+)")


def ensure_tool(name: str, required: bool = True) -> str:
    path = shutil.which(name)
    if not path and required:
        raise SystemExit(f"Required tool not found in PATH: {name}")
    return path or name


def parse_scores(pdbqt: Path) -> list[dict[str, str]]:
    scores: list[dict[str, str]] = []
    if not pdbqt.exists():
        return scores
    pose = 0
    for line in pdbqt.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.startswith("MODEL"):
            parts = line.split()
            pose = int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else pose + 1
        match = SCORE_RE.search(line)
        if match:
            if pose == 0:
                pose = len(scores) + 1
            scores.append(
                {
                    "pose": str(pose),
                    "affinity_kcal_mol": match.group(1),
                    "rmsd_lb": match.group(2),
                    "rmsd_ub": match.group(3),
                    "selection_note": "best pose defaults to lowest Vina affinity; inspect interactions before final interpretation" if pose == 1 else "",
                }
            )
    return scores


def write_scores(scores: list[dict[str, str]], output: Path) -> None:
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["pose", "affinity_kcal_mol", "rmsd_lb", "rmsd_ub", "selection_note"])
        writer.writeheader()
        writer.writerows(scores)


def coordinates_from_pdb_like(path: Path, residues: set[str] | None = None) -> list[tuple[float, float, float]]:
    coords: list[tuple[float, float, float]] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.startswith(("ATOM", "HETATM")):
            continue
        if residues:
            token1 = f"{line[21].strip()}:{line[17:20].strip().upper()}{line[22:26].strip()}".upper()
            token2 = f"{line[21].strip()}:{line[22:26].strip()}".upper()
            token3 = f"{line[17:20].strip().upper()}{line[22:26].strip()}".upper()
            if residues.isdisjoint({token1, token2, token3}):
                continue
        try:
            coords.append((float(line[30:38]), float(line[38:46]), float(line[46:54])))
        except ValueError:
            continue
    return coords


def coordinates_from_ligand(path: Path) -> list[tuple[float, float, float]]:
    suffix = path.suffix.lower()
    if suffix in {".pdb", ".pdbqt"}:
        return coordinates_from_pdb_like(path)
    try:
        from rdkit import Chem
    except ImportError:
        return []
    mol = None
    if suffix in {".sdf", ".sd"}:
        supplier = Chem.SDMolSupplier(str(path), removeHs=False)
        mol = next((item for item in supplier if item is not None), None)
    elif suffix == ".mol2":
        mol = Chem.MolFromMol2File(str(path), sanitize=False, removeHs=False)
    elif suffix == ".mol":
        mol = Chem.MolFromMolFile(str(path), sanitize=False, removeHs=False)
    if mol is None or mol.GetNumConformers() == 0:
        return []
    conf = mol.GetConformer()
    return [(float(conf.GetAtomPosition(i).x), float(conf.GetAtomPosition(i).y), float(conf.GetAtomPosition(i).z)) for i in range(mol.GetNumAtoms())]


def center_and_size(coords: list[tuple[float, float, float]], padding: float, minimum: float) -> tuple[list[float], list[float]]:
    if not coords:
        raise SystemExit("No coordinates available to define docking box.")
    mins = [min(coord[i] for coord in coords) for i in range(3)]
    maxs = [max(coord[i] for coord in coords) for i in range(3)]
    center = [(mins[i] + maxs[i]) / 2 for i in range(3)]
    size = [max(minimum, (maxs[i] - mins[i]) + padding) for i in range(3)]
    return center, size


def parse_residue_tokens(items: list[str]) -> set[str]:
    tokens: set[str] = set()
    for item in items:
        for part in re.split(r"[,\s]+", item.strip()):
            if part:
                tokens.add(part.upper())
    return tokens


def resolve_box(args: argparse.Namespace) -> tuple[list[float], list[float], str]:
    if args.center:
        size = args.size or [22.0, 22.0, 22.0]
        return list(args.center), list(size), "user-provided coordinates"
    if args.reference_ligand:
        coords = coordinates_from_ligand(args.reference_ligand)
        center, size = center_and_size(coords, args.box_padding, args.min_box_size)
        return center, size, f"reference ligand: {args.reference_ligand}"
    if args.pocket_residue:
        if not args.receptor_pdb:
            raise SystemExit("--pocket-residue requires --receptor-pdb.")
        tokens = parse_residue_tokens(args.pocket_residue)
        coords = coordinates_from_pdb_like(args.receptor_pdb, tokens)
        center, _ = center_and_size(coords, 0.0, 0.0)
        size = args.size or [22.0, 22.0, 22.0]
        return center, list(size), f"pocket residues: {', '.join(sorted(tokens))}"
    raise SystemExit(
        "Docking box is undefined. Provide --reference-ligand, --pocket-residue, or --center. "
        "P2Rank/fpocket can be used as a separate pocket-prediction aid, but predicted pockets should be reviewed."
    )


def extract_first_model(pdbqt: Path, out_pdbqt: Path) -> None:
    in_model = False
    wrote = False
    with pdbqt.open("r", encoding="utf-8", errors="ignore") as src, out_pdbqt.open("w", encoding="utf-8") as dst:
        for line in src:
            if line.startswith("MODEL"):
                in_model = True
                continue
            if line.startswith("ENDMDL") and in_model:
                break
            if in_model or not any(line.startswith(tag) for tag in ("MODEL", "ENDMDL")):
                if line.startswith(("ATOM", "HETATM", "ROOT", "BRANCH", "ENDBRANCH", "ENDROOT", "TORSDOF", "REMARK")):
                    dst.write(line)
                    wrote = True
        if wrote:
            dst.write("END\n")


def make_complex(receptor_pdb: Path, ligand_pdbqt: Path, out_complex: Path, log_file: Path) -> None:
    obabel = ensure_tool("obabel")
    first_pose = out_complex.with_name("best_pose.pdbqt")
    ligand_pdb = out_complex.with_name("best_pose_ligand.pdb")
    extract_first_model(ligand_pdbqt, first_pose)
    with log_file.open("a", encoding="utf-8") as handle:
        cmd = [obabel, str(first_pose), "-O", str(ligand_pdb)]
        handle.write(" ".join(cmd) + "\n")
        proc = subprocess.run(cmd, text=True, stdout=handle, stderr=subprocess.STDOUT, check=False)
    if proc.returncode != 0:
        raise SystemExit(f"OpenBabel failed while generating complex; see {log_file}")
    with out_complex.open("w", encoding="utf-8") as dst:
        for line in receptor_pdb.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith(("ATOM", "HETATM", "TER")):
                dst.write(line.rstrip() + "\n")
        for line in ligand_pdb.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith(("ATOM", "HETATM", "CONECT")):
                dst.write(line.rstrip() + "\n")
        dst.write("END\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receptor-pdbqt", required=True, type=Path)
    parser.add_argument("--ligand-pdbqt", required=True, type=Path)
    parser.add_argument("--center", nargs=3, type=float, metavar=("X", "Y", "Z"))
    parser.add_argument("--size", nargs=3, type=float, metavar=("SX", "SY", "SZ"))
    parser.add_argument("--reference-ligand", type=Path, help="Co-crystal/reference ligand used to define docking box.")
    parser.add_argument("--pocket-residue", action="append", default=[], help="Active-site residue token, e.g. A:LYS179 or LYS179.")
    parser.add_argument("--box-padding", type=float, default=8.0)
    parser.add_argument("--min-box-size", type=float, default=18.0)
    parser.add_argument("--outdir", default="docking", type=Path)
    parser.add_argument("--exhaustiveness", default=16, type=int)
    parser.add_argument("--num-modes", default=20, type=int)
    parser.add_argument("--energy-range", default=3, type=float)
    parser.add_argument("--cpu", type=int)
    parser.add_argument("--seed", type=int, default=2026)
    parser.add_argument("--receptor-pdb", type=Path, help="Cleaned receptor PDB for best_complex.pdb and residue-box mode.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    center, size, box_source = resolve_box(args)
    vina = ensure_tool("vina", required=not args.dry_run)
    args.outdir.mkdir(parents=True, exist_ok=True)
    out_pdbqt = args.outdir / "vina_poses.pdbqt"
    log_file = args.outdir / "vina.log"
    cmd = [
        vina,
        "--receptor",
        str(args.receptor_pdbqt),
        "--ligand",
        str(args.ligand_pdbqt),
        "--center_x",
        f"{center[0]:.3f}",
        "--center_y",
        f"{center[1]:.3f}",
        "--center_z",
        f"{center[2]:.3f}",
        "--size_x",
        f"{size[0]:.3f}",
        "--size_y",
        f"{size[1]:.3f}",
        "--size_z",
        f"{size[2]:.3f}",
        "--exhaustiveness",
        str(args.exhaustiveness),
        "--num_modes",
        str(args.num_modes),
        "--energy_range",
        str(args.energy_range),
        "--seed",
        str(args.seed),
        "--out",
        str(out_pdbqt),
    ]
    if args.cpu:
        cmd.extend(["--cpu", str(args.cpu)])

    metadata = {
        "system_type": "small molecule-target protein docking",
        "box_source": box_source,
        "center": center,
        "size": size,
        "exhaustiveness": args.exhaustiveness,
        "num_modes": args.num_modes,
        "energy_range": args.energy_range,
        "seed": args.seed,
        "best_pose_rule": "lowest Vina affinity by default; validate with interaction plausibility",
    }
    (args.outdir / "vina_command.txt").write_text(" ".join(cmd) + "\n", encoding="utf-8")
    (args.outdir / "docking_box.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    if not args.dry_run:
        with log_file.open("w", encoding="utf-8") as handle:
            proc = subprocess.run(cmd, text=True, stdout=handle, stderr=subprocess.STDOUT, check=False)
        if proc.returncode != 0:
            raise SystemExit(f"Vina failed; see log: {log_file}")
    scores = parse_scores(out_pdbqt)
    write_scores(scores, args.outdir / "docking_scores.csv")
    write_scores(scores, args.outdir / "vina_scores.csv")
    if args.receptor_pdb and not args.dry_run:
        make_complex(args.receptor_pdb, out_pdbqt, args.outdir / "best_complex.pdb", log_file)
    (args.outdir / "best_pose_selection.txt").write_text(
        "Default best pose is the pose with the lowest Vina affinity, usually pose 1. "
        "Use PLIP/ProLIF contacts, chemistry, and known SAR to judge plausibility.\n",
        encoding="utf-8",
    )
    print(f"Vina poses: {out_pdbqt}")
    print(f"Scores CSV: {args.outdir / 'docking_scores.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
