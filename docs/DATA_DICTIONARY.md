# Data dictionary and lineage

The four committed CSVs preserve the original values and bytes. The maintained loader applies aliases and derived fields in memory. Exact schemas below are read from their CSV headers. Missingness and record counts are available in the [audit](../results/tables/data_audit.csv) and [coverage table](../results/tables/text_coverage.csv).

## Snapshot files

| File | Rows | Columns | Meaning |
|---|---:|---:|---|
| [raw_collection.csv](../data/raw_collection.csv) | 1,108 | 29 | Earliest retained micro export, already transformed; 18 duplicate video-ID rows. |
| [micro_clean.csv](../data/micro_clean.csv) | 1,090 | 43 | Preprocessing/NLP snapshot; 1,090 unique video records. |
| [large_clean.csv](../data/large_clean.csv) | 1,177 | 34 | Large-labeled benchmark snapshot; three rows are below the subscriber threshold. |
| [preprocessing_insights.csv](../data/preprocessing_insights.csv) | 16 | 4 | Saved High/Low feature comparisons; historical summary rather than per-video observations. |

## micro_clean.csv fields

| Field | Definition or provenance |
|---|---|
| `video_id` | YouTube video identifier; primary observational key. |
| `video_title` | Video title returned by the API. |
| `description` | Video description; missing values remain in the snapshot. |
| `tags` | API metadata tags, serialized with ` &#124;&#124;&#124; `; distinct from visible hashtags. |
| `category_id` | YouTube category ID; the maintained adapter maps it to a readable category. |
| `published_at` | Video publication timestamp. Parse as UTC; not the collection timestamp. |
| `channel_id` | Channel identifier; use to detect repeated observations from the same channel. |
| `channel_title` | Stored channel display name. |
| `view_count` | Cumulative recorded view count at collection; exposure age is not controlled. |
| `like_count` | Recorded like count; collector uses zero for unavailable numeric fields. |
| `comment_count` | Recorded total comment count; not the number of stored excerpts. |
| `duration` | API ISO-8601 duration string. |
| `subscriber_count` | Recorded channel subscriber count; zero can include unavailable values from collection. |
| `hashtags_from_title` | Visible title hashtags, serialized with ` &#124;&#124;&#124; `. |
| `hashtags_from_desc` | Visible description hashtags, serialized with ` &#124;&#124;&#124; `. |
| `hashtag_count` | Stored hashtag occurrence count; may differ from the count of normalized unique hashtags. |
| `top_comments_text` | Up to ten relevant top-level comment excerpts joined with ` &#124;&#124;&#124; `; missing does not establish no comments. |
| `comment_like_count` | Like counts corresponding to the stored comment excerpts, serialized with ` &#124;&#124;&#124; `. |
| `like_rate` | Stored likes/views ratio; snapshot includes zero-view conventions and one value above one. Quantitative cohorts filter invalid rates. |
| `log_view_count` | `log1p` of `view_count`, retained from preprocessing. |
| `log_like_count` | `log1p` of `like_count`, retained from preprocessing. |
| `log_comment_count` | `log1p` of `comment_count`, retained from preprocessing. |
| `log_subscriber_count` | `log1p` of `subscriber_count`, retained from preprocessing. |
| `scaled_log_view_count` | Historical StandardScaler z-score of `log_view_count`. Retained, but current clustering refits its own scaler. |
| `scaled_log_like_count` | Historical StandardScaler z-score of `log_like_count`. Retained, but current clustering refits its own scaler. |
| `scaled_log_comment_count` | Historical StandardScaler z-score of `log_comment_count`. Retained, but current clustering refits its own scaler. |
| `scaled_log_subscriber_count` | Historical StandardScaler z-score of `log_subscriber_count`. Retained, but current clustering refits its own scaler. |
| `scaled_like_rate` | Historical StandardScaler z-score of `like_rate`. Retained, but current clustering refits its own scaler. |
| `scaled_hashtag_count` | Historical StandardScaler z-score of `hashtag_count`. Retained, but current clustering refits its own scaler. |
| `like_rate_group` | Saved median-based High/Low labels; 545 records each in the micro snapshot. |
| `post_hour` | Publication hour in UTC; aliased to `publish_hour` by the adapter. |
| `post_day` | English weekday label derived from the publication timestamp. |
| `desc_length` | Character length of description with missing text filled empty; aliased to `desc_len`. |
| `has_question_mark` | Description contains a question mark, encoded 0/1. |
| `has_exclamation` | Description contains an exclamation mark, encoded 0/1. |
| `title_hashtag_count` | Count of nonempty title hashtag items in the serialized field. |
| `desc_hashtag_count` | Count of nonempty description hashtag items in the serialized field. |
| `is_vlog` | Regex proxy for the word vlog in title/description; not a platform category. |
| `is_short` | Regex proxy for short/shorts in title/description; not official Shorts status. |
| `is_daily_life` | Text proxy for day in my life, daily life, or routine. |
| `is_first_video` | Text proxy for first vlog, first video, or my first; not independently verified channel history. |
| `duration_seconds` | Parsed duration in seconds; aliased to `duration_sec`. |
| `duration_bucket` | Historical labels: ≤1 min, 1–3 min, 3–10 min, 10–60 min, >60 min. Current comparisons use separately defined bins. |

## large_clean.csv fields

| Field | Definition or provenance |
|---|---|
| `video_id` | YouTube video identifier; primary observational key. |
| `video_title` | Video title returned by the API. |
| `description` | Video description; missing values remain in the snapshot. |
| `channel_id` | Channel identifier; use to detect repeated observations from the same channel. |
| `view_count` | Cumulative recorded view count at collection; exposure age is not controlled. |
| `like_count` | Recorded like count; collector uses zero for unavailable numeric fields. |
| `comment_count` | Recorded total comment count; not the number of stored excerpts. |
| `subscriber_count` | Recorded channel subscriber count; zero can include unavailable values from collection. |
| `hashtag_count` | Stored hashtag occurrence count; may differ from the count of normalized unique hashtags. |
| `duration_sec` | Video duration in seconds in the large snapshot. |
| `publish_hour` | Saved publication hour; interpreted as UTC in the original project. Large timestamps are not retained here for independent rederivation. |
| `publish_weekday` | Saved weekday integer, Monday=0 through Sunday=6. |
| `category_name` | Saved readable YouTube category label. |
| `like_rate` | Stored likes/views ratio; snapshot includes zero-view conventions and one value above one. Quantitative cohorts filter invalid rates. |
| `engagement_rate` | Saved large-cohort derived engagement metric. Exact derivation is not established by the supplied collection code; not used by the maintained analysis. |
| `comment_rate` | Saved large-cohort comment ratio feature. Not used in maintained analysis; original derivation was not recovered. |
| `desc_len` | Saved description length in the large dataset. |
| `has_external_link` | Saved indicator for an external link in description; original rule not fully recovered. |
| `has_cta` | Saved call-to-action text flag; original vocabulary not fully recovered. |
| `emoji_count` | Saved emoji count; original extraction rule not fully recovered. |
| `desc_quality_score` | Saved engineered description score; original weights not recovered. Not used in maintained analysis. |
| `weighted_sentiment` | Saved large-cohort sentiment feature; weighting provenance not recovered. Not used in maintained analysis. |
| `sentiment_label` | Saved large-cohort sentiment class; thresholds not recovered. |
| `all_hashtags` | Serialized Python-list-like collection of hashtags; safely parsed with `ast.literal_eval`. |
| `total_hashtags` | Saved large-cohort hashtag total; not substituted for normalized unique-tag counts. |
| `view_count_scaled` | Saved standardized `view_count` feature. Original fit parameters were not supplied; not used by current clustering. |
| `like_count_scaled` | Saved standardized `like_count` feature. Original fit parameters were not supplied; not used by current clustering. |
| `comment_count_scaled` | Saved standardized `comment_count` feature. Original fit parameters were not supplied; not used by current clustering. |
| `duration_sec_scaled` | Saved standardized `duration_sec` feature. Original fit parameters were not supplied; not used by current clustering. |
| `subscriber_count_scaled` | Saved standardized `subscriber_count` feature. Original fit parameters were not supplied; not used by current clustering. |
| `like_rate_scaled` | Saved standardized `like_rate` feature. Original fit parameters were not supplied; not used by current clustering. |
| `engagement_rate_scaled` | Saved standardized `engagement_rate` feature. Original fit parameters were not supplied; not used by current clustering. |
| `weighted_sentiment_scaled` | Saved standardized `weighted_sentiment` feature. Original fit parameters were not supplied; not used by current clustering. |
| `source` | Saved cohort identifier; maintained loader explicitly assigns micro/large. |

## Other input schemas

`raw_collection.csv` contains the first 29 fields of the micro schema, through `scaled_hashtag_count`, before group labels and later description/timing/duration features. It is not a raw API response archive. Its duplicate video IDs should not be counted as independent observations.

`preprocessing_insights.csv` has fields: `metric`, `high_value`, `low_value`, `difference`. Each row describes one metric and the saved High/Low group averages or their difference.

## Maintained derived fields

| Field | Definition |
|---|---|
| `efficiency_ratio` | `view_count / (subscriber_count + 1)` for corrected clustering. It measures scale-relative views, not labor efficiency. |
| `unique_hashtag_count` | Number of normalized, deduplicated visible hashtags per video. |
| `quadrant` | Golden, Exposure Trap, Niche or Ineffective relative to micro median views and median like rate. |
| `content_text` | Title plus description, missing fields filled empty. |
| `full_text` | Content text plus stored top comments. |
| `sentiment` | VADER compound score on full text. |
| `strongly_positive` | Full-text compound score strictly greater than 0.8. |
| `golden_score` | Micro cell median-view percentile minus large cell posting-density percentile; missing large cells receive zero density rank. |
| `micro_videos` / `large_videos` | Observed video counts for the specified cell or cluster, not unique creators or total platform supply. |
| `at_least_5_micro_videos` | Audit sensitivity flag; a heuristic support threshold, not a significance test. |

## Cohort and measurement conventions

Micro analysis requires positive recorded views, like rate in [0,1], and subscribers from 1 to 9,999. Large analysis requires positive views, like rate in [0,1], and at least 10,000 subscribers. The 1,090-row NLP sample retains original labels for historical comparability and therefore uses a different validity policy. See [reproducibility](REPRODUCIBILITY.md).

All rates in CSV outputs are proportions. Text frequency is token occurrences per video, not document prevalence. Means of individual video ratios are distinct from ratios of summed likes and views. Subscriber-relative views do not measure subscriber conversion or creator effort. Duration is not retention. Fields lacking recovered derivation are documented rather than assigned invented definitions.

YouTube records publication time, content metadata and statistics as separate fields; refer to the [official video resource](https://developers.google.com/youtube/v3/docs/videos). Video categories in the adapter use the saved IDs and common category names; unknown IDs remain Unknown. The adapter does not refresh API metadata.
