from __future__ import annotations

from fastapi import FastAPI

from .starvation import router as starvation_router

app = FastAPI(title="Station Health")

app.include_router(starvation_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
