from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime, time
from datetime import date as date_type
from zoneinfo import ZoneInfo

from . import repository
from .schemas import StarvationResponse

PEAK_TIMEZONE = ZoneInfo("UTC")


class StationNotFound(Exception):
    pass


class OperatorConfigMissing(Exception):
    pass


@dataclass(frozen=True)
class StarvationResult:
    station_id: int
    date: date_type
    starved: bool
    empty_reading_count: int
    min_empty_readings: int
    window_start: datetime
    window_end: datetime


def is_starved(empty_count: int, min_empty_readings: int) -> bool:
    return empty_count >= min_empty_readings


def build_window(
    requested_date: date_type,
    peak_start: str,
    peak_end: str,
    tz: ZoneInfo = PEAK_TIMEZONE,
) -> tuple[datetime, datetime]:
    start = datetime.combine(
        requested_date, time.fromisoformat(peak_start), tzinfo=tz
    ).astimezone(UTC)
    end = datetime.combine(
        requested_date, time.fromisoformat(peak_end), tzinfo=tz
    ).astimezone(UTC)
    return start, end


def check_station_starvation(
    connection: sqlite3.Connection,
    operator_id: int,
    station_id: int,
    requested_date: date_type,
) -> StarvationResult:

    if not repository.station_belongs_to_operator(connection, station_id, operator_id):
        raise StationNotFound

    config = repository.get_operator_config(connection, operator_id)
    if config is None:
        raise OperatorConfigMissing

    start, end = build_window(requested_date, config.peak_start, config.peak_end)

    empty_count = repository.count_empty_readings(connection, station_id, start, end)

    return StarvationResponse(
        station_id=station_id,
        date=requested_date,
        starved=is_starved(empty_count, config.min_empty_readings),
        empty_reading_count=empty_count,
        min_empty_readings=config.min_empty_readings,
        window_start=start,
        window_end=end,
    )
