# Validation record

Validation covers the committed data, numerical outputs and executable analysis.

- All six maintained notebooks executed successfully from fresh Jupyter kernels. The optional collection notebook ran with collection disabled; no live YouTube requests were made.
- The data audit, corrected clustering, NLP, tag rules and timing analyses executed from the committed snapshots.
- The four data snapshots remained unchanged from baseline commit `d5fa805`.
- The source manifest records 19 files, including 18 published sources and one local-only source. Published hashes account for credential and personal-attribution removals.
- Recomputed NLP means, group sizes, tag quadrants and stored-count correlations agree with the documented historical evidence within stated rounding tolerances.
- Quantity-bin totals cover the entire reconstructed micro and large cohorts. Timing tables include every observed micro cell and its sample size.
- Five regenerated analytical figures were visually inspected for legibility and clipping.
- Maintained notebooks passed schema and Python syntax validation. Repository documentation links resolved locally, and published sources were scanned for common API credential patterns.

Run `python scripts/validate_repository.py` to repeat the deterministic evidence checks. Package versions, data hashes, analysis source hash and the VADER lexicon archive hash are in [`run_manifest.json`](../results/run_manifest.json).

This validation establishes execution and internal consistency. It does not validate a causal creator-growth claim, recover absent raw API responses, or make the sample representative of YouTube. The historical source notebooks intentionally retain their original errors and missing-state dependencies. The original Word report remains unchanged.
