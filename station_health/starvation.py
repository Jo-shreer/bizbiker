from __future__ import annotations

from contextlib import closing
from datetime import UTC, date, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.concurrency import run_in_threadpool

from . import service
from .auth import current_operator_id
from .db import connect
from .schemas import StarvationResponse
from .supplied import DATABASE_PATH

router = APIRouter()

OperatorId = Annotated[int, Depends(current_operator_id)]

def _check(operator_id: int, station_id: int, requested_date: date):
    # Open, use and close on ONE worker thread, so SQLite never crosses threads.
    with closing(connect(DATABASE_PATH)) as connection:
        return service.check_station_starvation(
            connection, operator_id, station_id, requested_date
        )


@router.get(
    "/stations/{station_id}/starvation",
    response_model=StarvationResponse,
    status_code=status.HTTP_200_OK,
    responses={
        401: {"description": "Missing or invalid token"},
        404: {"description": "Station not found"},
        422: {"description": "Invalid station id or date, or date in the future"},
        500: {"description": "Operator configuration missing"},
    },
)
async def station_starvation(
    requested_date: Annotated[
        date, Query(alias="date", description="UTC calendar date, YYYY-MM-DD")
    ],
    station_id: Annotated[int, Path(gt=0, le=2**63 - 1)],
    operator_id: OperatorId,
):
    # Starvation is computed from recorded readings, so a future date is unknowable.
    if requested_date > datetime.now(UTC).date():
        raise HTTPException(status_code=422, detail="Date cannot be in the future")

    try:
        return await run_in_threadpool(_check, operator_id, station_id, requested_date)
    except service.StationNotFound:
        raise HTTPException(status_code=404, detail="Station not found")
    except service.OperatorConfigMissing:
        raise HTTPException(status_code=500, detail="Operator configuration missing")