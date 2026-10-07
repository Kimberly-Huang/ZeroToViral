# Evidence audit and reconciliation

This audit compares the final Word report, original presentation, saved notebook source and outputs, and the supplied CSV files. It separates reproduced observations from historical claims whose interpretation or implementation needs qualification. Source file hashes are recorded in the [manifest](../archive/source-manifest.csv). Baseline public repository: commit `d5fa805`.

## Evidence levels

**Recomputed** means the maintained script generated the cited result from committed inputs. **Historical** means the value or narrative appears in the submission but is not accepted as a newly verified result. **Reconstructed** means an explicit processing choice recovers historical counts or findings, with the missing source step disclosed. None of these labels implies causality.

## Data and pipeline reconciliation

| Item | Original material | Audit resolution |
|---|---|---|
| Observation unit | Report sometimes calls 1,091 and 1,178 records “channels” | Actual saved files contain 1,090 and 1,177 **video records**, representing 1,053 and 1,146 unique channels. The one-row-higher report counts are inconsistent with the CSVs. Counting headers is a possible explanation, not established provenance. |
| Raw data | `raw_collection.csv` described as raw API output | It already has engineered log/scaled columns; 1,108 rows contain 1,090 unique video IDs. Original raw API JSON was not supplied. |
| Micro analysis count | README claimed the stored file was 1,035 × 45 | The stored file is 1,090 × 43. Positive views remove 29 rows, valid like rate removes one more, and positive subscribers remove another 25: 1,035 remain. Field aliases and added category/source fields explain the 45-column analysis schema. |
| Large analysis count | 1,177 in clustering; 1,174 in tags | Three records in the “large” file have fewer than 10,000 subscribers. The maintained quantitative cohort consistently excludes them. |
| NLP labels | 545 High and 545 Low | Reproduced using stored labels across all 1,090 rows. Those rows include the zero-view and anomalous-rate records excluded elsewhere. |
| Execution | README said notebooks 03–06 could run directly | Paths, schemas and missing state prevented this. NLP searched for nonexistent files; K-Means referenced `df_combined` before defining it; tag code used undefined quantity variables. New entry points call one maintained script. Originals are archived. |
| Credentials | Literal credential in local collection notebook | Redacted in its public archive copy. The optional maintained notebook reads an environment variable and does not run collection by default. |

## Clustering

| Claim or behavior | Finding | Current treatment |
|---|---|---|
| Three vs four archetypes | Previous README mixed an early K=3 model with final K=4 labels | Document four historical archetypes and label the corrected rerun separately. |
| Efficiency definition | Early code uses `views / (subscribers + 1)`, but submitted cell 11 overwrites `df_combined['efficiency_ratio']` with `like_rate / view_count` | The maintained specification consistently uses views per subscriber-plus-one. Saved “final” output has efficiency values on the incompatible scale, so old efficiency magnitudes and growth multipliers are not reliable. |
| Report's “Viral Elite” efficiency 184.1 and 36× lever | Not supported by the saved final profiling table | Do not repeat as verified performance. Corrected cluster profiles are exported without attaching old numeric IDs to new groups. |
| K=4 best silhouette | Report says silhouette favors four, while the submitted path shows elbow/PCA experiments and incomplete state | The corrected rerun's K=3 silhouette is 0.592 versus 0.482 for K=4. Four remains an interpretive comparison, not an optimality claim. |
| Cluster names on PCA plot | `market_segment` was created before PCA refit and not updated before a plot | New plots use current numeric cluster IDs. Historical semantic labels are discussed as analyst interpretations. |
| Long videos imply retention/authority | Duration is measured, watch retention is not | Describe long-duration content; do not infer high retention or brand equity. |
| Archetype transitions prove a growth lifecycle | Cross-sectional observations do not track transitions | Present possible strategic positions, not an observed creator progression. |
| Pets & Animals is a market-wide “blue ocean” | The chart hard-codes a demand/supply summary. Demand means average views and supply means sampled video count | Retain as a historical hypothesis. Sample proportions and age/scale confounding prevent a platform-wide opportunity claim. |

## NLP

| Claim | Recomputed evidence | Interpretation |
|---|---|---|
| High/Low sentiment difference | 0.419069 vs 0.327392; strongly positive 33.0275% vs 22.9358% | Reproduced association, not a causal benefit of changing language. No significance claim is made. |
| Creator warmth explains the difference | Combined title, description and comments; content-only mean is 0.302182 vs 0.267554 | The gap shrinks from 0.091677 to 0.034628 when comments are excluded. This is a descriptive sensitivity check, not a decomposition of causality. |
| `jee` frequency difference +0.657 | Recomputed +0.656881 tokens per video | Context-specific vocabulary contrast, not a general instruction to add exam terms. |
| `assamese` appears only in High | High 0.106422; Low 0.001835 tokens/video | Low has a nonzero occurrence. “Exclusive” is incorrect for this term. |
| High topic shares all around 22–27% | Actual range 9.91–26.79% | Correct the deck's simplified heading. |
| Low top-topic share 39.0% | Recomputed 38.8991%, versus High 26.7890% | Approximately 38.9% at one decimal, not exactly 39.0%. Entropies 1.564818 and 1.507096 reproduce. |
| Topic concentration proves market saturation | Separate LDA models have different topics and vocabularies | Discuss sample concentration only; matched topics, stability checks and representative supply data would be needed. |
| Positive **comment** bigrams with sentiment >0.5 | Final code selects **full-text** sentiment >0.8 and uses full-text tokens | Maintained code follows the actual implementation and names the output accordingly. Repeated phrases cannot establish spam or insincere audience behavior. |
| Four or five pillars with a 25% cap | Recommendation in the report | Unvalidated heuristic. Five fitted topics do not prove a creator should use five content pillars. |

## Hashtags

The final tag notebook's quadrant counts reproduce exactly: Golden 226, Exposure Trap 292, Niche 292 and Ineffective 225. Rule transactions differ: only 186, 270 and 200 videos respectively have two or more hashtags. Support and lift are conditional on those subsets.

The submitted **stored hashtag count** correlation reproduces: Pearson −0.023399 (p=0.452065), Spearman −0.117983 (p=0.000142). The working notebook residualizes count and like rate on **views, subscribers and duration**, not subscribers alone. The coefficient reproduces as −0.022930. Its saved residual-Pearson p-value was about 0.4612; using the appropriate three-control degrees of freedom gives 0.461844. Neither establishes an independent linear effect, and a nonsignificant estimate does not prove no effect exists.

The previous README's “80% higher than 15+” conflates two comparisons. The saved output compares **no hashtags versus any hashtags** (medians approximately 0.0254 and 0.0141). The archived quantity table has a separate 15+ bin. Moreover, its micro bin counts total 1,025 rather than 1,035 and large counts total 1,171 rather than 1,174, so that table is not a complete accounting of the declared cohorts. Required bin-construction variables are absent from the saved final code.

The reconstruction therefore publishes a fully specified **unique hashtag** quantity table whose bins cover all 1,035 and 1,174 records. Its nonzero-bin values differ from the original report; it is not labeled an exact reproduction. Stored-count and unique-count correlations are both provided to expose the metric choice.

The 74% claim comes from rounded shares of manually categorized top-15 tags: 4/15 identity plus 7/15 content-specific is 11/15 = **73.3%**, not exactly 74%. The tag-type assignments and word-cloud weights include hard-coded values. They remain historical analysis, not automatic model outputs. The reconstructed rankings are derived directly from observations.

Association rules describe co-occurrence within a performance group. A lift of 12.9 is not a 12.9× increase in views, and selecting successful videos before mining tags cannot establish that the tag combination caused success. The report's three-tier recommendation mechanism was not measured by this dataset and is not adopted as a factual explanation.

## Timing and duration

The score is `percentile(micro median views) − percentile(large sampled post count)`, with missing large cells assigned zero. Its bounds are −1 to +1. It is a within-sample heuristic, not a probability; unobserved large posts do not demonstrate absent competition.

The original timing code sorts the top ten rows by weekday/hour for display, then selects `top10.iloc[0]` as “#1”. That can mislabel the top-scoring window. The maintained table retains score order. The deck's image-only results slide correctly shows Sunday 00:00 as the highest overall score, while the previous README emphasizes different windows.

| UTC window | Recomputed median views | Micro n | Large n | Score | Assessment |
|---|---:|---:|---:|---:|---|
| Sunday 00:00 | 4,409 | 1 | 2 | 0.806 | Highest score, one video |
| Monday 09:00 | 1,283 | 12 | 1 | 0.782 | Better-supported exploratory candidate |
| Saturday 09:00 | 143,837.5 | 2 | 4 | 0.687 | Very sparse |
| Monday 04:00 | 1,261 | 5 | 2 | 0.683 | Candidate under minimum-five sensitivity |
| Monday 06:00 | 1,940 | 9 | 3 | 0.682 | Candidate under minimum-five sensitivity |
| Friday 11:00 | 7,233.5 | 2 | 4 | 0.636 | Very sparse |

The short/mid/long duration winners in the report come from separately ranked duration cohorts. They must not be mixed with overall rankings. The maintained output includes each duration-specific cell's sample size.

Monday/Tuesday comprise 893/1,090 = 81.93% of the micro snapshot and 845/1,035 = 81.64% of the quantitative cohort. This is also a sampling limitation: the collector uses recent date-ordered searches. It does not establish that creators worldwide choose those days.

The duration analysis supports a sample-level trade-off: micro videos of 0–60 seconds have median 917 views and 1.31% like rate, while 60–600-second videos have 207 views and 3.21%, and >600-second videos have 244 views and 5.26%. Therefore “1–10 minutes maximizes engagement” is too strong. Official Shorts eligibility also involves criteria beyond a 60-second cutoff, as described in [YouTube guidance](https://support.google.com/youtube/answer/15424877).

## Presentation and business claims

The 43-slide original file contains image-only evidence, duplicate slides and unrelated SWOT/template slides. It is preserved unchanged and labeled as an original artifact. No claims of current platform market size, channel failure rate, creator concentration or measured business growth are promoted from its introductory slides without independently supported evidence.

The project demonstrates an exploratory research workflow and interpretable decision framing. The supplied evidence does not show a live deployment, an experiment with creators, incremental subscribers, revenue impact or a validated prediction system.
