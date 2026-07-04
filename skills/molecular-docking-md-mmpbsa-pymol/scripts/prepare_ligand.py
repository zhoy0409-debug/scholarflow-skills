#!/usr/bin/env python3
"""Prepare an organic small-molecule ligand for target-protein docking and MD."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


METALS = {
    "Li",
    "Na",
    "K",
    "Rb",
    "Cs",
    "Mg",
    "Ca",
    "Sr",
    "Ba",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Cd",
    "Hg",
    "Al",
    "Ga",
    "In",
    "Sn",
    "Pb",
}
COMMON_ORGANIC = {"H", "B", "C", "N", "O", "F", "P", "S", "Cl", "Br", "I"}


def ensure_tool(name: str, required: bool = True) -> str:
    path = shutil.which(name)
    if not path and required:
        raise SystemExit(f"Required tool not found in PATH: {name}")
    return path or name


def run_command(cmd: list[str], log_file: Path, dry_run: bool = False) -> None:
    with log_file.open("a", encoding="utf-8") as handle:
        handle.write(" ".join(cmd) + "\n")
        if dry_run:
            return
        proc = subprocess.run(cmd, text=True, stdout=handle, stderr=subprocess.STDOUT, check=False)
    if proc.returncode != 0:
        raise SystemExit(f"Command failed; see log: {log_file}")


def infer_format(path: Path, smiles: str | None) -> str:
    if smiles is not None:
        return "smiles"
    suffix = path.suffix.lower().lstrip(".")
    if suffix in {"smi", "smiles"}:
        return "smiles"
    if suffix in {"sdf", "sd", "mol2", "pdb", "pdbqt", "mol"}:
        return suffix
    raise SystemExit(f"Unsupported ligand format: {path.suffix}. Use sdf, mol2, pdb, pdbqt, mol, or smiles.")


def read_smiles(path: Path | None, smiles: str | None) -> str:
    if smiles:
        return smiles.strip()
    if not path:
        raise SystemExit("SMILES input requires --smiles or a .smi/.smiles file.")
    text = path.read_text(encoding="utf-8", errors="ignore").strip()
    if not text:
        raise SystemExit(f"SMILES file is empty: {path}")
    return text.split()[0]


def smiles_to_sdf(smiles: str, output: Path) -> None:
    try:
        from rdkit import Chem
        from rdkit.Chem import AllChem
    except ImportError as exc:
        raise SystemExit("RDKit is required to generate a 3D ligand from SMILES.") from exc
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise SystemExit("RDKit could not parse the input SMILES.")
    mol = Chem.AddHs(mol)
    status = AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
    if status != 0:
        raise SystemExit("RDKit failed to generate a 3D conformer from SMILES.")
    AllChem.UFFOptimizeMolecule(mol, maxIters=500)
    writer = Chem.SDWriter(str(output))
    writer.write(mol)
    writer.close()


def molecule_metadata(sdf: Path) -> dict[str, object]:
    metadata: dict[str, object] = {
        "net_charge": "unknown",
        "formal_charge": "unknown",
        "chiral_centers": [],
        "elements": [],
        "warnings": [],
        "protonation_state": "input hydrogens preserved where possible; hydrogens added during preparation",
        "tautomer_state": "not intentionally changed",
    }
    try:
        from rdkit import Chem
    except ImportError:
        metadata["warnings"].append("RDKit unavailable; charge, chirality, and unusual-element checks were limited.")
        return metadata
    supplier = Chem.SDMolSupplier(str(sdf), removeHs=False)
    mol = next((item for item in supplier if item is not None), None)
    if mol is None:
        metadata["warnings"].append("RDKit could not read prepared SDF metadata.")
        return metadata
    formal_charge = sum(atom.GetFormalCharge() for atom in mol.GetAtoms())
    elements = sorted({atom.GetSymbol() for atom in mol.GetAtoms()})
    chiral = Chem.FindMolChiralCenters(mol, includeUnassigned=True, useLegacyImplementation=False)
    metadata["net_charge"] = formal_charge
    metadata["formal_charge"] = formal_charge
    metadata["chiral_centers"] = [{"atom_index": idx, "configuration": label} for idx, label in chiral]
    metadata["elements"] = elements
    warnings = metadata["warnings"]
    if any(element in METALS for element in elements):
        warnings.append("Ligand contains metal atoms; GAFF/ACPYPE parameterization may be unreliable.")
    unusual = [element for element in elements if element not in COMMON_ORGANIC and element not in METALS]
    if unusual:
        warnings.append(f"Ligand contains uncommon elements for routine GAFF workflow: {', '.join(unusual)}.")
    if "B" in elements:
        warnings.append("Ligand contains boron/boronic-acid-like chemistry; docking and GAFF parameters need manual review.")
    if abs(formal_charge) > 2:
        warnings.append("Ligand has high formal charge; protonation and parameterization need manual review.")
    oxygen_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == "O")
    carbon_count = sum(1 for atom in mol.GetAtoms() if atom.GetSymbol() == "C")
    if oxygen_count >= 5 and carbon_count >= 5:
        warnings.append("Ligand may contain complex glycoside/sugar-like chemistry; validate protonation and parameters.")
    if any(label == "?" for _, label in chiral):
        warnings.append("Ligand contains unassigned chiral centers; do not assume docking stereochemistry is reliable.")
    return metadata


def write_metadata(path: Path, payload: dict[str, object]) -> None:
    text_lines = [f"{key}={value}" for key, value in payload.items() if key != "warnings"]
    warnings = payload.get("warnings", [])
    if warnings:
        text_lines.append("warnings:")
        text_lines.extend(f"- {item}" for item in warnings)
    path.with_suffix(".txt").write_text("\n".join(text_lines) + "\n", encoding="utf-8")
    path.with_suffix(".json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ligand", type=Path, help="Input ligand: sdf, mol2, pdb, pdbqt, mol, smi/smiles.")
    parser.add_argument("--smiles", help="Input SMILES string. Used only when no 3D structure is provided.")
    parser.add_argument("--outdir", default="prepared", type=Path)
    parser.add_argument("--prefix", default="ligand")
    parser.add_argument("--resname", default="LIG")
    parser.add_argument("--ph", type=float, help="Optional OpenBabel pH for protonation. Avoid unless intentionally changing protonation.")
    parser.add_argument("--force-gen3d", action="store_true", help="Regenerate 3D even if the input is already 3D.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.ligand and not args.smiles:
        raise SystemExit("Provide --ligand or --smiles.")
    input_format = infer_format(args.ligand or Path("ligand.smi"), args.smiles)
    obabel = ensure_tool("obabel", required=not args.dry_run)
    meeko = ensure_tool("mk_prepare_ligand.py", required=not args.dry_run)
    args.outdir.mkdir(parents=True, exist_ok=True)
    log_file = args.outdir / "prepare_ligand.log"
    if log_file.exists():
        log_file.unlink()

    sdf = args.outdir / "ligand.sdf"
    mol2 = args.outdir / "ligand.mol2"
    pdbqt = args.outdir / "ligand.pdbqt"
    metadata_base = args.outdir / "ligand_metadata"

    if input_format == "smiles":
        smiles = read_smiles(args.ligand, args.smiles)
        if args.dry_run:
            log_file.write_text(f"RDKit SMILES -> 3D SDF: {smiles} -> {sdf}\n", encoding="utf-8")
        else:
            smiles_to_sdf(smiles, sdf)
        source_note = "SMILES input; RDKit ETKDG 3D conformer generated"
    else:
        source = args.ligand
        assert source is not None
        sdf_cmd = [obabel, str(source), "-O", str(sdf), "-h"]
        if args.force_gen3d:
            sdf_cmd.append("--gen3d")
        if args.ph is not None:
            sdf_cmd.extend(["-p", str(args.ph)])
        run_command(sdf_cmd, log_file, args.dry_run)
        source_note = "3D input retained where present; hydrogens added; tautomer/protonation not intentionally changed"

    run_command([obabel, str(sdf), "-O", str(mol2), "-h"], log_file, args.dry_run)
    run_command([meeko, "-i", str(sdf), "-o", str(pdbqt)], log_file, args.dry_run)

    metadata = {
        "input": str(args.ligand) if args.ligand else "SMILES",
        "input_format": input_format,
        "resname": args.resname,
        "ph": args.ph,
        "preparation": source_note,
        "outputs": {"sdf": str(sdf), "mol2": str(mol2), "pdbqt": str(pdbqt)},
        **({} if args.dry_run else molecule_metadata(sdf)),
    }
    if args.ph is not None:
        metadata.setdefault("warnings", []).append("OpenBabel pH option was used; verify protonation state manually.")
    else:
        metadata.setdefault("warnings", []).append("Protonation/tautomer state was not intentionally changed; verify if biological pH matters.")
    write_metadata(metadata_base, metadata)

    print(f"Prepared SDF: {sdf}")
    print(f"Prepared MOL2: {mol2}")
    print(f"Ligand PDBQT: {pdbqt}")
    print(f"Metadata: {metadata_base.with_suffix('.json')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
