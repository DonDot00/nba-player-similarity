"""nba_api calls and the fetch_seasons() generator. (Phase 1: you write this.)"""

from collections.abc import Iterator

import pandas as pd


def fetch_season(season: str, mode: str) -> pd.DataFrame:
    """Download one season from LeagueDashPlayerStats.

    `season` looks like '2003-04'; `mode` is 'per100' or 'totals'.
    Should be decorated with @rate_limited and @cache_to_sqlite once those exist.
    """
    # TODO
    raise NotImplementedError


def fetch_seasons(seasons: list[str]) -> Iterator[tuple[str, pd.DataFrame]]:
    """Generator: yield (season, DataFrame) one season at a time.

    Streaming keeps only one season in memory while data flows into SQLite.
    """
    # TODO
    raise NotImplementedError
