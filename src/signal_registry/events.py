from typing import List

from moisture_sensor.moisture_measurement_result import MoistureMeasurementResult


class RequestMoistureMeasurementEvent:
    def __init__(self, sensors: List[int]) -> None:
        self.sensors = sensors


class MoistureMeasurementsResultEvent:
    def __init__(self, results: List[MoistureMeasurementResult]) -> None:
        self.sensors = results


class MoistureMeasurementResultEvent:
    def __init__(self, result: MoistureMeasurementResult) -> None:
        self.result = result

    def __str__(self):
        return f"<{self.__class__.__name__} for result: {self.result}>"


class IrrigationEvent:
    def __init__(self, valve: int, time_in_s: float) -> None:
        self.valve = valve
        self.time_in_s = time_in_s


class PanicEvent:
    def __init__(self, reason: str) -> None:
        self.reason = reason


class UpdateDisplayEvent:
    def __init__(self, line_1: str, line_2: str) -> None:
        self.line_1 = line_1
        self.line_2 = line_2

    def __str__(self):
        return f'<{self.__class__.__name__} for "{self.line_1}" "{self.line_2}">'


class ButtonEvent:
    def __init__(self, button: str) -> None:
        self.button = button

    def __str__(self):
        return f"<{self.__class__.__name__} for {self.button}>"
