from __future__ import annotations

from datetime import date as date_type
from datetime import datetime

from pydantic import BaseModel


class StarvationResponse(BaseModel):
    station_id: int
    date: date_type
    starved: bool
    empty_reading_count: int
    min_empty_readings: int
    window_start: datetime
    window_end: datetime