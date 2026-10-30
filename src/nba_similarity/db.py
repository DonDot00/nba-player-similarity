"""SQLAlchemy engine, table definitions, and read/write helpers for the SQLite cache."""

import pandas as pd
from sqlalchemy import Engine


def get_engine() -> Engine:
    """Return an engine for the database at config.DB_URL (create the data/ folder if needed)."""
    # TODO
    raise NotImplementedError


def save_season(df: pd.DataFrame, season: str, mode: str) -> None:
    """Write one season's stats (mode: 'per100' or 'totals') to the database."""
    # TODO
    raise NotImplementedError


def season_is_cached(season: str, mode: str) -> bool:
    """Return True if this season/mode has already been downloaded."""
    # TODO
    raise NotImplementedError


def load_seasons(mode: str) -> pd.DataFrame:
    """Load every stored season for `mode` into one DataFrame (with a SEASON column)."""
    # TODO
    raise NotImplementedError
