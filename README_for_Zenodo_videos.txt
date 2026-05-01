================================================================================
README for Zenodo data upload
================================================================================

Dataset title:
  Supplementary movies for automated synthesis of InSb quantum dots

Associated paper:
  Automated synthesis using kinetically controlled co-reduction improves the
  batch-to-batch reproducibility of InSb quantum dots
  Yang Bai et al.
  Nature Communications, 2026
  DOI: [PAPER_DOI]

Data DOI (this Zenodo record):
  [DATA_ZENODO_DOI]

================================================================================
1. What the videos are
================================================================================

The video files in this dataset are fixed-camera recordings of chemical
reaction vessels acquired during the synthesis of InSb quantum dots. Each
recording captures the full duration of one synthesis experiment. The camera
was positioned to capture the interior of the reaction vessel so that optical
changes — precipitate darkening and foam/bubble formation — are visible and
can be quantified.

Three video recordings are included:

  InCl3 reduction.mp4
      InCl3 precursor reduction at standard concentration (1x).

  3.5xInCl3 reduction.mp4
      InCl3 precursor reduction at elevated concentration (3.5x).

  SbCl3 reduction.mp4
      SbCl3 precursor reduction.

All videos are provided as-recorded (no post-processing, no cropping, no
compression beyond the camera's native codec).

================================================================================
2. Unprocessed raw data and Source Data
================================================================================

Unprocessed raw data and Source Data are not necessarily included in this
Zenodo record. They should be provided separately according to Nature
Communications production requirements (e.g., as Supplementary Data files
or as Source Data attached to the published paper).

If unprocessed raw data files are added to this Zenodo record, list them
explicitly in ZENODO_VIDEO_MANIFEST_TEMPLATE.md and update this README.

================================================================================
3. How the files relate to the GitHub analysis code
================================================================================

The Python scripts archived at:

  https://github.com/Yang1Bai/video_darkness_analysis

read the video files in this Zenodo record as input. To reproduce the analysis:

  1. Download the video files from this Zenodo record.
  2. Place them in a local `data/` directory.
  3. Clone or download the code from the GitHub repository (or its Zenodo
     code archive, DOI: [CODE_ZENODO_DOI]).
  4. Follow the step-by-step workflow in README.md.

The exact ROI coordinates and analysis parameters used for each video are
documented in the paper's Methods section and in `example_output/README.md`.

================================================================================
4. Suggested folder structure for this Zenodo upload
================================================================================

  zenodo_data_upload/
  ├── README_for_Zenodo_videos.txt      ← this file
  └── videos/
      ├── InCl3 reduction.mp4
      ├── 3.5xInCl3 reduction.mp4
      └── SbCl3 reduction.mp4

  Note: the three video filenames above are based on current working names.
  Confirm exact filenames before upload and update this README if they differ.
  Add a raw_data/ subfolder only if unprocessed data files are included in
  this record.

================================================================================
5. Suggested citation wording
================================================================================

For the video/data record (this Zenodo upload):

  Bai, Yang et al. (2026). Supplementary movies and unprocessed raw data for
  automated synthesis of InSb quantum dots [Dataset]. Zenodo.
  https://doi.org/[DATA_ZENODO_DOI]

For the analysis code (separate Zenodo software record):

  Bai, Yang (2026). video_darkness_analysis: supporting code for
  reaction-video optical analysis [Software]. Zenodo.
  https://doi.org/[CODE_ZENODO_DOI]

For the associated paper:

  Bai, Yang et al. (2026). Automated synthesis using kinetically controlled
  co-reduction improves the batch-to-batch reproducibility of InSb quantum
  dots. Nature Communications. https://doi.org/[PAPER_DOI]

================================================================================
