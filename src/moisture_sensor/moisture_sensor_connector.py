from pydispatch import dispatcher

from event_signal import EventSignal
from moisture_sensor.moisture_sensor_manager import MoistureSensorManager


class MoistureSensorConnector:
    def __init__(
        self,
        moisture_sensor: MoistureSensorManager,
    ) -> None:
        self.moisture_sensor = moisture_sensor
        dispatcher.connect(
            self.measure_moisture,
            signal=EventSignal.REQUEST_MOISTURE_MEASUREMENTS,
        )

    def measure_moisture(self, event):
        print("event@measure_moisture")
        print(event)
        results = self.moisture_sensor.check_sensors(event)
        dispatcher.send(
            signal=EventSignal.MOISTURE_MEASUREMENT_RESULTS,
            sender=self,
            event=results,
        )
