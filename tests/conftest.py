"""Shared pytest fixtures: tiny hand-made player tables so tests never touch NBA.com."""

import pandas as pd
import pytest


@pytest.fixture
def fake_totals() -> pd.DataFrame:
    """A few invented player-seasons with easy-to-check numbers (include a 0-FGA and a 0-TOV row)."""
    # TODO
    raise NotImplementedError


@pytest.fixture
def fake_per100() -> pd.DataFrame:
    """Matching per-100 table for the same invented players."""
    # TODO
    raise NotImplementedError
