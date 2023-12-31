import logging

logger = logging.getLogger(__name__)


class Plant:
    def __init__(
        self,
        plant_name,
        sensor_number,
        valve_number=None,
        watering_threshold=50,
        plant_id=None,
        water_plant=True,
    ):
        self.plant_name = plant_name
        self.sensor_number = sensor_number
        self.valve_number = valve_number if valve_number else sensor_number
        self.plant_id = plant_id if plant_id else plant_name
        self.watering_threshold = watering_threshold
        self.water_plant = water_plant
        logger.info(f"Instantiated class {self}.")

    @property
    def watering_threshold(self):
        return self._watering_threshold

    @watering_threshold.setter
    def watering_threshold(self, new_value):
        if new_value < 0 or new_value > 100:
            logger.warn(f"Invalid watering_threshold value {new_value} set for {self}.")
        self._watering_threshold = new_value

    def change_watering_threshold(self, change):
        new_value = self.watering_threshold + change
        if new_value > 100 or new_value < 0:
            return
        self.watering_threshold = new_value

    def __str__(self):
        return f"Plant(plant_name={self.plant_name}, plant_id={self.plant_id}, watering_threshold={self._watering_threshold})"
