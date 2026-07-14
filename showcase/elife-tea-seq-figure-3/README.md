# eLife TEA-seq Figure 3 Reproduction

This is a source-data re-render, not simulated demonstration data.

Swanson E, Lord C, Reading J, et al. *Simultaneous trimodal single-cell measurement of transcripts, epitopes, and chromatin accessibility using TEA-seq*. eLife 2021;10:e63632. DOI: [10.7554/eLife.63632](https://doi.org/10.7554/eLife.63632).

- Original figure: [eLife Figure 3](https://elifesciences.org/articles/63632/figures), panels a-e.
- Source data: [data 1](https://cdn.elifesciences.org/articles/63632/elife-63632-fig3-data1-v2.zip) and [data 2](https://cdn.elifesciences.org/articles/63632/elife-63632-fig3-data2-v2.zip).
- Licence: eLife content is CC BY unless otherwise indicated. Attribution is retained here.

`figure3a-d-atlas-rerender.png` and `figure3e-marker-heatmap-rerender.png` were generated from the published UMAP coordinates, cell labels, QC values, and ADT counts. The images were redesigned for online readability, not passed off as the original artwork.

To reproduce the assets, download and extract the two source-data archives, then set `ELIFE_SOURCE_DATA_1` and `ELIFE_SOURCE_DATA_2` to the two CSV files before running:

```bash
python reproduce_elife_63632_figure3_umaps.py
```
