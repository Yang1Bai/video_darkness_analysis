# Video-Based Darkness and Foam Analysis

Supporting code for the quantitative analysis of reaction-vessel video recordings reported in:

> **Automated Synthesis of Uniform and Reproducible InSb Quantum Dots via Kinetically Matched Co-reduction** -- *Yangning Zhang et al.* -- *Nature Communications*, 2026
> DOI: not yet available (to be updated upon publication)

This repository provides the Python scripts used to quantify precursor-reduction kinetics and extract optical features — darkness index and foam thickness — from fixed-camera reaction videos of chemical synthesis. All scripts accept command-line arguments so that paths, ROI coordinates, and analysis parameters can be varied without editing the source code.

---

## Repository structure

```
video_darkness_analysis/
+-- README.md
+-- requirements.txt
+-- src/
|   +-- check_video.py        # 1. Inspect video metadata; export reference frames
|   +-- set_roi.py            # 2. Visually verify ROI placement
|   +-- analyze_darkness.py   # 3. Extract darkness features from a fixed ROI
|   +-- smooth_features.py    # 4. Apply rolling-mean smoothing to feature CSV
|   +-- analyze_foam.py       # 5. Quantify foam thickness from a vertical strip ROI
|   +-- plot_combined.py      # 6. Combined dual-axis figure (foam + darkness)
|   \-- utils.py              #    Shared signal-processing utilities
\-- example_output/
    \-- README.md             #    Description of expected output files
```

---

## Data and code availability

> **Raw videos and unprocessed raw data are not tracked in this GitHub repository.**
> They will be archived separately on [Zenodo](https://zenodo.org) upon publication.
> The archival code release is archived on Zenodo at https://doi.org/10.5281/zenodo.19958176

For reference, the raw video recordings used in the associated paper are currently
available on Google Drive (interim storage only; the Zenodo archive supersedes this):

**[Download raw videos (interim)](https://drive.google.com/drive/folders/1RlZp30mjDbS6gUVqBfUZrhBVo98cTxp0)**

| File | Description |
|---|---|
| `InCl3 reduction.mp4` | InCl3 reduction reaction (1x concentration) |
| `3.5xInCl3 reduction.mp4` | InCl3 reduction reaction (3.5x concentration) |
| `SbCl3 reduction.mp4` | SbCl3 reduction reaction |

Download these files and place them in a local `data/` directory before running the analysis scripts.

---

## Installation

Python >= 3.8 is required.

```bash
pip install -r requirements.txt
```

All scripts are run from the `src/` directory (or with an appropriate
`PYTHONPATH`), because `analyze_foam.py` imports from `utils.py`.

```bash
cd src
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `opencv-python` | Video I/O, grayscale conversion, Gaussian filtering |
| `numpy` | Numerical array operations |
| `pandas` | CSV I/O and rolling-mean smoothing |
| `matplotlib` | Plotting |

---

## Recommended analysis workflow

Run the scripts in the order shown below. Each step produces output that is
consumed by the next.

### Step 1 -- Inspect the video

```bash
python check_video.py --video /path/to/reaction.mp4 --target_time 9
```

Prints video metadata (FPS, resolution, duration) and saves:
- `first_frame.jpg` -- used as the reference image in Step 2.
- `frame_9.0s.jpg`  -- a mid-experiment reference frame.

### Step 2 -- Verify ROI placement

```bash
# Darkness analysis ROI
python set_roi.py --image first_frame.jpg --roi 800 775 100 70

# Foam analysis ROI (vertical strip)
python set_roi.py --image first_frame.jpg --roi 800 500 125 350 --output foam_roi_check.jpg
```

Opens `first_frame.jpg`, draws the ROI as a red rectangle, and saves the
annotated image. Adjust the coordinates until the ROI is correctly placed
inside the reaction vessel.

### Step 3 -- Extract darkness features

```bash
python analyze_darkness.py \
    --video /path/to/reaction.mp4 \
    --roi 800 775 100 70 \
    --threshold 65 \
    --step_time 0.3 \
    --output darkness_features.csv
```

Samples the video at 0.3 s intervals, computes optical features within the
ROI, and writes `darkness_features.csv`.

### Step 4 -- Smooth feature time series (optional)

```bash
python smooth_features.py \
    --input darkness_features.csv \
    --window 9 \
    --output darkness_features_smooth.csv \
    --plot
```

Appends rolling-mean smoothed columns and optionally shows a preview plot.

### Step 5 -- Extract foam thickness

```bash
python analyze_foam.py \
    --video /path/to/reaction.mp4 \
    --roi 800 500 125 350 \
    --min_peak_value 2.0 \
    --min_peak_distance 12 \
    --smooth_window 15 \
    --output foam_features.csv \
    --plot
```

Processes every frame, detects air/foam/liquid interfaces from the vertical
intensity gradient, and writes `foam_features.csv`.

### Step 6 -- Combined plot

```bash
python plot_combined.py \
    --foam foam_features.csv \
    --darkness darkness_features.csv \
    --title "InCl3 (no Zn) - 03/02" \
    --output combined_plot.png
```

Produces a dual-axis figure with foam thickness (left axis) and darkness
features (right axis) plotted against time.

---

## Script descriptions

### `check_video.py`
Reads a video file, prints metadata (FPS, frame count, resolution, duration),
and exports a reference frame at t = 0 and at a user-specified time. Used
before analysis to confirm file integrity and to obtain a frame for ROI setup.

### `set_roi.py`
Draws a red rectangle on a reference frame image to visualise a proposed ROI.
Used iteratively to confirm ROI placement before committing coordinates to the
analysis scripts.

### `analyze_darkness.py`
Core darkness analysis. For each sampled frame, the ROI is cropped, converted
to grayscale, and Gaussian-blurred. Five features are computed and written to
a CSV (see *Extracted metrics* below).

### `smooth_features.py`
Applies a centered pandas rolling mean to the three primary darkness features.
Smoothed columns are appended to the CSV so that the original raw values are
always retained.

### `analyze_foam.py`
Foam/bubble quantification. A narrow vertical strip ROI is sampled every
frame. The mean vertical intensity profile is differentiated; significant
gradient peaks indicate optical interfaces. When two major interfaces are
detected, their pixel separation is taken as the foam thickness.

### `plot_combined.py`
Generates a publication-style dual-axis figure overlaying foam thickness (left
axis) and darkness features (right axis) on a shared time axis.

### `utils.py`
Shared helper functions used by `analyze_foam.py`: a box-kernel moving
average, 1D Gaussian smoothing (via OpenCV), and a local-peak detection
routine with minimum-amplitude and minimum-separation constraints.

---

## Extracted metrics

| Column | Definition |
|---|---|
| `time_s` | Elapsed time from the start of the video (seconds) |
| `mean_gray` | Mean pixel intensity in the ROI after Gaussian filtering (range 0-255) |
| `dark_ratio` | Fraction of ROI pixels with intensity < threshold |
| `darkness` | Normalized darkness index: `1 - mean_gray / 255` (range 0-1) |
| `std_gray` | Standard deviation of ROI pixel intensities |
| `std_gray_norm` | Normalized standard deviation: `std_gray / 255` (range 0-1) |
| `foam_height_px` | Raw foam thickness in pixels (0 when no foam is detected) |
| `foam_height_smooth` | Moving-average smoothed foam thickness |

---

## Key analysis parameters

| Parameter | Default | Description |
|---|---|---|
| `--threshold` | 65 | Grayscale intensity threshold for dark-pixel classification |
| `--step_time` | 0.3 s | Sampling interval for darkness analysis |
| `--window` | 9 | Rolling-mean window size for smoothing |
| `--min_peak_value` | 2.0 | Minimum gradient amplitude for interface detection |
| `--min_peak_distance` | 12 px | Minimum separation between two interface peaks |
| `--smooth_window` | 15 frames | Moving-average window for foam height |

---

## Reproducibility notes

- All analysis parameters are exposed as command-line arguments with documented
  defaults. The exact commands used to produce the figures in the paper are
  provided in the Methods section and reproduced in the `example_output/`
  folder.
- ROI coordinates are experiment-specific and must be verified using
  `set_roi.py` for each new video (see *Limitations* below).
- The darkness threshold (default 65) was chosen empirically based on the
  visual appearance of the precipitate against the glass vessel. We recommend
  verifying this value for recordings obtained under different lighting
  conditions.
- Frame sampling in `analyze_darkness.py` uses `round(fps * step_time)` to
  convert seconds to frames, which is robust to minor frame-rate variations.
- Foam analysis (`analyze_foam.py`) processes every frame rather than a
  sub-sampled sequence to capture transient foam dynamics at full temporal
  resolution.

---

## Limitations and assumptions

- **Fixed camera**: All scripts assume the camera does not move during the
  recording. Camera shake or repositioning will invalidate the fixed ROI.
- **Manually defined ROI**: The ROI must be defined separately for each
  experiment because the reaction vessel position may differ slightly between
  setups. Use `check_video.py` and `set_roi.py` to set coordinates
  interactively.
- **Stable lighting**: The darkness metrics assume uniform, stable ambient
  lighting throughout the recording. Changes in room lighting or direct
  sunlight will introduce artefacts.
- **Foam detection heuristics**: The interface detection relies on gradient
  peak analysis with empirically tuned thresholds (`min_peak_value`,
  `min_peak_distance`). These may require adjustment for videos with
  different contrast or foam morphology.
- **Foam thickness in pixels**: `foam_height_px` is reported in pixel units.
  Conversion to physical units requires an independent calibration measurement
  (e.g., a ruler placed in the field of view).

---

## Citation

If you use this code in your research, please cite the associated paper (see
header) and this repository:

```
Yang Bai (2026). video_darkness_analysis: supporting code for reaction-video
optical analysis (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.19958176
```

---

## License

MIT License -- see `LICENSE` for details.
