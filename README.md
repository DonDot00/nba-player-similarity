# NBA Player Similarity

Find the NBA players whose games look the most alike, measured two different ways:

1. **Impact similarity:** do two players put up the same *amount* of production across the box score, including plus-minus?
2. **Play-style similarity:** do two players produce the same *mix* of stats, regardless of volume? A star and a role player can share a style even when their impact is very different.

Each comparison runs on two levels:

| | Impact | Play style |
|---|---|---|
| **Seasons** (one player-season vs. another) | Top 50 most similar pairs | Top 50 most similar pairs |
| **Careers** (whole careers vs. each other) | Top 50 most similar pairs | Top 50 most similar pairs |

That gives four ranked lists. The most interesting output comes from comparing them: **pairs that rank high on style but low on impact** are players who play the same way at very different levels.

---

## Why I'm building this: a learning project

Besides answering a basketball question, this project is a deliberate way for me to **practice and strengthen Python concepts I haven't used much in real projects yet**. I'm writing the core code myself so I learn each concept by applying it to a real problem, not just reading about it.

| Concept | Where I practice it in this project |
|---|---|
| **Decorators** | `@rate_limited` to space out API calls, `@cache_to_sqlite` so each season is downloaded only once, `@timed` to measure how long each pipeline step takes |
| **Generators** | `fetch_seasons()` yields one season at a time so data streams into SQLite instead of sitting in memory; a generator that yields valid pairs while filtering out same-player matches |
| **NumPy / Pandas** | Cleaning the data, per-100 stats, ratio features, z-scores within each season (`groupby().transform()`), minutes-weighted career aggregation, `float32` feature matrices |
| **Testing (pytest)** | Testing feature formulas on hand-made players, divide-by-zero edge cases, z-score properties, pair filtering, distance symmetry, and decorators; mocking the API so tests never hit NBA.com |
| **Async basics** | `async def` FastAPI endpoints; an optional `asyncio` fetcher that uses a semaphore to keep requests polite |

My goal is to be able to explain how and why each of these works, not just to have code that runs.

---

## Data

- **Source:** [`nba_api`](https://pypi.org/project/nba-api/), a Python client for NBA.com's stats endpoints.
- **Main endpoint:** `LeagueDashPlayerStats`, which returns every player's season stats in one call. Each season is pulled in two modes:
  - **Per 100 possessions** for the impact features (fair across minutes played and pace)
  - **Totals** for building the ratios
- **Seasons covered:** 1996–97 to the present (the range NBA.com's detailed stats generally cover).
- **Storage:** every pull is cached in a local SQLite database (via SQLAlchemy). All analysis runs from the database, never live from the API.
- **Being a good API citizen:** NBA.com rate-limits heavy traffic, so requests are spaced out (about 2 or more seconds apart) and nothing is re-downloaded once it's cached.

### Who qualifies

- **Season search:** a player-season counts if the player appeared in **20+ games** that season.
- **Career search:** built from a player's qualifying seasons. Career minimum: **[TBD, e.g. 100+ games]**, so short careers don't clutter the results.

---

## Methodology

### Impact features (per 100 possessions)

PTS, OREB, DREB, AST, STL, BLK, TOV, FGA, 3PA, FTA, TS%, and **plus-minus**

- Plus-minus depends heavily on teammates, so it gets a **lower weight (0.5)** after standardizing.
- Redundant scoring stats (e.g., FGM alongside PTS and FGA) are left out so scoring isn't counted multiple times.

### Play-style features (volume-free)

| Feature | What it captures |
|---|---|
| 3PA / FGA | How perimeter-oriented the player is |
| FTA / FGA | How often they get to the line |
| AST / (AST + FGA) | Passer vs. shooter |
| AST / TOV | Ball security |
| OREB / REB | Crashing the glass vs. defensive boards |
| STL per 100 | Perimeter disruption (kept separate from blocks) |
| BLK per 100 | Rim protection (kept separate from steals) |
| % of points from 2s / 3s / FTs | Where the scoring comes from |

Divide-by-zero cases (e.g., 0 FGA or 0 TOV) are handled explicitly and tested.

### Standardization

- **Seasons:** each feature is turned into a z-score **against that season's league**, not all seasons combined. This adjusts for era (pace, the three-point boom), so a 2001 season and a 2024 season are each judged against their own league.
- **Careers:** a player's career feature is the **minutes-weighted average of their season z-scores**. This is era-adjusted, and short seasons count less than full ones.

### Finding the top 50 pairs

- **Distance:** Euclidean distance on the standardized (and weighted) features. Smaller means more similar.
- **No full distance matrix:** about 13,000 player-seasons would need a ~1.3 GB matrix. Instead, scikit-learn's `NearestNeighbors` finds each row's k nearest neighbors.
  - With k = 50, the exact top 50 pairs are guaranteed to appear among the neighbor lists.
  - The season search uses a larger k (~200) because **same-player pairs** (LeBron 2012 vs. LeBron 2013) are filtered out.
- Pairs are de-duplicated (A–B = B–A), and the 50 smallest distances are kept.

### Checking the results

- Sanity checks: similar archetypes should match (two traditional bigs, two high-volume three-point guards).
- A 2D PCA plot of every player, colored by position, to see whether the clusters make sense.

---

## Tech stack

- **Python 3.11+**
- **Data:** `nba_api`, `pandas`, `numpy`
- **Similarity:** `scikit-learn` (`NearestNeighbors`, `StandardScaler`, `PCA`)
- **Storage:** SQLite + SQLAlchemy
- **Testing:** `pytest`
- **API (later):** FastAPI
- **Frontend (later):** React + Vite, with radar charts for side-by-side player comparisons

---

## Project structure

```
nba-player-similarity/
├── README.md
├── requirements.txt
├── .gitignore
├── data/                     # SQLite database (gitignored)
├── notebooks/                # exploration and plots
├── outputs/                  # top-50 result tables
├── src/nba_similarity/
│   ├── __init__.py
│   ├── config.py             # seasons, thresholds, feature lists, weights
│   ├── decorators.py         # @rate_limited, @cache_to_sqlite, @timed
│   ├── db.py                 # SQLAlchemy models and helpers
│   ├── fetch.py              # nba_api calls + fetch_seasons() generator
│   ├── fetch_async.py        # optional asyncio fetcher with a semaphore
│   ├── features.py           # impact and style features, z-scores, career aggregation
│   ├── similarity.py         # nearest neighbors, pair filtering, top-50 ranking
│   ├── pipeline.py           # runs everything end to end
│   └── api/
│       └── main.py           # FastAPI: GET /similar/{player}?mode=impact|style&level=season|career
└── tests/
    ├── conftest.py           # shared fixtures (tiny fake player tables)
    ├── test_decorators.py
    ├── test_features.py
    └── test_similarity.py
```

---

## Roadmap

Each phase is built around one or two concepts so I learn them one at a time.

- [ ] **Phase 1: Data collection** *(decorators, generators)*
  - Fetch one season with `nba_api`, then write `@rate_limited` and `@cache_to_sqlite`
  - Write the `fetch_seasons()` generator and fill the database for 1996–97 to now
- [ ] **Phase 2: Features** *(NumPy / Pandas, testing)*
  - Build the impact and style features, with tests for every formula and edge case
  - Season-level z-scores and minutes-weighted career aggregation
- [ ] **Phase 3: Similarity** *(NumPy, testing)*
  - Nearest neighbors, same-player filtering, de-duplication, top 50 for all four searches
  - Sanity checks and a PCA plot
- [ ] **Phase 4: Serve it** *(async basics)*
  - FastAPI endpoints with `async def`
  - Optional: an asyncio fetcher with a semaphore
- [ ] **Phase 5: Frontend**
  - React page: player search, impact and style matches side by side, radar chart

---

## Setup

```bash
git clone <repo-url>
cd nba-player-similarity
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Run the tests:

```bash
pytest
```

Run the pipeline (once implemented):

```bash
python -m nba_similarity.pipeline
```

---

## Limitations

- Box-score stats don't capture everything, especially defense beyond steals and blocks.
- Plus-minus is noisy and team-dependent, which is why it gets a lower weight.
- Similarity depends on which features are chosen and how they're weighted. Different choices give different answers.
- The data covers 1996–97 onward, so earlier eras aren't included.

---

## Learning log

*Notes to myself as I go: what clicked, what confused me, and what I'd do differently.*

- **Decorators:**
- **Generators:**
- **NumPy / Pandas:**
- **Testing:**
- **Async:**
