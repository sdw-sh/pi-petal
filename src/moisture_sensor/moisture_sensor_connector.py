from pydispatch import dispatcher
from signal_registry.events import RequestMoistureMeasurementEvent


from signal_registry.signal_registry import SignalRegistry
from moisture_sensor.moisture_sensor_manager import MoistureSensorManager


class MoistureSensorConnector:
    def __init__(
        self,
        moisture_sensor: MoistureSensorManager,
    ) -> None:
        self.moisture_sensor = moisture_sensor
        dispatcher.connect(
            self.measure_moisture,
            signal=SignalRegistry.REQUEST_MOISTURE_MEASUREMENTS.signal,
        )

    def measure_moisture(self, event: RequestMoistureMeasurementEvent):
        results = self.moisture_sensor.check_sensors(event.sensors)
        dispatcher.send(
            signal=SignalRegistry.MOISTURE_MEASUREMENT_RESULTS.signal,
            sender=self,
            event=SignalRegistry.MOISTURE_MEASUREMENT_RESULTS.event(results),
        )
