from collections import namedtuple
from typing import NamedTuple
from datetime import datetime


class MoistureMeasurementResult(NamedTuple):
    sensor: int
    moisture_measurement: float
    datetime: datetime
