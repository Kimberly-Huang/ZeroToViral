# YouTube Market Entry Strategy for New Creators

**Columbia University — APAN 5205 Machine Learning II (Spring 2026)**

A data-driven study on how micro-creators (< 10K subscribers) can successfully break into the YouTube market. Using the YouTube Data API and a pipeline of four ML models — K-Means Clustering, NLP Analysis, Tag Strategy (Association Rules), and Time-Series Posting Analysis — we extract actionable recommendations for new channel growth.

---

## Project Overview

New YouTube creators face a cold-start problem: without an existing subscriber base, organic reach is almost impossible to achieve. This project collects 1,000+ videos from micro-creators and 1,000+ videos from large channels, then applies multiple machine learning techniques to identify what separates high-engagement content from low-engagement content.

**Research Question:** What content strategy, tags, sentiment, and posting timing maximize engagement for micro-creators?

---

## Key Findings

| Dimension | Finding |
|-----------|---------|
| **Market Segments** | Three distinct archetypes exist: *Viral Shorts* (high reach, low engagement), *Deep Content* (high engagement, long duration), and *Mainstream Majority* (low reach) |
| **Sentiment** | High like-rate videos have significantly higher VADER scores (0.419 vs 0.327); 33% vs 23% are "strongly positive" (compound > 0.8) |
| **Tag Strategy** | Identity + Content-specific tags make up 74% of top-performing tags vs 20% of bottom-performing tags; Format-chasing tags (e.g., `#viral`, `#shorts`) correlate with low engagement |
| **Hashtag Quantity** | Fewer hashtags → better engagement; videos with 0 hashtags have 80% higher median like rate than videos with 15+ |
| **Posting Windows** | Monday 9:00 UTC, Friday 11:00 UTC, and Saturday 9:00 UTC are top golden windows (high micro-creator performance, low large-channel competition) |
| **Duration** | Shorts (≤ 1 min) maximize reach; 1–10 min videos optimize for engagement rate |

---

## Project Structure

```
YouTube-Market-Entry-Strategy/
├── data/
│   ├── micro_clean.csv                   # 1,035 micro-creator videos (< 10K subs), cleaned
│   ├── large_clean.csv                   # 1,177 large-channel videos (> 10K subs), cleaned
│   ├── raw_collection.csv                # Raw API collection output
│   └── preprocessing_insights.csv        # High vs Low group comparison summary
├── notebooks/
│   ├── 01_data_collection.ipynb          # YouTube Data API v3 collection pipeline
│   ├── 02_data_preprocessing.ipynb       # Cleaning, feature engineering, group labeling
│   ├── 03_kmeans_clustering.ipynb        # Market segmentation (K-Means + PCA)
│   ├── 04_nlp_analysis.ipynb             # Sentiment, distinctive words, LDA topics
│   ├── 05_tag_strategy.ipynb             # Hashtag effectiveness + association rules
│   └── 06_time_series_posting.ipynb      # Golden posting windows by time & content type
├── outputs/                              # Generated charts and CSVs (created at runtime)
├── requirements.txt
└── .gitignore
```

---

## Pipeline

```
[YouTube Data API v3]
        ↓
01_data_collection.ipynb       → Raw video + channel data (~1,200 micro-creator videos)
        ↓
02_data_preprocessing.ipynb    → Cleaning · feature engineering · High/Low like-rate groups
        ↓
      ┌──────────────────────────────────────┐
      ↓                ↓            ↓         ↓
03_kmeans        04_nlp      05_tag_strategy  06_time_series
(Market Map)  (Sentiment+    (Hashtag         (Posting
              Topics)        Effectiveness)    Windows)
```

---

## Setup & Usage

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. (Optional) Collect fresh data

If you want to re-run data collection, open `notebooks/01_data_collection.ipynb` and replace `YOUR_YOUTUBE_API_KEY` with your own [YouTube Data API v3 key](https://console.cloud.google.com/). The pre-collected datasets are already included in `data/`.

### 3. Run analysis notebooks

The notebooks in `notebooks/` can be run independently starting from notebook `03` onward using the provided datasets. Notebooks `03`–`06` all load from `../data/micro_clean.csv` and `../data/large_clean.csv`.

```bash
jupyter notebook
# or
jupyter lab
```

Run notebooks in order:
1. `02_data_preprocessing.ipynb` — generates enriched datasets
2. `03_kmeans_clustering.ipynb` — market segmentation charts
3. `04_nlp_analysis.ipynb` — NLP outputs saved to `outputs/nlp_outputs/`
4. `05_tag_strategy.ipynb` — tag analysis charts
5. `06_time_series_posting.ipynb` — golden windows charts

---

## Data Description

### `micro_clean.csv` (1,035 rows · 45 columns)
Videos from channels with **< 10,000 subscribers**, collected via search queries targeting new creators (`"first vlog"`, `"study vlog"`, `"day in my life"`, etc.).

Key columns:
| Column | Description |
|--------|-------------|
| `video_id`, `video_title`, `description` | Core metadata |
| `view_count`, `like_count`, `comment_count` | Engagement metrics |
| `subscriber_count` | Channel size (< 10,000) |
| `like_rate` | `like_count / view_count` |
| `duration_sec` | Video length in seconds |
| `hashtag_count` | Total hashtags used |
| `publish_hour`, `post_day` | Posting time features |
| `is_vlog`, `is_short`, `is_daily_life`, `is_first_video` | Content type flags |
| `category_name` | YouTube category (e.g., People & Blogs, Gaming) |
| `source` | Dataset identifier (`micro`) |

### `large_clean.csv` (1,177 rows · 34 columns)
Videos from channels with **> 10,000 subscribers**, used as a benchmark comparison group.

---

## Methods

### K-Means Clustering (Notebook 03)
- Features: `efficiency_ratio` (views/subscribers), `like_rate`, `duration_sec`
- Preprocessing: log-transform + StandardScaler
- Optimal K: 4 (Elbow Method + PCA)
- Segments: *Rising Stars* · *Community Builders* · *Authority Archives* · *Viral Elite*

### NLP Analysis (Notebook 04)
- **VADER** sentiment scoring on title + description + comments
- **Distinctive word analysis**: frequency difference (High group − Low group)
- **Positive-text bigrams**: from strongly positive content (compound > 0.8)
- **LDA topic modeling**: 5 topics per group, topic saturation comparison

### Tag Strategy (Notebook 05)
- **2D Quadrant Framework**: Views × Like Rate → Golden / Niche / Exposure Trap / Ineffective
- **Tag type taxonomy**: Identity · Content-specific · Audience-descriptor · Format-chasing · Ambiguous
- **Association Rules** (Apriori, min_support=0.025, min_lift=1.3): co-occurring tag patterns per quadrant
- **Hashtag quantity analysis**: Pearson/Spearman correlation + partial correlation controlling for subscriber count

### Time-Series Posting Analysis (Notebook 06)
- **Heatmaps**: Median views by (day × hour) for micro vs large channels
- **Golden Window Score**: Micro performance rank − Large channel density rank
- Breakdown by content type (Vlog / Short / Daily Life), category, duration, and channel maturity

---

## Team

Columbia University APAN 5205 — Machine Learning II, Spring 2026
- Final project submitted for course credit

---

## Notes

- All data was collected via the YouTube Data API v3 under standard quota limits.
- The API key in `01_data_collection.ipynb` has been replaced with `YOUR_YOUTUBE_API_KEY`. Do not commit real API keys to version control.
- Timestamps in the dataset reflect UTC.
- The dataset skews toward South Asian and Indian content creators due to the search queries and YouTube's recommendation algorithm at collection time.
