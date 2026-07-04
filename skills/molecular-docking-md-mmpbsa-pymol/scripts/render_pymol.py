#!/usr/bin/env python3
"""Render publication-style 3D small-molecule target-protein interaction figures."""

from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
STYLE_TEMPLATE = SKILL_DIR / "assets" / "pymol_publication_style.pml"


def residue_selection(token: str) -> str | None:
    token = token.strip()
    if not token:
        return None
    match = re.search(r"(?:(?P<chain>[A-Za-z0-9])[:/_-])?(?:(?P<resn>[A-Za-z]{3})[:/_-]?)?(?P<resi>-?\d+[A-Za-z]?)", token)
    if not match:
        return None
    chain = match.group("chain")
    resi = match.group("resi")
    clauses = [f"resi {resi}"]
    if chain:
        clauses.append(f"chain {chain}")
    return "(" + " and ".join(clauses) + ")"


def read_highlight_residues(path: Path | None, top: int) -> list[str]:
    if not path or not path.exists():
        return []
    residues: list[tuple[str, float]] = []
    if path.suffix.lower() == ".csv":
        with path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                token = row.get("residue") or row.get("Residue") or row.get("residue_id") or ""
                value = row.get("total") or row.get("TOTAL") or row.get("delta_total") or "0"
                try:
                    score = abs(float(value))
                except ValueError:
                    score = 0.0
                if token:
                    residues.append((token, score))
        residues.sort(key=lambda item: item[1], reverse=True)
        return [item[0] for item in residues[:top]]
    return [line.strip() for line in path.read_text(encoding="utf-8", errors="ignore").splitlines() if line.strip()][:top]


def build_pml(args: argparse.Namespace, pml_file: Path, png_file: Path, pse_file: Path) -> None:
    style = STYLE_TEMPLATE.read_text(encoding="utf-8") if STYLE_TEMPLATE.exists() else "bg_color white\n"
    residues = read_highlight_residues(args.highlight_residues, args.top_residues)
    selections = [selection for token in residues if (selection := residue_selection(token))]
    highlight_expr = " or ".join(selections) if selections else "none"
    ligand_selection = args.ligand_selection
    pml = f"""{style}
load {args.complex.as_posix()}, complex
remove solvent
hide everything
show cartoon, polymer.protein
color grey80, polymer.protein
select ligand, ({ligand_selection})
show sticks, ligand
color orange, ligand
select binding_site, byres (polymer.protein within {args.contact_cutoff:.2f} of ligand)
show sticks, binding_site
color lightblue, binding_site
select highlighted_residues, {highlight_expr}
show sticks, highlighted_residues
color magenta, highlighted_residues
distance polar_contacts, ligand, polymer.protein, mode=2
set dash_color, black, polar_contacts
set label_color, black, polar_contacts
label (binding_site and name CA), "%s%s" % (resn, resi)
orient ligand or binding_site
zoom ligand or binding_site, {args.zoom_buffer:.2f}
png {png_file.as_posix()}, width={args.width}, height={args.height}, dpi={args.dpi}, ray=1
save {pse_file.as_posix()}
save {pml_file.as_posix()}
quit
"""
    pml_file.write_text(pml, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--complex", required=True, type=Path, help="Complex PDB.")
    parser.add_argument("--ligand-selection", default="organic", help='PyMOL selection, e.g. "resn LIG".')
    parser.add_argument("--outdir", default="figures", type=Path)
    parser.add_argument("--prefix", default="publication_3d")
    parser.add_argument("--highlight-residues", type=Path, help="CSV or text residue list, including MMPBSA decomposition CSV.")
    parser.add_argument("--top-residues", type=int, default=10)
    parser.add_argument("--contact-cutoff", type=float, default=5.0)
    parser.add_argument("--zoom-buffer", type=float, default=8.0)
    parser.add_argument("--width", type=int, default=2400)
    parser.add_argument("--height", type=int, default=1800)
    parser.add_argument("--dpi", type=int, default=300)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    args.outdir.mkdir(parents=True, exist_ok=True)
    pml_file = args.outdir / "scene.pml"
    png_file = args.outdir / f"{args.prefix}.png"
    pse_file = args.outdir / f"{args.prefix}.pse"
    build_pml(args, pml_file, png_file, pse_file)

    if args.dry_run:
        print(f"PyMOL script written: {pml_file}")
        return 0
    pymol = shutil.which("pymol")
    if not pymol:
        raise SystemExit("Required tool not found in PATH: pymol")
    log_file = args.outdir / f"{args.prefix}_pymol.log"
    cmd = [pymol, "-cq", str(pml_file)]
    with log_file.open("w", encoding="utf-8") as handle:
        proc = subprocess.run(cmd, text=True, stdout=handle, stderr=subprocess.STDOUT, check=False)
    if proc.returncode != 0:
        raise SystemExit(f"PyMOL failed; see log: {log_file}")
    print(f"PNG: {png_file}")
    print(f"PSE: {pse_file}")
    print(f"PML: {pml_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
