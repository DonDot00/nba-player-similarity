"""Runs the whole project end to end: fetch -> features -> similarity -> outputs/.

Run with: python -m nba_similarity.pipeline
"""


def run() -> None:
    """Fetch any missing seasons, build features, and write the four top-50 tables to outputs/."""
    # TODO: wire the other modules together (wrap steps with @timed)
    raise NotImplementedError


if __name__ == "__main__":
    run()
