from __future__ import annotations

import sqlite3
from datetime import UTC, date as date_type, datetime, time
from zoneinfo import ZoneInfo

from . import repository
from .schemas import StarvationResult

# Timezone in which peak_start/peak_end and the requested date are expressed.
# Per the brief this is UTC. Any IANA name works.
PEAK_TIMEZONE = ZoneInfo("UTC")


class StationNotFound(Exception):
    pass


class OperatorConfigMissing(Exception):
    pass


def is_starved(empty_count: int, min_empty_readings: int) -> bool:
    return empty_count >= min_empty_readings


def build_window(
    day: date_type,
    peak_start: str,
    peak_end: str,
    tz: ZoneInfo = PEAK_TIMEZONE,
) -> tuple[datetime, datetime]:
    start = datetime.combine(day, time.fromisoformat(peak_start), tzinfo=tz).astimezone(UTC)
    end = datetime.combine(day, time.fromisoformat(peak_end), tzinfo=tz).astimezone(UTC)
    return start, end


def check_station_starvation(
    connection: sqlite3.Connection,
    operator_id: int,
    station_id: int,
    day: date_type,
) -> StarvationResult:
    # Scoped by operator: another operator's station looks the same as a missing one.
    if not repository.station_belongs_to_operator(connection, station_id, operator_id):
        raise StationNotFound

    config = repository.get_operator_config(connection, operator_id)
    if config is None:
        raise OperatorConfigMissing

    start, end = build_window(day, config.peak_start, config.peak_end)
    empty_count = repository.count_empty_readings(connection, station_id, start, end)

    return StarvationResult(
        station_id=station_id,
        date=day,
        starved=is_starved(empty_count, config.min_empty_readings),
        empty_reading_count=empty_count,
        min_empty_readings=config.min_empty_readings,
        window_start=start,
        window_end=end,
    )
