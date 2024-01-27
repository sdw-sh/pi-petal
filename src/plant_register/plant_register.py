import logging

from typing import List

from utilities.functions import find
from plant_register.plant import Plant
from moisture_sensor.moisture_measurement_result import MoistureMeasurementResult

logger = logging.getLogger(__name__)


plants = [
    Plant("Palme", 0, watering_threshold=60, water_plant=False),
    Plant("Kaktus", 1, watering_threshold=30),
    Plant(
        "Gummibaum",
        2,
        plant_id="Test Plant 1",
        water_plant=False,
    ),
    Plant(
        "Wasserpflanze",
        3,
        valve=5,
        plant_id="Test Plant 2",
        water_plant=False,
    ),
    Plant(
        "Geldbaum",
        4,
        valve=5,
        plant_id="Test Plant 3",
    ),
]


class PlantRegister:
    def __init__(self, plants=plants) -> None:
        self.plants: List[Plant] = plants

    def get_sensors(self) -> List[int]:
        sensors = []
        for plant in self.plants:
            sensors.append(plant.sensor)
        return sensors

    def update_moisture_values(
        self,
        measurement_results: List[MoistureMeasurementResult],
    ):
        for result in measurement_results:
            self.update_moisture_value(result)

    def update_moisture_value(self, result: MoistureMeasurementResult):
        plant: Plant = find(
            self.plants,
            lambda plant: plant.sensor == result.sensor,
        )
        if plant is not None:
            plant.moisture_level = result.moisture_measurement
            plant.last_moisture_measurement = result.datetime
        else:
            logging.warn(
                f"No plant found for sensor #{result.sensor} in PlantRegister."
            )

    def get_short_moisture_value_strings(self):
        string = ""
        for plant in self.plants:
            string += f"{plant.sensor}:{plant.moisture_level}|"
        return string

    def request_irrigation(self):
        pass
