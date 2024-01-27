from collections import namedtuple
from typing import NamedTuple
from datetime import datetime


class MoistureMeasurementResult(NamedTuple):
    sensor: int
    moisture_measurement: float
    datetime: datetime

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} for {self.sensor}, moisture_measurement: {self.moisture_measurement}>"
