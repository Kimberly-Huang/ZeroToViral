# Recomputed evidence

These files were generated from the preserved CSV snapshots by [`scripts/analyze.py`](../scripts/analyze.py). They use the cohort definitions, model specifications and sensitivity checks documented in the reproducibility guide. [`run_manifest.json`](run_manifest.json) records input hashes, packages and specifications.

## Figures

| Figure | Reading |
|---|---|
| [Sentiment comparison](figures/sentiment_comparison.png) | Reproduced 545/545 full-text sentiment contrast |
| [Sampling by weekday](figures/sampling_by_day.png) | Strong temporal concentration in the micro sample |
| [Corrected clustering](figures/clustering_corrected.png) | PCA map and K diagnostics under a consistent feature definition |
| [Hashtag quantity](figures/hashtag_quantity.png) | Unique-tag quantity comparison and micro bin sample sizes |
| [Timing sample sizes](figures/timing_sample_sizes.png) | Top-scoring windows, with sparse cells colored separately |

## Tables

| Files | Meaning |
|---|---|
| [Data audit](tables/data_audit.csv), [cohort flow](tables/cohort_flow.csv) | Record/channel counts and sequential micro exclusions |
| [Text coverage](tables/text_coverage.csv), [categories](tables/micro_categories.csv) | Nonempty fields and category composition |
| [Posting day counts](tables/posting_day_counts.csv) | Seven weekday denominators |
| [Cluster profiles](tables/cluster_profiles_corrected.csv), [diagnostics](tables/cluster_diagnostics.csv), [loadings](tables/pca_loadings_corrected.csv), [variance](tables/pca_variance_corrected.csv) | Corrected four-cluster model and diagnostic evidence |
| [Sentiment](tables/sentiment.csv) | Full-text and content-only sentiment, group counts, strongly positive shares |
| [Keywords](tables/distinctive_keywords.csv) | All token-frequency differences per video |
| [Topic terms](tables/topic_terms.csv), [distributions](tables/topic_distributions.csv), [concentration](tables/topic_concentration.csv) | Separate group-specific LDA results |
| [High bigrams](tables/positive_full_text_bigrams_high.csv), [Low bigrams](tables/positive_full_text_bigrams_low.csv) | Filtered-token adjacency in strongly positive full text |
| [Tag quadrants](tables/tag_quadrants.csv), [thresholds](tables/tag_thresholds.csv), [performance](tables/tag_performance.csv) | Quadrant sizes, medians and tags appearing in ≥10 videos |
| [Hashtag quantity](tables/hashtag_quantity.csv), [correlations](tables/hashtag_correlations.csv) | Complete unique-tag bins and stored/unique count sensitivities |
| [Rule denominators](tables/rule_denominators.csv) | Eligible transactions and rule counts by quadrant |
| [Golden rules](tables/rules_golden.csv), [Exposure Trap rules](tables/rules_exposure_trap.csv), [Niche rules](tables/rules_niche.csv) | Full support/confidence/lift outputs; no causal interpretation |
| [All windows](tables/golden_windows.csv), [minimum-five windows](tables/golden_windows_min5.csv) | Score-ranked UTC cells with video counts |
| [Duration windows](tables/golden_windows_by_duration.csv), [hourly summaries](tables/posting_hours.csv), [duration summaries](tables/duration_summary.csv) | Segmented timing and duration evidence |

Rates are proportions unless a figure explicitly shows percentages. Text frequency is tokens per video. Counts refer to video records except columns explicitly named channels. All timing is UTC. Large-channel “density” is a sample count, not measured platform-wide competition.
