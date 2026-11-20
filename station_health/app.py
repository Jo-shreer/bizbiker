from __future__ import annotations

import logging

from fastapi import FastAPI

from .middleware import request_context
from .starvation import router as starvation_router

app = FastAPI(title="Station Health")

logging.basicConfig(level=logging.INFO)

app.include_router(starvation_router)

app.middleware("http")(request_context)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
