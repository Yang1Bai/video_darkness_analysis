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
| **Title** | Supplementary movies for automated synthesis of InSb quantum dots |
| **Publication date** | (set to paper publication date) |

### Creators

| Name | Affiliation | ORCID |
|---|---|---|
| Bai, Yang | (add affiliation) | (add ORCID if available) |

> **Note:** Add additional co-authors before publication if required.

### Description

This record contains supplementary movies associated with the Nature
Communications paper "Automated synthesis using kinetically controlled
co-reduction improves the batch-to-batch reproducibility of InSb quantum
dots". The files include fixed-camera reaction videos used for
precursor-reduction kinetic analysis and supporting darkness-index and
foam-thickness quantification.

> **Note:** Unprocessed raw data and Source Data should be provided
> separately according to Nature Communications production requirements,
> unless explicitly included in this Zenodo record.

### Keywords

```
InSb quantum dots
automated synthesis
precursor reduction
reaction video analysis
darkness index
foam thickness
supplementary movies
unprocessed raw data
```

### Licence

Creative Commons Attribution 4.0 International (CC BY 4.0)

### Files to upload

See `README_for_Zenodo_videos.txt` and `ZENODO_VIDEO_MANIFEST_TEMPLATE.md` in
the code repository for the video file list and suggested folder structure.
Unprocessed raw data and Source Data files should be added here only if
included in this Zenodo record per journal production requirements.

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
