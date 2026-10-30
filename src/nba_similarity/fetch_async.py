"""OPTIONAL (Phase 4): asyncio fetcher that limits concurrency with a semaphore."""

import pandas as pd


async def fetch_season_async(season: str, mode: str, semaphore) -> pd.DataFrame:
    """Fetch one season without blocking the event loop, holding the semaphore while requesting."""
    # TODO
    raise NotImplementedError


async def fetch_all_async(seasons: list[str], max_concurrent: int = 2) -> dict[str, pd.DataFrame]:
    """Fetch many seasons concurrently, at most `max_concurrent` at a time."""
    # TODO
    raise NotImplementedError
