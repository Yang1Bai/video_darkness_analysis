# Release Notes — v1.0.0

## Purpose

This is the archival release of `video_darkness_analysis` prepared in
conjunction with the submission of the associated Nature Communications paper:

> **Automated synthesis using kinetically controlled co-reduction improves the
> batch-to-batch reproducibility of InSb quantum dots**
> *Yang Bai et al.* — *Nature Communications*, 2026
> DOI: not yet available (to be updated upon publication)

The release provides a permanent, citable snapshot of the analysis code at the
state used to produce the figures and results reported in the paper.

---

## What is included in this release

All Python scripts in `src/` used to quantify precursor-reduction kinetics and
extract optical features from fixed-camera reaction-vessel videos:

| Script | Purpose |
|---|---|
| `check_video.py` | Inspect video metadata; export reference frames |
| `set_roi.py` | Visually verify ROI placement |
| `analyze_darkness.py` | Extract darkness index and related features |
| `smooth_features.py` | Apply rolling-mean smoothing to feature CSV |
| `analyze_foam.py` | Quantify foam thickness from a vertical strip ROI |
| `plot_combined.py` | Generate combined dual-axis publication figure |
| `utils.py` | Shared signal-processing utilities |

Supporting files:

- `README.md` — full usage documentation
- `requirements.txt` — Python dependency list
- `LICENSE` — MIT licence
- `CITATION.cff` — software citation metadata
- `example_output/README.md` — description of expected output files

---

## What is NOT included in this release

- **Raw video recordings** — not tracked in this repository. These will be
  archived separately on Zenodo as a dedicated data record (see
  `README_for_Zenodo_videos.txt`).
- **Unprocessed raw experimental data** — likewise archived separately on Zenodo.
- **Processed result files** (CSV, XLSX) — generated locally by running the
  scripts; not committed to git.
- **Generated figures and images** — not committed to git.

---

## Relationship to the Nature Communications paper

The recommended analysis workflow and command-line usage are documented in
`README.md` and `example_output/README.md`. All analysis parameters are
exposed as command-line arguments; the defaults match those used in the paper.

---

## Data archival

Raw video recordings and unprocessed raw data will be archived in a separate
Zenodo data record with its own DOI. The `README_for_Zenodo_videos.txt` file
in this repository contains the full dataset description and suggested citation
wording for that record.

---

## Zenodo code DOI

A Zenodo DOI for this software repository will be minted automatically after
the GitHub release is created and linked to Zenodo via the GitHub integration.
The DOI will be added to `README.md` and `CITATION.cff` once available.
