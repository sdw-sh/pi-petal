import time
import logging
import argparse


from plant import Plant
from moisture_sensor.moisture_sensor_manager import MoistureSensorManager
from pump.pump_manager import PumpManager
from moisture_sensor.sleep_until_next_n_minutes_multiple import (
    sleep_until_next_n_minutes_multiple,
)

logger = logging.getLogger(__name__)


class WateringManager:
    def __init__(self):
        self.min_moisture_increase_on_watering = 3
        self.watering_threshold = 40
        self.moisture_sensor = MoistureSensorManager.create_asd7830_based_controller()
        self.pump = PumpManager(pump_pin=12)
        # Todo add plant collection that cheks for ids
        self.plants = [
            Plant("Palm Tree", 0),
            Plant("Test Plant", 1, water_plant=False),
            Plant(
                "Test Plant",
                2,
                valve_number=5,
                plant_id="Test Plant 2",
                water_plant=False,
                watering_threshold=150,
            ),
        ]

        logging.info("WateringManager instantiated")

    # this allows nothing but the WateringManager running
    # might be a good idea to move one level up
    # for now it is fine
    def main_loop(self):
        while True:
            self.check(self.plants[0])
            sleep_until_next_n_minutes_multiple(10)

    def check(self, plant: Plant) -> None:
        soil_moisture_measurements = []
        soil_moisture = self.moisture_sensor.check_moisture(plant.sensor_number)
        if soil_moisture < self.watering_threshold and plant.water_plant:
            self.water(plant, soil_moisture)

    def _log_moisture_measurements(self, soil_moisture_measurements):
        log_message = "Moisture: "
        for index, value in enumerate(soil_moisture_measurements):
            divider = "" if index == 0 else "|"
            log_message = f"{log_message} {divider} {index}: {value}"
        logger.info(log_message)

    def water(self, plant: Plant, initial_soil_moisture: int) -> None:
        logger.info(
            f"Plant moisture of {initial_soil_moisture} is below threshold for {plant}, watering now."
        )
        if self.pump.is_locked:
            logger.warning("Tried to water but the pump is locked!")
            return
        if plant.water_plant == False:
            logger.warning(f"Tried to water {Plant} which is set to non watering!")
            return
        self.pump.on(seconds=3)
        # wait for a short while to let the water settle
        time.sleep(15)
        # check if some water reached the sensor
        watered_soil_moisture = self.moisture_sensor.check_moisture(0)
        if (
            watered_soil_moisture - initial_soil_moisture
            < self.min_moisture_increase_on_watering
        ):
            # if no water reached the sensor we have problem
            # pump running dry, or a loose hose
            # better stop all future watering until we checked
            logger.error(
                "Moisture level did not increase after watering. Check pump, hose etc.!"
            )
            self.panic()

    def panic(self):
        logger.error("WateringManager panicked!")
        self.pump.lock()
