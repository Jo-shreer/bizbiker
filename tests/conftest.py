from __future__ import annotations

from pathlib import Path

import pytest

from seed import build_database


@pytest.fixture
def database_path(tmp_path: Path) -> Path:
    return build_database(tmp_path / "station_health.db")
