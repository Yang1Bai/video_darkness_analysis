# Zenodo Video and Data Manifest Template

> **Instructions:**
> Fill in one row per file before uploading to Zenodo.
> Replace all placeholder values (marked with `[...]`) with actual information.
> Keep this file in the repository as a record of what was uploaded.
> Do not add actual video, image, or data files to the git repository —
> they are excluded by `.gitignore` and must be uploaded directly to Zenodo.

---

## Upload target

Zenodo data record: **Supplementary movies and unprocessed raw data for
automated synthesis of InSb quantum dots**
Data DOI: `[DATA_ZENODO_DOI]`

---

## File manifest

| File name | File type | Raw or processed | Description | Associated figure / analysis | Notes |
|---|---|---|---|---|---|
| `[filename_1.mp4]` | Video (MP4) | Raw | [Brief description of what reaction this video captures, e.g. "Fixed-camera recording of InCl3 reduction at 1× concentration"] | [e.g. "Fig. X; darkness-index and foam-thickness analysis via analyze_darkness.py and analyze_foam.py"] | [e.g. "Duration: Xs; resolution: W×H px; FPS: N"] |
| `[filename_2.mp4]` | Video (MP4) | Raw | [Brief description, e.g. "Fixed-camera recording of InCl3 reduction at 3.5× concentration"] | [e.g. "Fig. Y; same analysis pipeline as filename_1"] | [e.g. "Duration: Xs; resolution: W×H px; FPS: N"] |
| `[filename_3_raw_data.xlsx]` | Spreadsheet (XLSX) | Raw (unprocessed) | [Brief description of what raw measurements are tabulated, e.g. "Unprocessed batch records or instrument logs referenced in the Methods section"] | [e.g. "Supplementary Data [SUPPLEMENTARY_DATA_NUMBER]"] | [e.g. "Original instrument export; no post-processing applied"] |

---

## Completeness checklist

- [ ] All video files listed match files uploaded to Zenodo
- [ ] All raw data files listed match files uploaded to Zenodo
- [ ] File names here match exactly the names on Zenodo (case-sensitive)
- [ ] `[DATA_ZENODO_DOI]` filled in after Zenodo record is published
- [ ] `[CODE_ZENODO_DOI]` filled in after GitHub release is archived
- [ ] `[PAPER_DOI]` filled in after paper is published
- [ ] `README_for_Zenodo_videos.txt` uploaded alongside the data files on Zenodo
