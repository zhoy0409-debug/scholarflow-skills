from __future__ import annotations

import csv
import json
import os
import shutil
from collections import OrderedDict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SOURCE = Path(os.environ.get("ELIFE_SOURCE_DATA_1", ROOT / "source_data" / "Figure3_SourceData1_TypelabelsUMAP.csv"))
ADT_SOURCE = Path(os.environ.get("ELIFE_SOURCE_DATA_2", ROOT / "source_data" / "Figure3_SourceData2_ADTUMICounts.csv"))
OUT = ROOT / "generated"
FIGURES = OUT / "final_figures"
DATA = OUT / "source_data"
SOURCES = OUT / "figure_sources"
QA = OUT / "qa"
POLISHED = OUT / "polished_figures"
ARTICLE_URL = "https://elifesciences.org/articles/63632/figures"
DATA_URL = "https://cdn.elifesciences.org/articles/63632/elife-63632-fig3-data1-v2.zip"

ADT_LABELS = ["B.Naive", "B.Active", "Plasmablast", "T.CD4.Naive", "T.CD4.Memory", "T.CD4.CD45RO.CD45RA",
              "T.CD4.Exhausted", "T.CD8.Naive", "T.CD8.Effector", "T.CD8.Exhausted", "T.DoublePositive",
              "T.DoubleNegative", "NK", "DC.Myeloid", "Mono.CD14", "Mono.CD16"]
MARKERS = ["CD10", "CD185", "CD21", "CD24", "IgD", "IgM", "TCR.gd", "CD19", "CD40", "CD319", "CD38", "CD39",
           "CD71", "CD95", "CD197", "CD3", "TCR.ab", "CD4", "CD27", "CD8a", "KLRG1", "CD127", "CD45RO",
           "CD279", "CD56", "CD141", "FceRI", "HLA.DR", "CD11b", "CD11c", "CD14", "CD192", "CD269",
           "TCR.Va24.Ja18", "CD123", "CD16", "CD172a", "CD45RA", "CD86"]
POLISHED_COLORS = {
    "B.Naive": "#E86E45", "B.Activated": "#B54A6B", "B.Active": "#B54A6B", "Plasmablast": "#F0A429",
    "T.CD4.Naive": "#2F80ED", "T.CD4.Memory": "#00A878", "T.CD4.CD45RO.CD45RA": "#56CCF2",
    "T.CD4.Exhausted": "#58706B", "T.CD8.Naive": "#4A90E2", "T.CD8.Effector": "#254E9C",
    "T.CD8.Exhausted": "#7767C5", "T.DoublePositive": "#C65A9E", "T.DoubleNegative": "#13B886",
    "NK": "#78B22A", "DC.Myeloid": "#8E56D7", "Mono.CD14": "#B56EEA", "Mono.CD16": "#D26EFF",
}


def read_rows() -> list[dict[str, str]]:
    with SOURCE.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def plot_panel(rows: list[dict[str, str]], x_key: str, y_key: str, label_key: str, color_key: str, title: str, name: str) -> Path:
    grouped: OrderedDict[str, tuple[str, list[tuple[float, float]]]] = OrderedDict()
    for row in rows:
        if not row[x_key] or not row[y_key]:
            continue
        label = row[label_key]
        color = row[color_key]
        grouped.setdefault(label, (color, []))[1].append((float(row[x_key]), float(row[y_key])))
    fig, ax = plt.subplots(figsize=(12.6, 8.2))
    fig.suptitle(title, x=0.07, ha="left", fontsize=22, fontweight="bold", color="#10233F")
    cell_count = sum(len(points) for _, points in grouped.values())
    ax.set_title(f"Reproduced from article source data | n = {cell_count:,} cells", loc="left", fontsize=13, color="#61718A", pad=16)
    handles = []
    for label, (color, points) in grouped.items():
        x_values, y_values = zip(*points)
        ax.scatter(x_values, y_values, s=4.0, color=color, linewidth=0, alpha=0.92, rasterized=True)
        handles.append(Line2D([0], [0], marker="o", color="w", markerfacecolor=color, markersize=7, label=label))
    ax.set_xlabel("UMAP 1", fontsize=14)
    ax.set_ylabel("UMAP 2", fontsize=14)
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_linewidth(1.25)
    ax.tick_params(length=0, pad=7, labelsize=11, colors="#61718A")
    ax.set_aspect("equal", adjustable="datalim")
    ax.legend(handles=handles, title="Cell type", title_fontsize=12, fontsize=10, frameon=False,
              loc="upper left", bbox_to_anchor=(1.02, 1.0), borderaxespad=0, labelspacing=0.62, handletextpad=0.45)
    fig.subplots_adjust(right=0.74, top=0.83, bottom=0.12)
    output = FIGURES / name
    for suffix, kwargs in ((".png", {"dpi": 220}), (".svg", {}), (".pdf", {})):
        fig.savefig(output.with_suffix(suffix), bbox_inches="tight", pad_inches=0.16, facecolor="white", **kwargs)
    plt.close(fig)
    return output.with_suffix(".png")


def montage(paths: list[Path]) -> Path:
    tiles = []
    for path in paths:
        image = Image.open(path).convert("RGB")
        image.thumbnail((1000, 670))
        tiles.append(image.copy())
    canvas = Image.new("RGB", (2200, 860), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 38)
    draw.text((80, 42), "Published-figure reproduction | eLife Figure 3b and 3d", font=font, fill="#10233F")
    canvas.paste(tiles[0], (80, 130))
    canvas.paste(tiles[1], (1120, 130))
    output = QA / "elife-63632-figure3-umaps-montage.png"
    canvas.save(output, quality=96)
    return output


def median_xy(rows: list[dict[str, str]], x_key: str, y_key: str, label_key: str, labels: set[str]) -> tuple[float, float] | None:
    points = [(float(row[x_key]), float(row[y_key])) for row in rows if row[label_key] in labels and row[x_key] and row[y_key]]
    if not points:
        return None
    return tuple(np.median(np.array(points), axis=0))


def add_panel_label(ax: plt.Axes, label: str) -> None:
    ax.text(-0.20, 1.03, label, transform=ax.transAxes, fontsize=22, fontweight="bold", va="top", color="black")


def continuous_umap(ax: plt.Axes, rows: list[dict[str, str]], x_key: str, y_key: str, value_key: str, label: str) -> None:
    points = [(float(row[x_key]), float(row[y_key]), float(row[value_key])) for row in rows if row[x_key] and row[y_key] and row[value_key]]
    x_values, y_values, values = np.array(points).T
    if value_key == "adt_umis":
        values = np.log10(values + 1)
    scatter = ax.scatter(x_values, y_values, c=values, cmap="viridis", s=3.2, linewidth=0, rasterized=True)
    ax.set_xlabel(x_key.replace("_", " "), fontsize=11)
    ax.set_ylabel(y_key.replace("_", " "), fontsize=11)
    ax.set_aspect("equal", adjustable="datalim")
    colorbar = ax.figure.colorbar(scatter, ax=ax, orientation="horizontal", fraction=0.055, pad=0.08)
    colorbar.ax.tick_params(length=0, labelsize=8)
    colorbar.set_label(label, fontsize=9)


def categorical_umap(ax: plt.Axes, rows: list[dict[str, str]], x_key: str, y_key: str, label_key: str, color_key: str) -> None:
    groups: OrderedDict[str, tuple[str, list[tuple[float, float]]]] = OrderedDict()
    for row in rows:
        if not row[x_key] or not row[y_key]:
            continue
        groups.setdefault(row[label_key], (row[color_key], []))[1].append((float(row[x_key]), float(row[y_key])))
    for color, points in groups.values():
        x_values, y_values = zip(*points)
        ax.scatter(x_values, y_values, s=3.2, color=color, linewidth=0, rasterized=True)
    ax.set_xlabel(x_key.replace("_", " "), fontsize=11)
    ax.set_ylabel(y_key.replace("_", " "), fontsize=11)
    ax.set_aspect("equal", adjustable="datalim")


def full_figure_reproduction(rows: list[dict[str, str]]) -> Path:
    figure = plt.figure(figsize=(18.0, 10.4))
    grid = figure.add_gridspec(2, 3, width_ratios=[1.0, 1.0, 1.12], wspace=0.36, hspace=0.28)
    ax_a = figure.add_subplot(grid[0, 0])
    ax_b = figure.add_subplot(grid[0, 1])
    ax_c = figure.add_subplot(grid[1, 0])
    ax_d = figure.add_subplot(grid[1, 1])
    ax_e = figure.add_subplot(grid[:, 2])

    continuous_umap(ax_a, rows, "atac_umap_1", "atac_umap_2", "peaks_frac", "FRIP")
    categorical_umap(ax_b, rows, "atac_umap_1", "atac_umap_2", "atac_pbmc_type_label", "atac_pbmc_type_color")
    continuous_umap(ax_c, rows, "adt_umap_1", "adt_umap_2", "adt_umis", "log10(ADT UMIs + 1)")
    categorical_umap(ax_d, rows, "adt_umap_1", "adt_umap_2", "adt_manual_type_label", "adt_manual_type_color")
    for axis, label in ((ax_a, "a"), (ax_b, "b"), (ax_c, "c"), (ax_d, "d"), (ax_e, "e")):
        axis.spines[["top", "right"]].set_visible(False)
        axis.tick_params(length=0, labelsize=9, colors="#55657B")
        add_panel_label(axis, label)

    b_annotations = [
        ("T.CD4.Memory", {"T.CD4.Memory"}, (-4.8, -3.0)),
        ("T.CD4.Naive", {"T.CD4.Naive"}, (-4.6, 2.7)),
        ("B.Naive/Activated", {"B.Naive", "B.Activated"}, (-0.2, 8.0)),
        ("Mono.CD14/CD16", {"Mono.CD14", "Mono.CD16"}, (5.2, 2.6)),
        ("T.CD8.Naive/Effector\nand DoubleNegative", {"T.CD8.Naive", "T.CD8.Effector", "T.DoubleNegative"}, (-0.7, -1.3)),
        ("NK", {"NK"}, (1.4, -4.8)),
    ]
    for text, labels, location in b_annotations:
        point = median_xy(rows, "atac_umap_1", "atac_umap_2", "atac_pbmc_type_label", labels)
        if point is None:
            continue
        x_value, y_value = point
        ax_b.annotate(text, xy=(x_value, y_value), xytext=location, fontsize=8.6, ha="left", va="center",
                      arrowprops={"arrowstyle": "-", "color": "#1F2937", "lw": 0.8})

    d_annotations = [
        ("Mono.CD16", {"Mono.CD16"}, (-10.5, 11.4)), ("Mono.CD14", {"Mono.CD14"}, (-5.8, 11.4)),
        ("DC.Myeloid", {"DC.Myeloid"}, (-8.0, 7.5)), ("NK", {"NK"}, (-3.5, 0.2)),
        ("T.CD4.Memory", {"T.CD4.Memory"}, (4.4, 6.1)), ("T.CD4.Exhausted", {"T.CD4.Exhausted"}, (2.3, 4.5)),
        ("T.CD4.Naive", {"T.CD4.Naive"}, (3.5, -3.2)), ("T.DoubleNegative", {"T.DoubleNegative"}, (-2.2, 3.3)),
        ("T.DoublePositive", {"T.DoublePositive"}, (2.9, -7.0)), ("T.CD8.Naive", {"T.CD8.Naive"}, (4.5, -7.7)),
        ("T.CD8.Effector", {"T.CD8.Effector"}, (-5.2, -8.7)), ("T.CD8.Exhausted", {"T.CD8.Exhausted"}, (-7.2, -4.6)),
        ("B.Active", {"B.Active"}, (-9.8, -6.2)), ("B.Naive", {"B.Naive"}, (-9.8, -8.3)),
        ("Plasmablast", {"Plasmablast"}, (-12.3, -5.5)),
    ]
    for text, labels, location in d_annotations:
        point = median_xy(rows, "adt_umap_1", "adt_umap_2", "adt_manual_type_label", labels)
        if point is None:
            continue
        x_value, y_value = point
        ax_d.annotate(text, xy=(x_value, y_value), xytext=location, fontsize=7.8, ha="left", va="center",
                      arrowprops={"arrowstyle": "-", "color": "#1F2937", "lw": 0.7})

    adt_labels = ["B.Naive", "B.Active", "Plasmablast", "T.CD4.Naive", "T.CD4.Memory", "T.CD4.CD45RO.CD45RA",
                  "T.CD4.Exhausted", "T.CD8.Naive", "T.CD8.Effector", "T.CD8.Exhausted", "T.DoublePositive",
                  "T.DoubleNegative", "NK", "DC.Myeloid", "Mono.CD14", "Mono.CD16"]
    label_by_barcode = {row["barcodes"]: row["adt_manual_type_label"] for row in rows if row["adt_manual_type_label"]}
    color_by_label = {row["adt_manual_type_label"]: row["adt_manual_type_color"] for row in rows if row["adt_manual_type_label"]}
    values: dict[tuple[str, str], list[float]] = {}
    with ADT_SOURCE.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            cell_type = label_by_barcode.get(row["barcodes"])
            if cell_type in adt_labels and row["target"] != "total":
                values.setdefault((row["target"], cell_type), []).append(float(row["count"]))
    markers = ["CD10", "CD185", "CD21", "CD24", "IgD", "IgM", "TCR.gd", "CD19", "CD40", "CD319", "CD38", "CD39",
               "CD71", "CD95", "CD197", "CD3", "TCR.ab", "CD4", "CD27", "CD8a", "KLRG1", "CD127", "CD45RO",
               "CD279", "CD56", "CD141", "FceRI", "HLA.DR", "CD11b", "CD11c", "CD14", "CD192", "CD269",
               "TCR.Va24.Ja18", "CD123", "CD16", "CD172a", "CD45RA", "CD86"]
    matrix = np.array([[np.median(values.get((marker, cell_type), [0.0])) for cell_type in adt_labels] for marker in markers])
    matrix /= np.maximum(matrix.max(axis=1, keepdims=True), 1.0)
    heatmap = ax_e.imshow(matrix, cmap="plasma", aspect="auto", interpolation="nearest", vmin=0, vmax=1)
    ax_e.set_yticks(range(len(markers)), markers, fontsize=7.3)
    ax_e.set_xticks([])
    ax_e.tick_params(length=0)
    counts = [sum(1 for value in label_by_barcode.values() if value == cell_type) for cell_type in adt_labels]
    for index, (cell_type, count) in enumerate(zip(adt_labels, counts)):
        ax_e.text(index, -1.35, cell_type, rotation=90, ha="center", va="bottom", fontsize=7.2, color="#1F2937")
        ax_e.add_patch(plt.Rectangle((index - 0.5, -2.85), 1.0, 0.65, color=color_by_label[cell_type]))
        ax_e.text(index, -3.70, str(count), rotation=90, ha="center", va="center", fontsize=7.2, color="#1F2937")
    ax_e.text(-1.2, -3.70, "N cells", ha="right", va="center", fontsize=9, color="#1F2937")
    ax_e.set_ylim(len(markers) - 0.5, -4.35)
    for spine in ax_e.spines.values():
        spine.set_visible(False)
    colorbar = figure.colorbar(heatmap, ax=ax_e, orientation="horizontal", fraction=0.045, pad=0.05)
    colorbar.set_label("Frac. max. ADT UMIs", fontsize=8)
    colorbar.ax.tick_params(labelsize=7, length=0)
    figure.subplots_adjust(left=0.055, right=0.985, bottom=0.07, top=0.93)
    output = FIGURES / "figure3a-e-full-reproduction"
    for suffix, kwargs in ((".png", {"dpi": 240}), (".svg", {}), (".pdf", {})):
        figure.savefig(output.with_suffix(suffix), bbox_inches="tight", pad_inches=0.12, facecolor="white", **kwargs)
    plt.close(figure)
    return output.with_suffix(".png")


def polish_axes(ax: plt.Axes) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_linewidth(1.4)
    ax.tick_params(length=0, labelsize=11, colors="#607089", pad=7)
    ax.set_facecolor("#FFFFFF")


def polished_scatter(ax: plt.Axes, rows: list[dict[str, str]], x_key: str, y_key: str, title: str, value_key: str | None = None) -> None:
    if value_key:
        points = [(float(row[x_key]), float(row[y_key]), float(row[value_key])) for row in rows if row[x_key] and row[y_key] and row[value_key]]
        x_values, y_values, values = np.array(points).T
        if value_key == "adt_umis":
            values = np.log10(values + 1)
        scatter = ax.scatter(x_values, y_values, c=values, cmap="turbo", s=5.0, linewidth=0, alpha=0.94, rasterized=True)
        colorbar = ax.figure.colorbar(scatter, ax=ax, orientation="horizontal", fraction=0.052, pad=0.11)
        colorbar.outline.set_visible(False)
        colorbar.ax.tick_params(length=0, labelsize=9)
        colorbar.set_label("FRIP" if value_key == "peaks_frac" else "log10(ADT UMIs + 1)", fontsize=10, color="#10233F")
    else:
        label_key = "atac_pbmc_type_label" if x_key.startswith("atac") else "adt_manual_type_label"
        groups: OrderedDict[str, list[tuple[float, float]]] = OrderedDict()
        for row in rows:
            if row[x_key] and row[y_key] and row[label_key]:
                groups.setdefault(row[label_key], []).append((float(row[x_key]), float(row[y_key])))
        for label, points in groups.items():
            x_values, y_values = zip(*points)
            ax.scatter(x_values, y_values, s=5.0, color=POLISHED_COLORS.get(label, "#64748B"), linewidth=0, alpha=0.93, rasterized=True)
    polish_axes(ax)
    ax.set_aspect("equal", adjustable="datalim")
    ax.set_title(title, loc="left", fontsize=15, color="#10233F", fontweight="bold", pad=14)
    ax.set_xlabel("UMAP 1", fontsize=12, color="#10233F")
    ax.set_ylabel("UMAP 2", fontsize=12, color="#10233F")


def published_atlas_rerender(rows: list[dict[str, str]]) -> Path:
    figure, axes = plt.subplots(2, 2, figsize=(16.4, 12.2))
    figure.suptitle("Chromatin and surface-protein cell atlas", x=0.07, ha="left", fontsize=25, fontweight="bold", color="#10233F")
    figure.text(0.07, 0.934, "TEA-seq PBMC data re-rendered from the published Figure 3 source tables", fontsize=13, color="#607089")
    polished_scatter(axes[0, 0], rows, "atac_umap_1", "atac_umap_2", "Chromatin accessibility quality", "peaks_frac")
    polished_scatter(axes[0, 1], rows, "atac_umap_1", "atac_umap_2", "Chromatin accessibility cell states")
    polished_scatter(axes[1, 0], rows, "adt_umap_1", "adt_umap_2", "Surface-protein abundance", "adt_umis")
    polished_scatter(axes[1, 1], rows, "adt_umap_1", "adt_umap_2", "Surface-protein cell states")
    handles = [Line2D([0], [0], marker="o", color="w", markerfacecolor=POLISHED_COLORS[label], markersize=8, label=label.replace(".", " "))
               for label in ADT_LABELS]
    figure.legend(handles=handles, ncol=4, frameon=False, fontsize=12.5, loc="lower center", bbox_to_anchor=(0.5, 0.025),
                  columnspacing=1.6, handletextpad=0.35)
    figure.subplots_adjust(left=0.08, right=0.97, top=0.90, bottom=0.22, wspace=0.28, hspace=0.33)
    output = POLISHED / "figure3a-d-atlas-rerender"
    for suffix, kwargs in ((".png", {"dpi": 220}), (".svg", {}), (".pdf", {})):
        figure.savefig(output.with_suffix(suffix), bbox_inches="tight", pad_inches=0.16, facecolor="white", **kwargs)
    plt.close(figure)
    return output.with_suffix(".png")


def marker_matrix(rows: list[dict[str, str]]) -> tuple[np.ndarray, list[int]]:
    label_by_barcode = {row["barcodes"]: row["adt_manual_type_label"] for row in rows if row["adt_manual_type_label"]}
    values: dict[tuple[str, str], list[float]] = {}
    with ADT_SOURCE.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            cell_type = label_by_barcode.get(row["barcodes"])
            if cell_type in ADT_LABELS and row["target"] != "total":
                values.setdefault((row["target"], cell_type), []).append(float(row["count"]))
    matrix = np.array([[np.median(values.get((marker, cell_type), [0.0])) for cell_type in ADT_LABELS] for marker in MARKERS])
    matrix /= np.maximum(matrix.max(axis=1, keepdims=True), 1.0)
    counts = [sum(1 for cell_type in label_by_barcode.values() if cell_type == label) for label in ADT_LABELS]
    return matrix, counts


def display_label(label: str) -> str:
    labels = {
        "B.Naive": "B\nnaive", "B.Active": "B\nactive", "Plasmablast": "Plasma\nblast", "T.CD4.Naive": "CD4\nnaive",
        "T.CD4.Memory": "CD4\nmemory", "T.CD4.CD45RO.CD45RA": "CD4\nRO/RA", "T.CD4.Exhausted": "CD4\nexhausted",
        "T.CD8.Naive": "CD8\nnaive", "T.CD8.Effector": "CD8\neffector", "T.CD8.Exhausted": "CD8\nexhausted",
        "T.DoublePositive": "Double\npositive", "T.DoubleNegative": "Double\nnegative", "NK": "NK", "DC.Myeloid": "DC\nmyeloid",
        "Mono.CD14": "Mono\nCD14", "Mono.CD16": "Mono\nCD16",
    }
    return labels[label]


def published_heatmap_rerender(rows: list[dict[str, str]]) -> Path:
    matrix, counts = marker_matrix(rows)
    figure = plt.figure(figsize=(16.4, 12.0))
    grid = figure.add_gridspec(2, 1, height_ratios=[0.14, 1], hspace=0.035)
    header = figure.add_subplot(grid[0])
    ax = figure.add_subplot(grid[1])
    figure.suptitle("ADT marker architecture across cell types", x=0.075, ha="left", fontsize=25, fontweight="bold", color="#10233F")
    figure.text(0.075, 0.934, "Median ADT counts from the published TEA-seq Figure 3 source data, scaled within each marker", fontsize=13, color="#607089")
    image = ax.imshow(matrix, cmap="magma", vmin=0, vmax=1, aspect="auto", interpolation="nearest")
    ax.set_yticks(range(len(MARKERS)), MARKERS, fontsize=10.5, color="#334155")
    ax.set_xticks(range(len(ADT_LABELS)), [display_label(label) for label in ADT_LABELS], fontsize=9.5, color="#334155")
    ax.tick_params(length=0, pad=8)
    for spine in ax.spines.values():
        spine.set_visible(False)
    header.set_xlim(-0.5, len(ADT_LABELS) - 0.5)
    header.set_ylim(0, 1.25)
    for index, (label, count) in enumerate(zip(ADT_LABELS, counts)):
        header.add_patch(Rectangle((index - 0.42, 0.1), 0.84, 0.45, color=POLISHED_COLORS[label]))
        header.text(index, 0.77, f"{count}", ha="center", va="center", fontsize=10, color="#10233F", fontweight="bold")
    header.text(-0.83, 0.77, "Cells", ha="right", va="center", fontsize=10, color="#607089")
    header.axis("off")
    colorbar = figure.colorbar(image, ax=ax, orientation="horizontal", fraction=0.042, pad=0.075)
    colorbar.outline.set_visible(False)
    colorbar.ax.tick_params(length=0, labelsize=10)
    colorbar.set_label("Fraction of maximum ADT count per marker", fontsize=11, color="#10233F")
    figure.subplots_adjust(left=0.105, right=0.985, top=0.89, bottom=0.11)
    output = POLISHED / "figure3e-marker-heatmap-rerender"
    for suffix, kwargs in ((".png", {"dpi": 220}), (".svg", {}), (".pdf", {})):
        figure.savefig(output.with_suffix(suffix), bbox_inches="tight", pad_inches=0.16, facecolor="white", **kwargs)
    plt.close(figure)
    return output.with_suffix(".png")


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"Missing article source data: {SOURCE}")
    for directory in (FIGURES, DATA, SOURCES, QA, POLISHED):
        directory.mkdir(parents=True, exist_ok=True)
    rows = read_rows()
    outputs = [
        plot_panel(rows, "atac_umap_1", "atac_umap_2", "atac_pbmc_type_label", "atac_pbmc_type_color",
                   "TEA-seq Figure 3b | scATAC-seq cell-type UMAP", "figure3b-atac-umap-reproduction"),
        plot_panel(rows, "adt_umap_1", "adt_umap_2", "adt_manual_type_label", "adt_manual_type_color",
                   "TEA-seq Figure 3d | ADT cell-type UMAP", "figure3d-adt-umap-reproduction"),
    ]
    full = full_figure_reproduction(rows)
    polished = [published_atlas_rerender(rows), published_heatmap_rerender(rows)]
    overview = montage(outputs)
    assert all(path.exists() and path.stat().st_size > 10_000 for path in [*outputs, full, *polished, overview])
    shutil.copy2(SOURCE, DATA / SOURCE.name)
    shutil.copy2(Path(__file__), SOURCES / Path(__file__).name)
    metadata = {
        "status": "Published-figure reproduction from real article source data.",
        "article": "Swanson et al. (2021), Simultaneous trimodal single-cell measurement of transcripts, epitopes, and chromatin accessibility using TEA-seq, eLife 10:e63632.",
        "doi": "https://doi.org/10.7554/eLife.63632",
        "source_figure": "Figure 3a-e (individual b/d panels, full multi-panel reproduction, and polished source-data re-renders)",
        "article_url": ARTICLE_URL,
        "source_data_url": DATA_URL,
        "license": "CC BY (eLife content, unless otherwise indicated). Attribution retained in README.",
        "reproduce": "python work/reproduce_elife_63632_figure3_umaps.py",
        "outputs": [str(path) for path in [*outputs, full, *polished]],
    }
    (OUT / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Published Figure Reproduction: eLife TEA-seq Figure 3\n\n"
        "This package reproduces Figure 3a-e from the published source data. It uses the article's original UMAP coordinates, cell-type labels, supplied colors, QC values, ADT counts, and cell-type summaries; it does not use simulated observations.\n\n"
        "## Recommended GitHub display assets\n\n"
        "- `polished_figures/figure3a-d-atlas-rerender.png` - readable four-panel atlas re-render\n"
        "- `polished_figures/figure3e-marker-heatmap-rerender.png` - readable standalone marker heatmap\n\n"
        "## Attribution and source\n\n"
        "Swanson E, Lord C, Reading J, et al. *Simultaneous trimodal single-cell measurement of transcripts, epitopes, and chromatin accessibility using TEA-seq*. eLife 2021;10:e63632. DOI: [10.7554/eLife.63632](https://doi.org/10.7554/eLife.63632).\n\n"
        "- Original figure: [Figure 3](https://elifesciences.org/articles/63632/figures) panels a-e\n"
        "- Original source data: [Figure 3 source data 1](https://cdn.elifesciences.org/articles/63632/elife-63632-fig3-data1-v2.zip) and [source data 2](https://cdn.elifesciences.org/articles/63632/elife-63632-fig3-data2-v2.zip)\n"
        "- License: eLife content is CC BY unless otherwise indicated; this reproduction retains attribution.\n\n"
        "## Reproduce\n\n```powershell\npython work/reproduce_elife_63632_figure3_umaps.py\n```\n\n"
        "The `polished_figures/` directory contains a source-data re-render split into a readable UMAP atlas and marker heatmap for GitHub display. Outputs are PNG, SVG, and PDF.\n",
        encoding="utf-8",
    )
    print(overview)


if __name__ == "__main__":
    main()
