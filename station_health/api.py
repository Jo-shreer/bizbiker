from __future__ import annotations

import sqlite3
from datetime import date as date_type
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path

from . import service
from .auth import current_operator_id
from .db import connect
from .schemas import StarvationResult
from .supplied import DATABASE_PATH

router = APIRouter()


# async so setup, route and teardown all run on the same thread
# (sqlite connections can't cross threads).
async def get_connection():
    connection = connect(DATABASE_PATH)
    try:
        yield connection
    finally:
        connection.close()


@router.get("/stations/{station_id}/starvation", response_model=StarvationResult)
async def station_starvation(
    date: date_type,
    station_id: Annotated[int, Path(gt=0, le=2**63 - 1)],
    operator_id: int = Depends(current_operator_id),
    connection: sqlite3.Connection = Depends(get_connection),
):
    try:
        return service.check_station_starvation(connection, operator_id, station_id, date)
    except service.StationNotFound:
        raise HTTPException(status_code=404, detail="Station not found")
    except service.OperatorConfigMissing:
        raise HTTPException(status_code=500, detail="Operator configuration missing")
