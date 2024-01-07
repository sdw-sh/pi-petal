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

    def request_moisture_measurements(self):
        sensors = self.plant_register.get_sensors()
        dispatcher.send(
            signal=EventSignal.REQUEST_MOISTURE_MEASUREMENTS,
            sender=self,
            event=sensors,
        )


def create_plant_register_connector():
    register = PlantRegister()
    connector = PlantRegisterConnector(register)
    return connector
