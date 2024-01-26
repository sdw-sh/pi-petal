from pydispatch import dispatcher

from signal_registry.signal_registry import SignalRegistry
from plant_register.plant_register import PlantRegister


class PlantRegisterConnector:
    def __init__(self, plant_register: PlantRegister) -> None:
        self.plant_register = plant_register
        dispatcher.connect(
            self.request_moisture_measurements,
            SignalRegistry.CHECK_PLANTS.signal,
        )
        dispatcher.connect(
            self.update_moisture_values,
            SignalRegistry.MOISTURE_MEASUREMENT_RESULTS.signal,
        )

    def request_moisture_measurements(self):
        sensors = self.plant_register.get_sensors()
        dispatcher.send(
            signal=SignalRegistry.REQUEST_MOISTURE_MEASUREMENTS.signal,
            sender=self,
            event=sensors,
        )

    def update_moisture_values(self, event):
        self.plant_register.update_moisture_values(event)
        message = self.plant_register.get_short_moisture_value_strings()
        dispatcher.send(
            signal=SignalRegistry.UPDATE_DISPLAY.signal,
            sender=self,
            event=SignalRegistry.UPDATE_DISPLAY.event(message, ""),
        )


def create_plant_register_connector():
    register = PlantRegister()
    connector = PlantRegisterConnector(register)
    return connector
