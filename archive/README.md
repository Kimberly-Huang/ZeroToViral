# Source archive

This directory preserves the project history so that the maintained analysis can be checked against the material actually submitted.

- [`source-manifest.csv`](source-manifest.csv) maps all 19 supplied files to repository locations and records original and published SHA-256 hashes.
- [`submission/`](submission/) retains final and working notebooks, proposal data and the Data Architect phase. Four duplicate CSVs are mapped to their identical existing `data/` files instead of stored twice.
- [`previous-github-notebooks/`](previous-github-notebooks/) and [`previous-README.md`](previous-README.md) retain the repository version at baseline commit `d5fa805` before the reconstruction.
- [`reports/original/`](../reports/original/) contains the original final report and presentation.

The submitted collection notebook had a literal API credential. Its public archive copy replaces that credential with `REDACTED_API_KEY`. Original local files were not changed. The manifest records this intentional hash difference. No original notebook is presented as a clean-kernel executable workflow.

`Data Architect_Phase1/initial_code_time_series.ipynb` and `final_code_time_series.ipynb` overlap with the working/final timing notebooks; both are retained to preserve file provenance. The supplied `APIs_Raw_Original_files` directory was empty and contained no recoverable API responses.

The presentation contains 43 slides, including duplicate content, image-only slides, and unrelated template material on slides 32–40 and 43. It is an original source artifact, not the curated project narrative. The final report also contains placeholder figure references and interpretations qualified by the retrospective. Consult the maintained [case study](../docs/CASE_STUDY.md) and [evidence audit](../docs/EVIDENCE_AUDIT.md) for current interpretation.
