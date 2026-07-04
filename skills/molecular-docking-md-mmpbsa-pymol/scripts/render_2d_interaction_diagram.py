#!/usr/bin/env python3
"""Render a Maestro-like 2D ligand interaction diagram."""

from __future__ import annotations

import argparse
import base64
import csv
import html
import json
import math
import re
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_STYLE = SKILL_DIR / "assets" / "maestro_like_2d_style.json"

HYDROPHOBIC = {"ALA", "VAL", "LEU", "ILE", "MET", "PHE", "TRP", "PRO", "TYR", "CYS"}
POLAR = {"SER", "THR", "ASN", "GLN", "HIS", "GLY"}
ACIDIC = {"ASP", "GLU"}
BASIC = {"LYS", "ARG", "HIP", "HID", "HIE"}
WATERS = {"HOH", "WAT", "SOL", "H2O"}

INTERACTION_ALIASES = {
    "hydrogen_bonds": "hydrogen_bond",
    "hydrogen_bond": "hydrogen_bond",
    "hydrogenbond": "hydrogen_bond",
    "hbond": "hydrogen_bond",
    "hbonds": "hydrogen_bond",
    "hydrophobic_interactions": "hydrophobic",
    "hydrophobic_interaction": "hydrophobic",
    "hydrophobic": "hydrophobic",
    "pistacking": "pi_stacking",
    "pi_stacks": "pi_stacking",
    "pi_stack": "pi_stacking",
    "pi_stacking": "pi_stacking",
    "pi-stacking": "pi_stacking",
    "pi_cation_interactions": "pi_cation",
    "pi_cation_interaction": "pi_cation",
    "pi-cation": "pi_cation",
    "pication": "pi_cation",
    "salt_bridges": "salt_bridge",
    "salt_bridge": "salt_bridge",
    "saltbridge": "salt_bridge",
    "halogen_bonds": "halogen_bond",
    "halogen_bond": "halogen_bond",
    "water_bridges": "water_bridge",
    "water_bridge": "water_bridge",
    "metal_complexes": "metal_complex",
    "metal_complex": "metal_complex",
}


@dataclass
class Interaction:
    residue: str
    resname: str
    chain: str
    resnum: str
    interaction_type: str
    ligand_atom: int | None = None
    distance: float | None = None
    source: str = "unknown"


def load_style(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def residue_class(resname: str) -> str:
    resname = resname.upper()
    if resname in ACIDIC:
        return "acidic"
    if resname in BASIC:
        return "basic"
    if resname in HYDROPHOBIC:
        return "hydrophobic"
    if resname in POLAR:
        return "polar"
    return "unknown"


def normalize_interaction_type(value: str) -> str:
    key = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return INTERACTION_ALIASES.get(key, key if key in INTERACTION_ALIASES.values() else "contact")


def residue_id(resname: str, chain: str, resnum: str) -> str:
    chain_part = f"{chain}:" if chain else ""
    return f"{chain_part}{resname.upper()}{resnum}"


def read_ligand_mol(path: Path | None, complex_path: Path | None, ligand_resname: str | None):
    try:
        from rdkit import Chem
        from rdkit.Chem import AllChem
    except ImportError as exc:
        raise SystemExit("RDKit is required for 2D ligand diagrams. Install the mol-mmpbsa environment.") from exc

    mol = None
    if path:
        suffix = path.suffix.lower()
        if suffix in {".sdf", ".sd"}:
            supplier = Chem.SDMolSupplier(str(path), removeHs=False)
            mol = next((item for item in supplier if item is not None), None)
        elif suffix == ".mol2":
            mol = Chem.MolFromMol2File(str(path), sanitize=True, removeHs=False)
        elif suffix in {".mol", ".mdl"}:
            mol = Chem.MolFromMolFile(str(path), sanitize=True, removeHs=False)
        elif suffix == ".pdb":
            mol = Chem.MolFromPDBFile(str(path), sanitize=True, removeHs=False)
        elif suffix in {".smi", ".smiles"}:
            smiles = path.read_text(encoding="utf-8", errors="ignore").split()[0]
            mol = Chem.MolFromSmiles(smiles)
            if mol is not None:
                mol = Chem.AddHs(mol)
        if mol is None:
            raise SystemExit(f"Could not read ligand molecule: {path}")
    elif complex_path:
        block = extract_ligand_pdb_block(complex_path, ligand_resname)
        mol = Chem.MolFromPDBBlock(block, sanitize=True, removeHs=False)
        if mol is None:
            mol = Chem.MolFromPDBBlock(block, sanitize=False, removeHs=False)
    else:
        raise SystemExit("Provide --ligand or --complex.")

    if mol is None:
        raise SystemExit("Could not build an RDKit ligand molecule.")
    try:
        Chem.SanitizeMol(mol)
    except Exception:
        pass
    AllChem.Compute2DCoords(mol)
    return mol


def extract_ligand_pdb_block(complex_path: Path, ligand_resname: str | None) -> str:
    chosen: list[str] = []
    first_residue: tuple[str, str, str] | None = None
    for line in complex_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.startswith("HETATM"):
            continue
        resname = line[17:20].strip()
        if resname in WATERS:
            continue
        chain = line[21].strip()
        resnum = line[22:26].strip()
        key = (resname, chain, resnum)
        if ligand_resname and resname.upper() != ligand_resname.upper():
            continue
        if first_residue is None:
            first_residue = key
        if key == first_residue:
            chosen.append(line)
    if not chosen:
        raise SystemExit(f"No ligand HETATM records found in {complex_path}")
    return "\n".join(chosen) + "\nEND\n"


def child_text(elem: ET.Element, names: set[str]) -> str:
    for child in elem.iter():
        tag = child.tag.split("}")[-1].lower()
        if tag in names and child.text:
            return child.text.strip()
    return ""


def parse_ligand_atom(elem: ET.Element) -> int | None:
    keys = {
        "ligatomidx",
        "ligcarbonidx",
        "ligcoo",
        "acceptoridx",
        "donoridx",
        "lig_idx",
        "ligand_atom",
    }
    for child in elem.iter():
        tag = child.tag.split("}")[-1].lower()
        if tag not in keys or not child.text:
            continue
        numbers = re.findall(r"\d+", child.text)
        if numbers:
            value = int(numbers[0])
            return value - 1 if value > 0 else value
    return None


def parse_plip_xml(path: Path) -> list[Interaction]:
    interactions: list[Interaction] = []
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return interactions
    for elem in root.iter():
        tag = elem.tag.split("}")[-1].lower()
        interaction_type = INTERACTION_ALIASES.get(tag)
        if not interaction_type:
            continue
        resname = child_text(elem, {"restype", "resname", "restype_l"})
        resnum = child_text(elem, {"resnr", "resnum", "residue_number"})
        chain = child_text(elem, {"reschain", "chain"})
        dist_text = child_text(elem, {"dist", "distance"})
        distance = None
        if dist_text:
            match = re.search(r"[-+]?\d+(?:\.\d+)?", dist_text)
            distance = float(match.group(0)) if match else None
        if resname and resnum:
            interactions.append(
                Interaction(
                    residue=residue_id(resname, chain, resnum),
                    resname=resname.upper(),
                    chain=chain,
                    resnum=resnum,
                    interaction_type=interaction_type,
                    ligand_atom=parse_ligand_atom(elem),
                    distance=distance,
                    source=f"PLIP XML:{path.name}",
                )
            )
    return interactions


def parse_plip_txt(path: Path) -> list[Interaction]:
    interactions: list[Interaction] = []
    current_type = "contact"
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        lower = line.lower()
        for alias, normalized in INTERACTION_ALIASES.items():
            if alias.replace("_", " ") in lower or alias.replace("_", "-") in lower:
                current_type = normalized
                break
        match = re.search(r"\b([A-Z]{3})\s+([A-Za-z]?)\s*:?\s*(-?\d+[A-Za-z]?)\b", line)
        if not match:
            match = re.search(r"\b([A-Za-z]?)\s*:?\s*([A-Z]{3})\s*(-?\d+[A-Za-z]?)\b", line)
            if match:
                chain, resname, resnum = match.groups()
            else:
                continue
        else:
            resname, chain, resnum = match.groups()
        distance = None
        dist_match = re.search(r"\b(\d+\.\d+)\b", line)
        if dist_match:
            distance = float(dist_match.group(1))
        interactions.append(
            Interaction(
                residue=residue_id(resname, chain, resnum),
                resname=resname.upper(),
                chain=chain,
                resnum=resnum,
                interaction_type=current_type,
                distance=distance,
                source=f"PLIP TXT:{path.name}",
            )
        )
    return interactions


def parse_prolif_table(path: Path) -> list[Interaction]:
    interactions: list[Interaction] = []
    if path.suffix.lower() == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        rows = data if isinstance(data, list) else data.get("interactions", [])
    else:
        with path.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
    for row in rows:
        lowered = {str(k).lower(): v for k, v in dict(row).items()}
        residue = str(lowered.get("residue") or lowered.get("protein") or lowered.get("resid") or "")
        interaction_type = str(lowered.get("interaction") or lowered.get("interaction_type") or lowered.get("type") or "contact")
        if not residue:
            continue
        match = re.search(r"(?:(?P<chain>[A-Za-z0-9])[:/_-])?(?P<resname>[A-Za-z]{3})[:/_-]?(?P<resnum>-?\d+[A-Za-z]?)", residue)
        if match:
            chain = match.group("chain") or str(lowered.get("chain") or "")
            resname = match.group("resname").upper()
            resnum = match.group("resnum")
        else:
            resname = str(lowered.get("resname") or "UNK").upper()
            chain = str(lowered.get("chain") or "")
            resnum = str(lowered.get("resnum") or lowered.get("residue_number") or "")
        distance = None
        try:
            distance = float(lowered.get("distance") or lowered.get("dist") or "")
        except ValueError:
            pass
        ligand_atom = None
        try:
            ligand_atom = int(lowered.get("ligand_atom") or lowered.get("ligand_atom_index") or "")
        except ValueError:
            pass
        interactions.append(
            Interaction(
                residue=residue_id(resname, chain, resnum),
                resname=resname,
                chain=chain,
                resnum=resnum,
                interaction_type=normalize_interaction_type(interaction_type),
                ligand_atom=ligand_atom,
                distance=distance,
                source=f"ProLIF:{path.name}",
            )
        )
    return interactions


def find_plip_files(plip_dir: Path | None, explicit_xml: Path | None, explicit_txt: Path | None) -> tuple[list[Path], list[Path]]:
    xml_files = [explicit_xml] if explicit_xml else []
    txt_files = [explicit_txt] if explicit_txt else []
    if plip_dir and plip_dir.exists():
        xml_files.extend(sorted(plip_dir.rglob("*.xml")))
        txt_files.extend(sorted(plip_dir.rglob("*.txt")))
    return ([p for p in xml_files if p and p.exists()], [p for p in txt_files if p and p.exists()])


def collect_interactions(args: argparse.Namespace) -> tuple[list[Interaction], str]:
    interactions: list[Interaction] = []
    xml_files, txt_files = find_plip_files(args.plip_dir, args.plip_xml, args.plip_txt)
    for path in xml_files:
        interactions.extend(parse_plip_xml(path))
    if interactions:
        return dedupe_interactions(interactions), "PLIP"
    for path in txt_files:
        interactions.extend(parse_plip_txt(path))
    if interactions:
        return dedupe_interactions(interactions), "PLIP"
    if args.prolif:
        interactions.extend(parse_prolif_table(args.prolif))
        if interactions:
            return dedupe_interactions(interactions), "ProLIF"
    interactions.extend(run_prolif_if_possible(args.complex, args.ligand_resname))
    if interactions:
        return dedupe_interactions(interactions), "ProLIF"
    interactions.extend(geometric_contacts(args.complex, args.ligand_resname, args.contact_cutoff))
    return dedupe_interactions(interactions), "geometric fallback"


def dedupe_interactions(interactions: list[Interaction]) -> list[Interaction]:
    seen: set[tuple[str, str, int | None]] = set()
    output: list[Interaction] = []
    for item in interactions:
        key = (item.residue, item.interaction_type, item.ligand_atom)
        if key in seen:
            continue
        seen.add(key)
        output.append(item)
    return output


def run_prolif_if_possible(complex_path: Path | None, ligand_resname: str | None) -> list[Interaction]:
    if not complex_path or not complex_path.exists() or not ligand_resname:
        return []
    try:
        import MDAnalysis as mda
        import prolif as plf
    except ImportError:
        return []
    try:
        universe = mda.Universe(str(complex_path))
        protein = universe.select_atoms("protein")
        ligand = universe.select_atoms(f"resname {ligand_resname}")
        if len(protein) == 0 or len(ligand) == 0:
            return []
        fp = plf.Fingerprint()
        fp.run(universe.trajectory[:1], ligand, protein)
        table = fp.to_dataframe()
    except Exception:
        return []
    interactions: list[Interaction] = []
    if getattr(table, "empty", True):
        return interactions
    try:
        stacked = table.stack()
    except Exception:
        return interactions
    for index, value in stacked.items():
        if not bool(value):
            continue
        text = " ".join(str(part) for part in index if part is not None)
        match = re.search(r"(?:(?P<chain>[A-Za-z0-9])[:/_-])?(?P<resname>[A-Za-z]{3})[:/_-]?(?P<resnum>-?\d+[A-Za-z]?)", text)
        if not match:
            continue
        interaction_type = normalize_interaction_type(str(index[-1]))
        interactions.append(
            Interaction(
                residue=residue_id(match.group("resname"), match.group("chain") or "", match.group("resnum")),
                resname=match.group("resname").upper(),
                chain=match.group("chain") or "",
                resnum=match.group("resnum"),
                interaction_type=interaction_type,
                source="ProLIF direct",
            )
        )
    return interactions


def parse_pdb_atoms(path: Path) -> list[dict[str, Any]]:
    atoms: list[dict[str, Any]] = []
    if not path:
        return atoms
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.startswith(("ATOM", "HETATM")):
            continue
        try:
            atoms.append(
                {
                    "record": line[:6].strip(),
                    "atom": line[12:16].strip(),
                    "resname": line[17:20].strip().upper(),
                    "chain": line[21].strip(),
                    "resnum": line[22:26].strip(),
                    "x": float(line[30:38]),
                    "y": float(line[38:46]),
                    "z": float(line[46:54]),
                }
            )
        except ValueError:
            continue
    return atoms


def geometric_contacts(complex_path: Path | None, ligand_resname: str | None, cutoff: float) -> list[Interaction]:
    if not complex_path or not complex_path.exists():
        return []
    atoms = parse_pdb_atoms(complex_path)
    ligand_atoms = [
        atom
        for atom in atoms
        if atom["record"] == "HETATM"
        and atom["resname"] not in WATERS
        and (not ligand_resname or atom["resname"] == ligand_resname.upper())
    ]
    protein_atoms = [atom for atom in atoms if atom["record"] == "ATOM"]
    if not ligand_atoms or not protein_atoms:
        return []
    best: dict[tuple[str, str, str], float] = {}
    for latom in ligand_atoms:
        for patom in protein_atoms:
            dx = latom["x"] - patom["x"]
            dy = latom["y"] - patom["y"]
            dz = latom["z"] - patom["z"]
            dist = math.sqrt(dx * dx + dy * dy + dz * dz)
            if dist <= cutoff:
                key = (patom["resname"], patom["chain"], patom["resnum"])
                best[key] = min(best.get(key, dist), dist)
    interactions = []
    for (resname, chain, resnum), dist in sorted(best.items(), key=lambda item: item[1])[:24]:
        interactions.append(
            Interaction(
                residue=residue_id(resname, chain, resnum),
                resname=resname,
                chain=chain,
                resnum=resnum,
                interaction_type="hydrophobic" if residue_class(resname) == "hydrophobic" else "contact",
                distance=dist,
                source=f"distance <= {cutoff:.1f} A",
            )
        )
    return interactions


def draw_ligand_svg(mol, width: int, height: int, style: dict[str, Any]) -> tuple[str, dict[int, tuple[float, float]]]:
    from rdkit.Chem.Draw import rdMolDraw2D

    drawer = rdMolDraw2D.MolDraw2DSVG(width, height)
    options = drawer.drawOptions()
    options.bondLineWidth = float(style["ligand"].get("bond_line_width", 2.0))
    options.atomLabelFontSize = int(style["ligand"].get("atom_label_font_size", 18))
    rdMolDraw2D.PrepareAndDrawMolecule(drawer, mol)
    coords: dict[int, tuple[float, float]] = {}
    for idx in range(mol.GetNumAtoms()):
        point = drawer.GetDrawCoords(idx)
        coords[idx] = (float(point.x), float(point.y))
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText().replace("svg:", "")
    match = re.search(r"<svg[^>]*>(.*)</svg>", svg, flags=re.S)
    body = match.group(1) if match else svg
    return body, coords


def place_residues(interactions: list[Interaction], width: int, height: int, ligand_box: tuple[float, float, float, float]) -> dict[str, tuple[float, float]]:
    residues = []
    for item in interactions:
        if item.residue not in residues:
            residues.append(item.residue)
    count = max(len(residues), 1)
    cx = width / 2
    cy = height / 2 - 10
    rx = max(430, (ligand_box[2] - ligand_box[0]) * 0.95)
    ry = max(300, (ligand_box[3] - ligand_box[1]) * 1.05)
    positions: dict[str, tuple[float, float]] = {}
    for i, residue in enumerate(residues):
        angle = -math.pi / 2 + 2 * math.pi * i / count
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle)
        x = min(max(70, x), width - 70)
        y = min(max(70, y), height - 150)
        positions[residue] = (x, y)
    return positions


def line_anchor(atom_coords: dict[int, tuple[float, float]], ligand_offset: tuple[float, float], item: Interaction, residue_xy: tuple[float, float], center_xy: tuple[float, float]) -> tuple[float, float]:
    if item.ligand_atom is not None and item.ligand_atom in atom_coords:
        x, y = atom_coords[item.ligand_atom]
        return x + ligand_offset[0], y + ligand_offset[1]
    cx, cy = center_xy
    rx, ry = residue_xy
    dx = rx - cx
    dy = ry - cy
    length = math.sqrt(dx * dx + dy * dy) or 1.0
    return cx + dx / length * 185, cy + dy / length * 135


def svg_text(x: float, y: float, text: str, size: int, weight: str = "normal", anchor: str = "middle") -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" '
        f'font-size="{size}" font-weight="{weight}" font-family="Arial, Helvetica, sans-serif" '
        f'fill="#202124">{html.escape(text)}</text>'
    )


def render_svg(mol, interactions: list[Interaction], source: str, style: dict[str, Any], output_svg: Path) -> dict[str, Any]:
    width = int(style["canvas"]["width"])
    height = int(style["canvas"]["height"])
    ligand_w = int(style["ligand"]["width"])
    ligand_h = int(style["ligand"]["height"])
    ligand_body, atom_coords = draw_ligand_svg(mol, ligand_w, ligand_h, style)
    ligand_x = (width - ligand_w) / 2
    ligand_y = (height - ligand_h) / 2 + float(style["ligand"].get("offset_y", 0))
    ligand_box = (ligand_x, ligand_y, ligand_x + ligand_w, ligand_y + ligand_h)
    center_xy = (width / 2, ligand_y + ligand_h / 2)
    positions = place_residues(interactions, width, height, ligand_box)
    bubble_style = style["residue_bubbles"]
    radius = float(bubble_style["radius"])
    elements: list[str] = []
    elements.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">')
    elements.append(f'<rect width="100%" height="100%" fill="{style["canvas"]["background"]}"/>')
    elements.append("<defs>")
    elements.append('<marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth"><path d="M0,0 L0,6 L9,3 z" fill="#202124"/></marker>')
    elements.append("</defs>")
    if style.get("pocket", {}).get("enabled", True):
        pocket = style["pocket"]
        elements.append(
            f'<ellipse cx="{center_xy[0]:.1f}" cy="{center_xy[1]:.1f}" rx="330" ry="235" '
            f'fill="{pocket["fill"]}" fill-opacity="{pocket["fill_opacity"]}" stroke="{pocket["stroke"]}" '
            f'stroke-width="{pocket["stroke_width"]}" stroke-dasharray="{pocket["dasharray"]}"/>'
        )
    for item in interactions:
        residue_xy = positions.get(item.residue)
        if not residue_xy:
            continue
        anchor = line_anchor(atom_coords, (ligand_x, ligand_y), item, residue_xy, center_xy)
        interaction_style = style["interactions"].get(item.interaction_type, style["interactions"]["contact"])
        marker = ' marker-end="url(#arrow)"' if interaction_style.get("arrow") else ""
        dash = interaction_style.get("dasharray", "")
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        elements.append(
            f'<line x1="{anchor[0]:.1f}" y1="{anchor[1]:.1f}" x2="{residue_xy[0]:.1f}" y2="{residue_xy[1]:.1f}" '
            f'stroke="{interaction_style["color"]}" stroke-width="{interaction_style["stroke_width"]}" '
            f'stroke-linecap="round"{dash_attr}{marker}/>'
        )
    elements.append(f'<g id="ligand" transform="translate({ligand_x:.1f},{ligand_y:.1f})">{ligand_body}</g>')
    for residue, (x, y) in positions.items():
        items = [item for item in interactions if item.residue == residue]
        first = items[0]
        fill = bubble_style.get(residue_class(first.resname), bubble_style["unknown"])
        label = f"{first.resname}{first.resnum}"
        if first.chain:
            label = f"{first.chain}:{label}"
        elements.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius:.1f}" fill="{fill}" '
            f'stroke="{bubble_style["stroke"]}" stroke-width="{bubble_style["stroke_width"]}"/>'
        )
        elements.append(svg_text(x, y - 3, label, int(bubble_style["font_size"]), "bold"))
        type_labels = sorted({style["interactions"].get(item.interaction_type, style["interactions"]["contact"])["label"] for item in items})
        elements.append(svg_text(x, y + 18, ", ".join(type_labels)[:22], int(bubble_style["subfont_size"])))
    if style.get("legend", {}).get("enabled", True):
        lx = float(style["legend"]["x"])
        ly = float(style["legend"]["y"])
        elements.append(svg_text(lx, ly, "Residue class", int(style["legend"]["font_size"]), "bold", "start"))
        legend_rows = [("Hydrophobic", "hydrophobic"), ("Polar", "polar"), ("Acidic", "acidic"), ("Basic", "basic")]
        for i, (label, key) in enumerate(legend_rows):
            y = ly + 24 + 24 * i
            elements.append(f'<rect x="{lx:.1f}" y="{y - 13:.1f}" width="18" height="18" rx="9" fill="{bubble_style[key]}" stroke="{bubble_style["stroke"]}"/>')
            elements.append(svg_text(lx + 28, y + 1, label, int(style["legend"]["font_size"]), "normal", "start"))
        elements.append(svg_text(width - 34, height - 28, f"Maestro-like 2D diagram; source: {source}", 13, "normal", "end"))
    elements.append("</svg>")
    output_svg.write_text("\n".join(elements), encoding="utf-8")
    return {"width": width, "height": height, "source": source, "residue_count": len(positions)}


def write_png(svg_file: Path, png_file: Path) -> None:
    try:
        import cairosvg
    except ImportError as exc:
        raise SystemExit("cairosvg is required to write PNG output. Install it or use the SVG output.") from exc
    cairosvg.svg2png(url=str(svg_file), write_to=str(png_file), dpi=300)


def write_csv(interactions: list[Interaction], output: Path) -> None:
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["residue", "resname", "chain", "resnum", "property", "interaction_type", "ligand_atom", "distance", "source"],
        )
        writer.writeheader()
        for item in interactions:
            row = asdict(item)
            row["property"] = residue_class(item.resname)
            writer.writerow(row)


def write_json(interactions: list[Interaction], metadata: dict[str, Any], output: Path) -> None:
    payload = {
        "note": "Maestro-like diagram generated with open-source tooling; not a Schrodinger/Maestro output unless a licensed Schrodinger workflow was explicitly used.",
        "metadata": metadata,
        "interactions": [asdict(item) | {"property": residue_class(item.resname)} for item in interactions],
    }
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def maybe_write_schrodinger_note(output_dir: Path) -> None:
    import os
    import shutil

    schrodinger = os.environ.get("SCHRODINGER")
    commands = {name: shutil.which(name) for name in ["maestro", "run", "structconvert", "prepwizard"]}
    available = {name: path for name, path in commands.items() if path}
    if schrodinger or available:
        note = {
            "SCHRODINGER": schrodinger,
            "commands": available,
            "policy": "Detected only as an optional licensed route. This script does not bypass licensing and does not require Schrodinger.",
        }
        (output_dir / "schrodinger_optional_detection.json").write_text(json.dumps(note, indent=2), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--complex", type=Path, help="Protein-ligand complex PDB.")
    parser.add_argument("--receptor", type=Path, help="Optional receptor PDB for documentation.")
    parser.add_argument("--ligand", type=Path, help="Ligand SDF/MOL2/PDB/SMI. Prefer this for accurate 2D chemistry.")
    parser.add_argument("--ligand-resname", default="LIG")
    parser.add_argument("--plip-xml", type=Path)
    parser.add_argument("--plip-txt", type=Path)
    parser.add_argument("--plip-dir", type=Path)
    parser.add_argument("--prolif", type=Path, help="ProLIF CSV or JSON.")
    parser.add_argument("--style", default=DEFAULT_STYLE, type=Path)
    parser.add_argument("--outdir", default="figures", type=Path)
    parser.add_argument("--prefix", default="ligand_interaction_2d")
    parser.add_argument("--contact-cutoff", type=float, default=4.2)
    args = parser.parse_args()

    if not args.complex and not args.ligand:
        raise SystemExit("Provide --complex or --ligand.")
    args.outdir.mkdir(parents=True, exist_ok=True)
    style = load_style(args.style)
    mol = read_ligand_mol(args.ligand, args.complex, args.ligand_resname)
    interactions, source = collect_interactions(args)
    if not interactions:
        interactions = [
            Interaction(
                residue="UNK0",
                resname="UNK",
                chain="",
                resnum="0",
                interaction_type="contact",
                source="no interaction source found",
            )
        ]
        source = "none"
    svg_file = args.outdir / f"{args.prefix}.svg"
    png_file = args.outdir / f"{args.prefix}.png"
    csv_file = args.outdir / f"{args.prefix}.csv"
    json_file = args.outdir / f"{args.prefix}.json"
    metadata = render_svg(mol, interactions, source, style, svg_file)
    write_png(svg_file, png_file)
    write_csv(interactions, csv_file)
    write_json(interactions, metadata, json_file)
    maybe_write_schrodinger_note(args.outdir)
    print(f"2D SVG: {svg_file}")
    print(f"2D PNG: {png_file}")
    print(f"2D CSV: {csv_file}")
    print(f"2D JSON: {json_file}")
    print("Note: output is Maestro-like and was not generated by Schrodinger/Maestro unless you explicitly used a licensed Schrodinger route.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
