import logging

logger = logging.getLogger(__name__)


class Plant:
    def __init__(
        self,
        plant_name,
        sensor,
        valve=None,
        watering_threshold=50,
        plant_id=None,
        water_plant=True,
    ):
        self.plant_name = plant_name
        self.sensor = sensor
        self.valve = valve if valve else sensor
        self.plant_id = plant_id if plant_id else plant_name
        # TODO rename all watering to irrigation
        self.irrigation_threshold = watering_threshold
        self.irrigate_plant = water_plant
        self.moisture_level = None
        self.last_moisture_measurement = None
        self.last_irrigation_event = None
        logger.info(f"Instantiated class {self}.")

    @property
    def irrigation_threshold(self):
        return self._irrigation_threshold

    @irrigation_threshold.setter
    def irrigation_threshold(self, new_value):
        if new_value < 0 or new_value > 100:
            logger.warn(f"Invalid watering_threshold value {new_value} set for {self}.")
        self._irrigation_threshold = new_value

    def change_irrigation_threshold(self, change):
        new_value = self.irrigation_threshold + change
        if new_value > 100 or new_value < 0:
            return
        self.irrigation_threshold = new_value

    def get_plant_string(self):
        return f"Plant(plant_name={self.plant_name}, plant_id={self.plant_id}, watering_threshold={self._irrigation_threshold})"

    def __str__(self):
        return self.get_plant_string()
