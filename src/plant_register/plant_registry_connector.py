from pydispatch import dispatcher

from signal_registry.signal_registry import SignalRegistry
from plant_register.plant_registry import PlantRegistry
from signal_registry.events import (
    MoistureMeasurementResultEvent,
)


class PlantRegistryConnector:
    def __init__(self, plant_register: PlantRegistry) -> None:
        self.plant_register = plant_register
        dispatcher.connect(
            self.request_moisture_measurements,
            SignalRegistry.CHECK_PLANTS.signal,
        )
        dispatcher.connect(
            self.update_moisture_value,
            SignalRegistry.MOISTURE_MEASUREMENT_RESULT.signal,
        )

    def request_moisture_measurements(self):
        sensors = self.plant_register.get_sensors()
        dispatcher.send(
            signal=SignalRegistry.REQUEST_MOISTURE_MEASUREMENTS.signal,
            sender=self,
            event=SignalRegistry.REQUEST_MOISTURE_MEASUREMENTS.event(sensors),
        )

    def update_moisture_value(self, event: MoistureMeasurementResultEvent):
        plant = self.plant_register.update_moisture_value(event.result)
        if plant:
            dispatcher.send(
                signal=SignalRegistry.IRRIGATE.signal,
                sender=self,
                event=SignalRegistry.IRRIGATE.event(
                    plant.valve, plant.irrigation_duration_in_s
                ),
            )

        message = self.plant_register.get_short_moisture_value_strings()
        dispatcher.send(
            signal=SignalRegistry.UPDATE_DISPLAY.signal,
            sender=self,
            event=SignalRegistry.UPDATE_DISPLAY.event(message, ""),
        )


def create_plant_registry_connector():
    register = PlantRegistry()
    connector = PlantRegistryConnector(register)
    return connector
