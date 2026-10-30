"""Project-wide settings: seasons, thresholds, feature lists, weights, paths.

Everything tunable lives here so the other modules contain no magic numbers.
"""

from datetime import date
from pathlib import Path

# --- Seasons ---------------------------------------------------------------
FIRST_SEASON_START_YEAR = 1996  # the 1996-97 season


def season_label(start_year: int) -> str:
    """Turn a start year into NBA.com's season string, e.g. 1996 -> '1996-97'."""
    return f"{start_year}-{(start_year + 1) % 100:02d}"


def _current_season_start_year(today: date | None = None) -> int:
    """A new season starts in October, so before October we are still in last year's."""
    today = today or date.today()
    return today.year if today.month >= 10 else today.year - 1


FIRST_SEASON = season_label(FIRST_SEASON_START_YEAR)
SEASONS = [
    season_label(year)
    for year in range(FIRST_SEASON_START_YEAR, _current_season_start_year() + 1)
]

# --- Qualification thresholds ----------------------------------------------
MIN_GAMES_SEASON = 20
MIN_GAMES_CAREER = 100  # placeholder (README: TBD); revisit after looking at the data

# --- Features --------------------------------------------------------------
# Impact features are per 100 possessions; PLUS_MINUS is down-weighted.
IMPACT_FEATURES = [
    "PTS", "OREB", "DREB", "AST", "STL", "BLK", "TOV",
    "FGA", "FG3A", "FTA", "TS_PCT", "PLUS_MINUS",
]
PLUS_MINUS_WEIGHT = 0.5
FEATURE_WEIGHTS = {"PLUS_MINUS": PLUS_MINUS_WEIGHT}  # anything missing defaults to 1.0

# Play-style features are ratios, so they ignore volume.
STYLE_FEATURES = [
    "FG3A_RATE",      # 3PA / FGA
    "FTA_RATE",       # FTA / FGA
    "AST_SHARE",      # AST / (AST + FGA)
    "AST_TO_TOV",     # AST / TOV
    "OREB_SHARE",     # OREB / REB
    "STL_PER100",
    "BLK_PER100",
    "PTS_FROM_2_PCT",
    "PTS_FROM_3_PCT",
    "PTS_FROM_FT_PCT",
]

# --- Nearest neighbors ------------------------------------------------------
K_CAREERS = 50
K_SEASONS = 200  # larger because same-player pairs get filtered out
TOP_N_PAIRS = 50

# --- Storage and API --------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "data" / "nba.db"
DB_URL = f"sqlite:///{DB_PATH.as_posix()}"

API_DELAY_SECONDS = 2.0  # minimum gap between NBA.com requests
