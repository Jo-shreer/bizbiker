from __future__ import annotations

import sqlite3
from datetime import UTC, date as date_type, datetime, time
from typing import Annotated
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, HTTPException, Path

from .auth import current_operator_id
from .db import connect
from .supplied import DATABASE_PATH

router = APIRouter()

# Timezone in which peak_start/peak_end and the requested date are expressed.
# Per the brief this is UTC. Any IANA name works, e.g. "Europe/Paris".
PEAK_TIMEZONE = ZoneInfo("UTC")


# async so setup, route and teardown all run on the same thread
# (sqlite connections can't cross threads).
async def get_connection():
    connection = connect(DATABASE_PATH)
    try:
        yield connection
    finally:
        connection.close()


def is_starved(empty_count: int, min_empty_readings: int) -> bool:
    return empty_count >= min_empty_readings


def build_window(
    day: date_type,
    peak_start: str,
    peak_end: str,
    tz: ZoneInfo = PEAK_TIMEZONE,
):
    start = datetime.combine(day, time.fromisoformat(peak_start), tzinfo=tz).astimezone(UTC)
    end = datetime.combine(day, time.fromisoformat(peak_end), tzinfo=tz).astimezone(UTC)
    return start, end


@router.get("/stations/{station_id}/starvation")
async def station_starvation(
    date: date_type,
    station_id: Annotated[int, Path(gt=0, le=2**63 - 1)],
    operator_id: int = Depends(current_operator_id),
    connection: sqlite3.Connection = Depends(get_connection),
):
    # Scoped by operator: another operator's station looks the same as a missing one.
    station = connection.execute(
        "SELECT id FROM stations WHERE id = ? AND operator_id = ?",
        (station_id, operator_id),
    ).fetchone()
    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")

    config = connection.execute(
        "SELECT peak_start, peak_end, min_empty_readings "
        "FROM operator_configs WHERE operator_id = ?",
        (operator_id,),
    ).fetchone()
    if config is None:
        raise HTTPException(status_code=500, detail="Operator configuration missing")

    start, end = build_window(date, config["peak_start"], config["peak_end"])

    # Half-open window [start, end); DISTINCT collapses duplicate timestamps.
    empty_count = connection.execute(
        """
        SELECT COUNT(DISTINCT recorded_at) FROM dock_readings
        WHERE station_id = ? AND bikes_available = 0
          AND recorded_at >= ? AND recorded_at < ?
        """,
        (station_id, start.isoformat(), end.isoformat()),
    ).fetchone()[0]

    return {
        "station_id": station_id,
        "date": date.isoformat(),
        "starved": is_starved(empty_count, config["min_empty_readings"]),
        "empty_reading_count": empty_count,
        "min_empty_readings": config["min_empty_readings"],
        "window_start": start.isoformat(),
        "window_end": end.isoformat(),
    }
