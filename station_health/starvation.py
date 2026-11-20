from __future__ import annotations

import sqlite3
from datetime import UTC, date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status

from . import service
from .auth import current_operator_id
from .db import connect
from .schemas import StarvationResponse
from .supplied import DATABASE_PATH

router = APIRouter()

# async so setup, route and teardown run on the same thread
# (sqlite connections can't cross threads).
async def get_connection():
    connection = connect(DATABASE_PATH)
    try:
        yield connection
    finally:
        connection.close()

OperatorId = Annotated[int, Depends(current_operator_id)]
DbConnection = Annotated[sqlite3.Connection, Depends(get_connection)]


@router.get("/stations/{station_id}/starvation", 
            response_model=StarvationResponse,
            status_code=status.HTTP_200_OK,)
async def station_starvation(
    requested_date: Annotated[
        date, Query(alias="date", description="UTC calendar date, YYYY-MM-DD")
    ],
    station_id: Annotated[int, Path(gt=0, le=2**63 - 1)],
    operator_id: OperatorId,
    connection: DbConnection
):
    if requested_date > datetime.now(UTC).date():
        raise HTTPException(status_code=422, detail="Date cannot be in the future")

    try:
        return service.check_station_starvation(
            connection, operator_id, station_id, requested_date
        )
    except service.StationNotFound:
        raise HTTPException(status_code=404, detail="Station not found")
    except service.OperatorConfigMissing:
        raise HTTPException(status_code=500, detail="Operator configuration missing")