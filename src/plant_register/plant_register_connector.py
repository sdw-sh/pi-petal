from pydispatch import dispatcher

from event_signal import EventSignal
from plant_register.plant_register import PlantRegister


class PlantRegisterConnector:
    def __init__(self, plant_register: PlantRegister) -> None:
        self.plant_register = plant_register
        dispatcher.connect(
            self.request_moisture_measurements,
            EventSignal.CHECK_PLANTS,
        )
        dispatcher.connect(
            self.update_moisture_values,
            EventSignal.MOISTURE_MEASUREMENT_RESULTS,
        )

    def request_moisture_measurements(self):
        sensors = self.plant_register.get_sensors()
        dispatcher.send(
            signal=EventSignal.REQUEST_MOISTURE_MEASUREMENTS,
            sender=self,
            event=sensors,
        )

    def update_moisture_values(self, event):
        self.plant_register.update_moisture_values(event)
        message = self.plant_register.get_short_moisture_value_strings()
        dispatcher.send(
            signal=EventSignal.UPDATE_DISPLAY,
            sender=self,
            event=(message, ""),
        )


def create_plant_register_connector():
    register = PlantRegister()
    connector = PlantRegisterConnector(register)
    return connector
