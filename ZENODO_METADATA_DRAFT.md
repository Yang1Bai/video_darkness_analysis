# Zenodo Metadata Draft

> **This file is a human-readable draft only.**
> Do not upload this file to Zenodo directly.
> Use it as a reference when filling in the Zenodo web form or when
> preparing `.zenodo.json` after both DOIs are confirmed.
>
> Placeholders to fill in before finalising:
> - `[PAPER_DOI]` — assigned by Nature Communications upon acceptance/publication
> - `[DATA_ZENODO_DOI]` — assigned after uploading the video/data record to Zenodo
> - `[CODE_ZENODO_DOI]` — assigned after creating the GitHub release and
>   triggering the Zenodo GitHub integration

---

## Record 1 — Software / code archive

| Field | Value |
|---|---|
| **Upload type** | Software |
| **Title** | video_darkness_analysis: supporting code for reaction-video optical analysis |
| **Version** | 1.0.0 |
| **Publication date** | 2026-05-01 (update to actual release date) |

### Creators

| Name | Affiliation | ORCID |
|---|---|---|
| Bai, Yang | (add affiliation) | (add ORCID if available) |

### Description

Supporting Python code for extracting darkness index and foam thickness from
fixed-camera reaction-vessel videos used in the associated Nature
Communications paper. The scripts quantify precursor-reduction kinetics from
optical features — precipitate darkening and foam/bubble layer thickness —
computed from video recordings of InSb quantum dot synthesis reactions.

### Keywords

```
reaction video analysis
precursor reduction
darkness index
foam thickness
automated synthesis
InSb quantum dots
```

### Licence

MIT

### Related identifiers

| Relation | Identifier | Note |
|---|---|---|
| `isSupplementTo` | `[PAPER_DOI]` | Associated Nature Communications paper |
| `isSupplementedBy` | `[DATA_ZENODO_DOI]` | Separate Zenodo data record (videos + raw data) |
| `isIdenticalTo` | `https://github.com/Yang1Bai/video_darkness_analysis` | GitHub source repository |
| **Self** | `[CODE_ZENODO_DOI]` | This record's DOI (assigned by Zenodo on creation) |

### Notes for Zenodo form

- Select **"Reserve DOI"** before submitting so the code DOI can be added to
  `README.md` and `CITATION.cff` before the GitHub release is made public.
- The software archive will be created automatically by Zenodo via the GitHub
  integration after the GitHub release (`v1.0.0`) is tagged and published.
- Do not manually upload a zip; let Zenodo fetch from GitHub.

---

## Record 2 — Data archive (videos + unprocessed raw data)

| Field | Value |
|---|---|
| **Upload type** | Dataset |
| **Title** | Supplementary movies and unprocessed raw data for automated synthesis of InSb quantum dots |
| **Publication date** | (set to paper publication date) |

### Creators

| Name | Affiliation | ORCID |
|---|---|---|
| Bai, Yang | (add affiliation) | (add ORCID if available) |

### Description

Fixed-camera video recordings of chemical reaction vessels acquired during the
synthesis of InSb quantum dots, together with unprocessed raw experimental
data referenced in the associated Nature Communications paper. Three video
files are included: InCl3 reduction at standard concentration, InCl3 reduction
at elevated concentration (3.5×), and SbCl3 reduction. Videos are provided as
recorded with no post-processing. Analysis code for these videos is archived
separately (see Related identifiers).

### Keywords

```
InSb quantum dots
automated synthesis
reaction video
precursor reduction
supplementary data
```

### Licence

Creative Commons Attribution 4.0 International (CC BY 4.0)

### Files to upload

See `README_for_Zenodo_videos.txt` in the code repository for the full file
list and suggested folder structure.

### Related identifiers

| Relation | Identifier | Note |
|---|---|---|
| `isSupplementTo` | `[PAPER_DOI]` | Associated Nature Communications paper |
| `isSupplementedBy` | `[CODE_ZENODO_DOI]` | Zenodo code/software record |
| `isDocumentedBy` | `https://github.com/Yang1Bai/video_darkness_analysis` | GitHub analysis code |
| **Self** | `[DATA_ZENODO_DOI]` | This record's DOI (assigned by Zenodo on creation) |

---

## DOI fill-in checklist

- [ ] Paper accepted → fill in `[PAPER_DOI]`
- [ ] Data record uploaded to Zenodo → fill in `[DATA_ZENODO_DOI]`
- [ ] GitHub release `v1.0.0` created → Zenodo mints `[CODE_ZENODO_DOI]`
- [ ] Update `README.md` with paper DOI and code DOI
- [ ] Update `CITATION.cff` with code DOI (`doi:` field)
- [ ] Update `ZENODO_METADATA_DRAFT.md` related-identifier tables (or retire this file)
