# Planning: NBA Player Similarity

The team's working plan: who owns what, the one-week schedule, step-by-step checklists for each role, and how we work with git and Claude Code.

---

## Team and roles

| Role | Person | Owns | Concepts practiced most |
|---|---|---|---|
| **A: Data** | [Name] | `fetch.py`, `decorators.py`, `db.py`, `data/raw/` | Decorators, generators |
| **B: Features** | [Name] | `features.py` | Pandas/NumPy, testing |
| **C: Similarity + API** | [Name] | `similarity.py`, `api/main.py`, `fetch_async.py` | NumPy, async |

**Difficulty:** B is the most approachable, A is medium (decorators with arguments, API quirks), and C is the hardest (pair logic, async, and integration with everyone else's work).

### Cross-training rules (so everyone learns every concept)

- **Everyone writes at least one decorator:** A writes `@rate_limited` and `@cache_to_sqlite`, B writes `@timed`, C writes `@requires_columns`.
- **Everyone writes at least one generator:** A writes `fetch_seasons()`, B writes `iter_seasons_from_db()`, C writes `iter_valid_pairs()`.
- **You test someone else's code:** A tests C's module, B tests A's module, C tests B's module.
- **Everyone writes at least one async FastAPI endpoint.**

---

## One-week schedule

| Day | Together | A: Data | B: Features | C: Similarity + API |
|---|---|---|---|---|
| **1** | Kickoff + setup | Download all seasons, commit raw files | Impact features (fake data) | Nearest neighbors (fake data) |
| **2** | | `db.py`, `@cache_to_sqlite` | Style ratios + tests | Pair generator |
| **3** | | `@rate_limited`, `fetch_seasons()` | Z-scores, careers, `@timed` | Top 50 × 4, `@requires_columns` |
| **4** | **Switch to real data** | Tests for C | Tests for A, save feature tables | Tests for B |
| **5** | | `/players` endpoint | PCA plot, `/players/{id}/features` | `/similar`, `/top-pairs`, async fetcher |
| **6** | Sanity checks + bug fixes | | | |
| **7** | Write-up, Learning log, demo | | | |

If something takes longer, that's okay. Push the frontend and polish past the week, but keep the handoffs on track.

### Handoff points

| When | Handoff | If it's late |
|---|---|---|
| End of Day 1 | A commits the raw data files to `data/raw/` | B and C keep working on fake data |
| End of Day 3 | B's feature functions work on fake data | C keeps using the fake feature table |
| Day 4 | Everyone switches to real data | Pair up on whatever is blocking |

---

## Day 1: everyone together (kickoff, about 2 hours)

- [ ] Create the private GitHub repo, add all three of us as collaborators, and protect `main` so changes require a PR.
- [ ] Everyone clones it, makes a venv, runs `pip install -r requirements.txt`, and runs `pytest`. The stubs should load without errors.
- [ ] Agree on the **data formats** and write them in `docs/data_contracts.md`:
  - Raw season table (A → B): `player_id, player_name, season, team, gp, min, pts, oreb, dreb, ast, stl, blk, tov, fgm, fga, fg3m, fg3a, ftm, fta, plus_minus` (per-100 and totals versions)
  - Feature table (B → C): `player_id, player_name, season (or "career"), level, mode, <feature columns...>`
- [ ] Put small **fake versions** of both tables (about 10 made-up players over 2 seasons) in `tests/conftest.py`.
- [ ] Add a GitHub Actions workflow that runs `pytest` on every PR.
- [ ] Turn the checklists below into GitHub Issues and assign them.
- [ ] Decide the **career minimum games** (suggested: 100) and put it in `config.py`.

---

## Role A: Data (decorators, generators, database)

**Day 1**
- [ ] Fetch **one** season from `LeagueDashPlayerStats` in both `Per100Possessions` and `Totals` modes. Look at the columns, and update `docs/data_contracts.md` if anything differs.
- [ ] Check how **traded players** appear (one combined row, or one row per team). Decide how to handle them, and tell B.
- [ ] Write a simple script that downloads every season from 1996–97 to now (with a `time.sleep` between calls for now) and saves:
  - `data/raw/season_stats_per100.parquet`
  - `data/raw/season_stats_totals.parquet`
- [ ] Check the files are under 50 MB, then commit them so everyone has the data.

**Day 2**
- [ ] Build `db.py`: a SQLAlchemy model for raw season stats, `load_raw_into_db()`, `save_season()`, and `load_season()`.
- [ ] Write **`@cache_to_sqlite`**: if the season is already in the database, return it. Otherwise, call the wrapped function and save the result.

**Day 3**
- [ ] Write **`@rate_limited(seconds=2)`**. It's a decorator *with arguments*, which means three nested functions. Learn why.
- [ ] Write the **`fetch_seasons(start, end)` generator**. It yields one season's DataFrame at a time and uses both decorators. Use it to refresh the current season.
- [ ] Replace the Day 1 `time.sleep` script with `fetch_seasons()`.

**Day 4**
- [ ] Write **tests for C's `similarity.py`**: a player's distance to himself is 0, distances are symmetric, no same-player pairs appear, and the expected nearest neighbor is found in a tiny dataset.
- [ ] Help B load the real data.

**Day 5**
- [ ] Write the async endpoint `GET /players?search=` (case-insensitive name search).

**Days 6–7**
- [ ] Sanity checks with the team, then write your part of the Learning log and demo the data pipeline.

---

## Role B: Features (Pandas/NumPy, testing)

**Day 1** (using the fake data)
- [ ] Build the **impact features** (per 100): PTS, OREB, DREB, AST, STL, BLK, TOV, FGA, 3PA, FTA, plus-minus, and **TS% = PTS / (2 × (FGA + 0.44 × FTA))**.
- [ ] Write a test for each formula using a hand-made player whose correct answers you've worked out yourself.

**Day 2**
- [ ] Build the **style features** with safe division: 3PA/FGA, FTA/FGA, AST/(AST+FGA), AST/TOV, OREB/REB, STL per 100, BLK per 100.
- [ ] Build **share of points from 2s, 3s, and FTs** from the totals (2s = 2 × (FGM − FG3M), 3s = 3 × FG3M, FTs = FTM).
- [ ] Decide what 0 FGA, 0 TOV, or 0 REB should produce, write it down, and test it.

**Day 3**
- [ ] Compute **z-scores within each season**: `groupby("season").transform(lambda s: (s - s.mean()) / s.std())`. Apply the **0.5 weight** to plus-minus afterward.
- [ ] Test that every season has mean ≈ 0 and std ≈ 1.
- [ ] Build **career features**: minutes-weighted average of each player's season z-scores, then apply the career game minimum.
- [ ] Write **`@timed`** and put it on each feature step.
- [ ] Write the **`iter_seasons_from_db()` generator**.

**Day 4**
- [ ] Switch to the real data, and save four feature tables to the database: impact/style × season/career.
- [ ] Write **tests for A's code**: `@rate_limited` actually waits, `@cache_to_sqlite` skips the API when the data is cached, and `fetch_seasons()` yields the right number of seasons. **Mock the API** so the tests never call NBA.com.

**Day 5**
- [ ] Make a PCA notebook: plot every player in 2D, colored by position, and save the image for the README.
- [ ] Write the async endpoint `GET /players/{id}/features`.

**Days 6–7**
- [ ] Sanity checks with the team, then write your part of the Learning log and demo the features.

---

## Role C: Similarity + API (NumPy, async)

**Day 1** (using the fake feature table)
- [ ] Build the nearest-neighbor search: a `float32` feature matrix fed into `NearestNeighbors(n_neighbors=k, n_jobs=-1)`, with k from `config.py` (50 for careers, 200 for seasons).
- [ ] Understand why k = 50 guarantees the exact top 50 pairs for careers, and why seasons need a bigger k.

**Day 2**
- [ ] Write the **`iter_valid_pairs()` generator**. It skips same-player pairs, removes duplicates (A–B = B–A), and yields `(player_a, player_b, distance)`.

**Day 3**
- [ ] Produce the **top 50 pairs for all four searches**, and save them to `outputs/*.csv` and the database.
- [ ] Write **`@requires_columns(...)`**, which raises a clear error if a DataFrame is missing the expected columns. Use it on your functions.

**Day 4**
- [ ] Run on the real feature tables from B.
- [ ] Write **tests for B's `features.py`**: formula values, divide-by-zero cases, z-score properties, and career weighting.

**Day 5**
- [ ] Build the FastAPI app with async endpoints:
  - `GET /similar/{player}?mode=impact|style&level=season|career`
  - `GET /top-pairs?mode=impact|style&level=season|career`
- [ ] Build `fetch_async.py`, an asyncio fetcher that uses `asyncio.Semaphore(1)` and `asyncio.to_thread()` around the `nba_api` calls (since `nba_api` isn't async).

**Days 6–7**
- [ ] Lead the sanity checks: do the matches make basketball sense? Find the most interesting **close-on-style, far-on-impact** pairs for the write-up. Write your part of the Learning log and demo the API.

---

## Data rules

- The raw data is downloaded **once** by A and committed to `data/raw/` as Parquet or CSV.
- **Never commit the SQLite `.db` file.** Each person builds it locally from the raw files.
- If a file goes over ~50 MB, upload it as a GitHub Release asset instead and add a download script.
- Keep the repo **private** while it contains NBA.com data. Check the data terms before making it public.

---

## Git workflow

- Never push directly to `main`.
- One branch per task: `feature/<short-name>` (e.g. `feature/rate-limiter`).
- Open a PR. **One teammate must approve before merging**, and CI (`pytest`) must pass.
- Small PRs, merged often, at least once a day.
- Commit messages are written by us, in our own words. **No AI co-author or attribution lines.**

---

## Working with Claude Code

Start every session with: **"Read PLANNING.md first."**

### Tutoring rules

This is a learning project. Each of us is writing the core code ourselves to learn decorators, generators, NumPy/Pandas, pytest, and async.

- Briefly explain the concept first, with a small example that is **not** the project code.
- Tell me what to build and which file it goes in, then **let me write it**.
- When I'm stuck, start with small hints. Give a full solution **only if I explicitly ask**.
- Review my code: bugs, edge cases, more Pythonic approaches, and why.
- Help me write tests for what I built.
- Before moving on, ask 1–2 quick questions to check I understand it, and suggest a line for the README Learning log.
- Boilerplate that isn't a learning concept (SQLAlchemy setup, plot styling, FastAPI wiring) is fine to write, but explain it.
- Stub files in `src/nba_similarity/` and `tests/` are intentionally unimplemented. Leave them for the person who owns them unless they explicitly ask for a full solution.
- Check off finished roadmap items in `README.md`.

### Code conventions

- Python 3.11+, source under `src/nba_similarity/`, tests under `tests/` (pytest).
- Settings and magic numbers live in `config.py`.
- Tests must never hit NBA.com. Mock the API.
- Be polite to NBA.com: rate-limit requests, and cache everything (SQLite locally, raw files in `data/raw/`).

### Module ownership

- Only edit files owned by the person you're working with (see **Team and roles**).
- If a change is needed in someone else's file, describe it so it can be raised with them. Don't make it.

### Not a collaborator

- Claude Code is a tutoring tool, not a team member. We use it only as a coding helper, the same way any developer uses an editor, linter, or search engine. The `.claude/` folder is committed so the tool behaves the same for all three of us.
- Never add `Co-Authored-By`, "Generated with Claude Code", or any Claude/Anthropic attribution to commits, PRs, or files.
- Never list Claude as a contributor or author anywhere in the repo.
