#!/usr/bin/env python3
"""Parse gmx_MMPBSA outputs and generate publication-ready CSV/PNG summaries."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ENERGY_NAMES = {
    "VDWAALS": "van_der_waals",
    "EEL": "electrostatic",
    "EGB": "polar_solvation_gb",
    "EPB": "polar_solvation_pb",
    "ESURF": "sasa_nonpolar",
    "ENPOLAR": "nonpolar_solvation",
    "EDISPER": "dispersion",
    "DELTA TOTAL": "delta_g_bind",
}


def parse_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def parse_summary(results: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not results.exists():
        return rows
    section = "unknown"
    pattern = re.compile(r"^\s*(DELTA TOTAL|VDWAALS|EEL|EGB|EPB|ESURF|ENPOLAR|EDISPER)\s+([-+0-9.Ee]+)(?:\s+([-+0-9.Ee]+))?")
    for line in results.read_text(encoding="utf-8", errors="ignore").splitlines():
        upper = line.upper()
        if "GENERALIZED BORN" in upper or "MM/GBSA" in upper or "GBSA" in upper:
            section = "gb"
        elif "POISSON" in upper or "MM/PBSA" in upper or "PBSA" in upper:
            section = "pb"
        match = pattern.match(line)
        if not match:
            continue
        value = parse_float(match.group(2))
        if value is None:
            continue
        sd = parse_float(match.group(3) or "")
        rows.append(
            {
                "section": section,
                "component": ENERGY_NAMES.get(match.group(1), match.group(1).lower()),
                "value_kcal_mol": f"{value:.6g}",
                "std_kcal_mol": "" if sd is None else f"{sd:.6g}",
            }
        )
    return rows


def write_summary(rows: list[dict[str, str]], output: Path) -> None:
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["section", "component", "value_kcal_mol", "std_kcal_mol"])
        writer.writeheader()
        writer.writerows(rows)


def normalize_decomp_csv(input_csv: Path) -> list[dict[str, str]]:
    try:
        import pandas as pd
    except ImportError:
        return []
    data = pd.read_csv(input_csv)
    if data.empty:
        return []
    cols = {col.lower().strip(): col for col in data.columns}
    residue_col = cols.get("residue") or cols.get("resid") or data.columns[0]
    total_col = None
    for key, col in cols.items():
        if key in {"total", "delta total", "delta_total"} or "total" == key.split()[-1]:
            total_col = col
    if total_col is None:
        numeric = data.select_dtypes(include="number")
        if numeric.empty:
            return []
        total_col = numeric.columns[-1]
    rows = []
    for _, row in data.iterrows():
        rows.append({"residue": str(row[residue_col]), "total": str(row[total_col])})
    return rows


def parse_decomp_dat(path: Path) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    if not path.exists():
        return rows
    line_re = re.compile(r"^\s*([A-Za-z0-9_:.+-]+)\s+(.+)$")
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        match = line_re.match(line)
        if not match:
            continue
        residue = match.group(1)
        numbers = [parse_float(item) for item in match.group(2).split()]
        values = [item for item in numbers if item is not None]
        if len(values) < 2:
            continue
        rows.append({"residue": residue, "total": f"{values[-1]:.6g}"})
    return rows


def write_decomp(rows: list[dict[str, str]], output: Path) -> None:
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["residue", "total"])
        writer.writeheader()
        writer.writerows(rows)


def plot_energy_summary(summary_csv: Path, png_file: Path) -> None:
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
        import seaborn as sns
    except ImportError:
        return
    data = pd.read_csv(summary_csv)
    if data.empty:
        return
    plot_data = data[data["component"] != "delta_g_bind"].copy()
    if plot_data.empty:
        return
    plot_data["value_kcal_mol"] = pd.to_numeric(plot_data["value_kcal_mol"], errors="coerce")
    plt.figure(figsize=(7, 4), dpi=160)
    sns.barplot(data=plot_data, x="component", y="value_kcal_mol", hue="section")
    plt.axhline(0, color="black", lw=0.8)
    plt.ylabel("Energy (kcal/mol)")
    plt.xlabel("")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(png_file, dpi=300)
    plt.close()


def plot_decomp(decomp_csv: Path, png_file: Path, top: int) -> None:
    try:
        import matplotlib.pyplot as plt
        import pandas as pd
        import seaborn as sns
    except ImportError:
        return
    data = pd.read_csv(decomp_csv)
    if data.empty or "total" not in data:
        return
    data["total"] = pd.to_numeric(data["total"], errors="coerce")
    data = data.dropna(subset=["total"])
    if data.empty:
        return
    data["abs_total"] = data["total"].abs()
    plot_data = data.sort_values("abs_total", ascending=False).head(top).sort_values("total")
    plt.figure(figsize=(7, max(4, 0.28 * len(plot_data))), dpi=160)
    sns.barplot(data=plot_data, x="total", y="residue", color="#4C78A8")
    plt.axvline(0, color="black", lw=0.8)
    plt.xlabel("Per-residue contribution (kcal/mol)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(png_file, dpi=300)
    plt.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", required=True, type=Path, help="FINAL_RESULTS_MMPBSA.dat")
    parser.add_argument("--decomp", type=Path, help="FINAL_DECOMP_MMPBSA.csv or .dat")
    parser.add_argument("--outdir", default="mmpbsa", type=Path)
    parser.add_argument("--top", type=int, default=20)
    args = parser.parse_args(argv)

    args.outdir.mkdir(parents=True, exist_ok=True)
    summary_rows = parse_summary(args.results)
    summary_csv = args.outdir / "summary_mmpbsa.csv"
    write_summary(summary_rows, summary_csv)
    plot_energy_summary(summary_csv, args.outdir / "publication_mmpbsa_summary.png")

    decomp_path = args.decomp
    if decomp_path is None:
        for candidate in ["FINAL_DECOMP_MMPBSA.csv", "FINAL_DECOMP_MMPBSA.dat"]:
            path = args.outdir / candidate
            if path.exists():
                decomp_path = path
                break
    if decomp_path:
        decomp_rows = normalize_decomp_csv(decomp_path) if decomp_path.suffix.lower() == ".csv" else parse_decomp_dat(decomp_path)
        if decomp_rows:
            decomp_csv = args.outdir / "per_residue_decomposition.csv"
            write_decomp(decomp_rows, decomp_csv)
            plot_decomp(decomp_csv, args.outdir / "residue_decomp_top20.png", args.top)

    print(f"Summary CSV: {summary_csv}")
    print(f"Energy plot: {args.outdir / 'publication_mmpbsa_summary.png'}")
    if (args.outdir / "per_residue_decomposition.csv").exists():
        print(f"Residue decomposition CSV: {args.outdir / 'per_residue_decomposition.csv'}")
        print(f"Residue plot: {args.outdir / 'residue_decomp_top20.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
