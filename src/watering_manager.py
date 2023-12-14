import time
import logging

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
        self.number_of_sensors = 5

        logging.info("WateringManager instantiated")

    # this allows nothing but the WateringManager running
    # might be a good idea to move one level up
    # for now it is fine
    def main_loop(self):
        while True:
            self.check()
            sleep_until_next_n_minutes_multiple(10)

    def check(self):
        soil_moisture_measurements = []
        for sensor in range(self.number_of_sensors):
            soil_moisture = self.moisture_sensor.check_humidity(sensor)
            soil_moisture_measurements.append(soil_moisture)
        if soil_moisture_measurements[0] < self.watering_threshold:
            self.water(soil_moisture_measurements[0])

    def _log_moisture_measurements(self, soil_moisture_measurements):
        log_message = "Moisture: "
        for index, value in enumerate(soil_moisture_measurements):
            divider = "" if index == 0 else "|"
            log_message = f"{log_message} {divider} {index}: {value}"
        logger.info(log_message)
    
    def water(self, initial_soil_moisture):
        logger.info(
            f"Plant moisture of {initial_soil_moisture} is below {self.watering_threshold}, watering now."
        )
        if self.pump.is_locked:
            logger.warning("Tried to water but the pump is locked!")
            return
        self.pump.on(seconds=3)
        # wait for a short while to let the water settle
        time.sleep(15)
        # check if some water reached the sensor
        watered_soil_moisture = self.moisture_sensor.check_humidity(0)
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
