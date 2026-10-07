# Analysis sources

The archive contains analysis notebooks, proposal data and earlier result versions used to document the analytical workflow.

- [`source-manifest.csv`](source-manifest.csv) records source hashes, publication status and the location of each included file. Four duplicate CSVs map to the identical snapshots under `data/`.
- [`submission/`](submission/) contains the analysis source notebooks and Data Architect phase data.
- [`previous-github-notebooks/`](previous-github-notebooks/) and [`previous-README.md`](previous-README.md) contain the earlier repository version at baseline commit `d5fa805`.
- [`reports/original/`](../reports/original/) contains the final research report.

Public notebook copies omit credentials and personal attribution. The manifest records changes to published file hashes. Sources marked `local_only` are not included in the current public repository.

The earlier timing notebooks overlap with the corresponding phase notebooks. Historical notebooks may depend on intermediate variables or files; executable entry points are in [`notebooks/`](../notebooks/). Method definitions and result differences are documented in the [methodology audit](../docs/EVIDENCE_AUDIT.md).
