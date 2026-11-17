from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class OperatorConfig:
    peak_start: str
    peak_end: str
    min_empty_readings: int


def station_belongs_to_operator(
    connection: sqlite3.Connection, station_id: int, operator_id: int
) -> bool:
    row = connection.execute(
        "SELECT 1 FROM stations WHERE id = ? AND operator_id = ?",
        (station_id, operator_id),
    ).fetchone()
    return row is not None


def get_operator_config(
    connection: sqlite3.Connection, operator_id: int
) -> OperatorConfig | None:
    row = connection.execute(
        "SELECT peak_start, peak_end, min_empty_readings "
        "FROM operator_configs WHERE operator_id = ?",
        (operator_id,),
    ).fetchone()
    return OperatorConfig(**dict(row)) if row else None


def count_empty_readings(
    connection: sqlite3.Connection,
    station_id: int,
    start: datetime,
    end: datetime,
) -> int:
    # Half-open window [start, end); DISTINCT collapses duplicate timestamps.
    return connection.execute(
        """
        SELECT COUNT(DISTINCT recorded_at) FROM dock_readings
        WHERE station_id = ? AND bikes_available = 0
          AND recorded_at >= ? AND recorded_at < ?
        """,
        (station_id, start.isoformat(), end.isoformat()),
    ).fetchone()[0]


