# Reproducing the analysis

`archive/` and `reports/original/` contain analysis sources and the research report. `scripts/analyze.py` and `notebooks/` provide the executable analysis. Source hashes and publication status are recorded in the source manifest.

## Environment and execution

Tested with Python 3.13 on macOS. Package versions, input hashes and model settings are recorded in [`results/run_manifest.json`](../results/run_manifest.json). The full observed environment is in [`requirements-lock.txt`](../requirements-lock.txt); it includes notebook and optional historical visualization packages. The original project did not preserve its package versions.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m nltk.downloader -d .cache/nltk_data vader_lexicon
python scripts/analyze.py
python scripts/validate_repository.py
```

The initial package and VADER lexicon downloads require internet access. Analysis then runs from the committed snapshots without an API key or fresh YouTube requests. Run from the repository root. The analysis script resolves file locations relative to its own path, so it also works from another working directory. Outputs are overwritten deterministically within `results/`.

To reproduce only one section:

```bash
python scripts/analyze.py --section audit
python scripts/analyze.py --section cluster
python scripts/analyze.py --section nlp
python scripts/analyze.py --section tags
python scripts/analyze.py --section timing
```

The numbered notebooks are thin, documented entry points into the same implementation. Open them with a Jupyter front end using the installed environment. Notebooks 02–06 execute offline once dependencies and the lexicon are installed. Notebook 01 is optional and deliberately requires an explicit collection flag and an environment variable before making API requests.

## Input contract

The four CSVs under `data/` remain byte-identical to the existing public repository and the corresponding local submitted files. `raw_collection.csv` is the earliest retained export, but already includes transformations; it is not raw JSON from the API.

| Use | Micro rows | Large rows | Policy |
|---|---:|---:|---|
| Preserved snapshot | 1,090 | 1,177 | No changes to original files |
| Historical NLP reconstruction | 1,090 | — | Retain stored High/Low labels, 545 each |
| Quantitative reconstruction | 1,035 | 1,174 | Positive views, valid like rate, positive micro subscribers below 10,000; large subscribers at least 10,000 |

The explicit positive-subscriber filter reconstructs the historical micro count. An exact original intermediate `micro_clean.csv` containing 1,035 rows was not among the supplied files. Matching row counts and selected output statistics is strong reconciliation evidence, but does not establish byte-for-byte recovery of that missing file.

The adapter aliases `post_hour` to `publish_hour`, `duration_seconds` to `duration_sec`, and `desc_length` to `desc_len`. It derives category names from saved category IDs and adds the cohort source label. These changes are in memory; inputs remain unchanged.

## Model specifications

### Segmentation

The corrected specification uses views divided by subscribers plus one, like rate, and video duration. Apply `log1p`, `StandardScaler`, two-component PCA, then K-Means with four clusters, `random_state=42`, and `n_init=10`. K=2–8 inertia and silhouette scores are exported. Four clusters are retained to compare with the submitted framing, not automatically declared optimal. The corrected result uses 2,209 video records, because three below-threshold records are removed from the large cohort. Historical clustering used 2,212 records and contains inconsistent efficiency formulas and stale variable state.

### NLP

Retain the submitted stopword sets and ASCII-letter cleaning. VADER scores raw title + description + top comments. The added content-only score is a sensitivity check. Keywords use token counts per video, not the percentage of videos containing each word. For each group, fit a separate five-topic LDA on title + description using `CountVectorizer(max_features=1000, min_df=2)`, batch learning, and seed 42. Report dominant topic shares and entropy in natural-log units. Topic IDs are local to each separately fitted model.

Bigrams follow the saved final code: adjacent retained tokens in combined full text for videos with VADER >0.8. The report's description of comment-only bigrams at >0.5 is not the implemented procedure. Removing stopwords can make tokens adjacent that were not adjacent in the original text.

### Tags

Normalize and deduplicate title/description hashtags per video. Keep tags found in at least ten videos for performance rankings. Define four quadrants using the micro cohort's median views and median like rate. Apriori uses minimum support 0.025 and rules use minimum lift 1.3. Transactions contain videos with at least two hashtags within each quadrant; the denominator is exported explicitly. No tag-type percentages or illustrative word-cloud weights are hard-coded in the reconstructed outputs.

Quantity bins count **unique parsed hashtags**, with boundaries 0, 1–3, 4–7, 8–15 and 16+. The original “15+” label overlaps the previous interval; the new label is unambiguous. Correlation tables separately expose stored hashtag counts and unique counts. Partial correlations include a one-control log-subscriber sensitivity and the working notebook's views/subscribers/duration control set. P-values use the corresponding residual degrees of freedom; these are descriptive analyses without multiplicity or channel dependence correction.

### Timing

Within observed weekday/hour cells, rank micro median views and large video counts separately with percentile ranks and average tie handling. Left-join density to observed micro cells and assign zero density rank to unobserved large cells, matching the historical scoring approach. Subtract density rank from performance rank. The theoretical score bounds are −1 to +1, not 0 to 1. Scores are relative ordering heuristics, not success probabilities.

Every row includes the micro sample size. The minimum-five sensitivity table filters the original scored cells without reranking. Five is a transparency threshold chosen for this reconstruction, not a statistically validated sample requirement. Duration-specific scores use the corresponding large duration cohort. The bins are analysis conventions, not official Shorts classifications.

## What is and is not reproduced

The validation checks data hashes, sample flows, source archive integrity, notebook structure, output arithmetic and selected historical results. It does not establish causal effects, platform-level representativeness, forecasting performance or business impact. No live collection was run during this reconstruction. Large-channel collection cannot be reproduced completely because a complete collection script and raw API response archive were not supplied. Original notebooks retain their historical outputs, missing-state dependencies and methodological inconsistencies for audit.

## Validation record

All six maintained notebooks were executed successfully from fresh Jupyter kernels, with live collection disabled. See the [validation record](VALIDATION.md) for checks and scope.
