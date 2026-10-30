"""Feature engineering. (Phase 2: you write these.)

Builds impact and play-style features, season z-scores, and career aggregates.
"""

import numpy as np
import pandas as pd


def safe_divide(numerator, denominator, fill: float = 0.0):
    """Element-wise division that returns `fill` wherever the denominator is 0."""
    # TODO
    raise NotImplementedError


def filter_qualifying_seasons(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only player-seasons with at least config.MIN_GAMES_SEASON games."""
    # TODO
    raise NotImplementedError


def add_impact_features(per100: pd.DataFrame, totals: pd.DataFrame) -> pd.DataFrame:
    """Return per-100 impact features (including TS%) for each player-season."""
    # TODO
    raise NotImplementedError


def add_style_features(totals: pd.DataFrame) -> pd.DataFrame:
    """Return the volume-free ratio features (3PA/FGA, AST/TOV, ...) for each player-season."""
    # TODO
    raise NotImplementedError


def zscore_within_season(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    """Standardize each feature against its own season (use groupby('SEASON').transform)."""
    # TODO
    raise NotImplementedError


def apply_weights(df: pd.DataFrame, weights: dict[str, float]) -> pd.DataFrame:
    """Multiply feature columns by their weights (missing columns default to 1.0)."""
    # TODO
    raise NotImplementedError


def aggregate_careers(df: pd.DataFrame, feature_cols: list[str]) -> pd.DataFrame:
    """Collapse seasons into one row per player: minutes-weighted mean of season z-scores.

    Drops players below config.MIN_GAMES_CAREER total games.
    """
    # TODO
    raise NotImplementedError


def to_feature_matrix(df: pd.DataFrame, feature_cols: list[str]) -> np.ndarray:
    """Return the features as a float32 NumPy matrix."""
    # TODO
    raise NotImplementedError
