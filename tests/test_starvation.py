from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

import station_health.starvation as starvation
from seed import build_database
from station_health.app import app

METRO = {"Authorization": "Bearer metro-token"}
HARBOUR = {"Authorization": "Bearer harbour-token"}


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = build_database(tmp_path / "test.db")
    monkeypatch.setattr(starvation, "DATABASE_PATH", db_path)
    return TestClient(app)


def get(client, station, headers=METRO, date="2026-09-15"):
    return client.get(
        f"/stations/{station}/starvation?date={date}", headers=headers
    )


# --- Results against the seed data ---

@pytest.mark.parametrize(
    "station, headers, count, starved",
    [
        (101, METRO, 3, True),    # excludes 07:45, 10:00 and the 14 Sept reading
        (102, METRO, 2, False),   # below threshold
        (103, METRO, 3, True),    # docks_total=0, counted literally
        (104, METRO, 2, False),   # duplicate timestamp counted once
        (201, HARBOUR, 2, True),  # operator 2 window and minimum
        (202, HARBOUR, 1, False),
    ],
)
def test_seeded_stations(client, station, headers, count, starved):
    response = get(client, station, headers)
    assert response.status_code == 200
    body = response.json()
    assert body["empty_reading_count"] == count
    assert body["starved"] is starved


def test_no_readings_on_date(client):
    response = get(client, 101, date="2026-01-01")
    assert response.status_code == 200
    body = response.json()
    assert body["empty_reading_count"] == 0
    assert body["starved"] is False


def test_response_shape(client):
    body = get(client, 101).json()
    assert set(body) == {
        "station_id",
        "date",
        "starved",
        "empty_reading_count",
        "min_empty_readings",
        "window_start",
        "window_end",
    }


# --- Operator isolation ---

def test_other_operator_looks_like_missing_station(client):
    cross = get(client, 101, HARBOUR)
    missing = get(client, 999, HARBOUR)
    assert cross.status_code == missing.status_code == 404
    assert cross.json() == missing.json()


def test_metro_cannot_see_harbour_station(client):
    assert get(client, 201, METRO).status_code == 404


# --- Authentication ---

def test_missing_token_is_401(client):
    response = client.get("/stations/101/starvation?date=2026-09-15")
    assert response.status_code == 401


def test_unknown_token_is_401(client):
    response = get(client, 101, {"Authorization": "Bearer nope"})
    assert response.status_code == 401


# --- Validation ---

@pytest.mark.parametrize("bad_date", ["15-09-2026", "abc", "2026-13-01", "2026-02-30"])
def test_bad_date_is_422(client, bad_date):
    assert get(client, 101, date=bad_date).status_code == 422


@pytest.mark.parametrize("station_id", [0, -1, 2**63, "abc"])
def test_bad_station_id_is_422(client, station_id):
    assert get(client, station_id).status_code == 422


def test_future_date_is_422(client):
    tomorrow = (datetime.now(UTC) + timedelta(days=1)).date().isoformat()
    assert get(client, 101, date=tomorrow).status_code == 422