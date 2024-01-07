from typing import List
from plant_register.plant import Plant
from moisture_sensor.moisture_measurement_result import MoistureMeasurementResult

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
        valve_number=5,
        plant_id="Test Plant 2",
        water_plant=False,
    ),
    Plant(
        "Geldbaum",
        4,
        valve_number=5,
        plant_id="Test Plant 3",
    ),
]


def find(list, condition):
    for element in list:
        if condition(element):
            return element
    return None


class PlantRegister:
    def __init__(self, plants=plants) -> None:
        self.plants = plants

    def request_moisture_measurements(self):
        pass

    def update_moisture_values(
        self, measurement_results: List[MoistureMeasurementResult]
    ):
        for result in measurement_results:
            plant: Plant = find(
                self.plants,
                lambda plant: plant.sensor_number == result.sensor,
            )
            if plant is not None:
                plant.moisture_level = result.moisture_measurement
                plant.last_moisture_measurement = result.datetime

    def request_irrigation(self):
        pass
