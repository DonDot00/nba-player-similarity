"""FastAPI app. (Phase 4)

GET /similar/{player}?mode=impact|style&level=season|career
"""

from fastapi import FastAPI

app = FastAPI(title="NBA Player Similarity")


@app.get("/similar/{player}")
async def similar(player: str, mode: str = "impact", level: str = "season"):
    """Return the players most similar to `player` for the given mode and level."""
    # TODO
    raise NotImplementedError
