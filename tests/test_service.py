from datetime import date
from zoneinfo import ZoneInfo

from station_health.service import build_window, is_starved


def test_is_starved_at_and_around_minimum():
    assert is_starved(3, 3) is True   # exactly the minimum counts
    assert is_starved(2, 3) is False
    assert is_starved(4, 3) is True


def test_build_window_is_utc():
    start, end = build_window(date(2026, 9, 15), "08:00", "10:00")
    assert start.isoformat() == "2026-09-15T08:00:00+00:00"
    assert end.isoformat() == "2026-09-15T10:00:00+00:00"


def test_build_window_other_operator():
    start, end = build_window(date(2026, 9, 15), "07:30", "09:30")
    assert start.isoformat() == "2026-09-15T07:30:00+00:00"
    assert end.isoformat() == "2026-09-15T09:30:00+00:00"


def test_build_window_converts_from_other_timezone():
    start, end = build_window(
        date(2026, 9, 15), "08:00", "10:00", ZoneInfo("Europe/Dublin")
    )
    assert start.isoformat() == "2026-09-15T07:00:00+00:00"  # summer time, UTC+1
    assert end.isoformat() == "2026-09-15T09:00:00+00:00"