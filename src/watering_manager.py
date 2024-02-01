import time
import logging
import RPi.GPIO as GPIO

from buttons.button_manager import ButtonManager
from plant_register.plant import Plant
from moisture_sensor.moisture_sensor_manager import MoistureSensorManager
from irrigation.pump_manager import PumpManager
from moisture_sensor.sleep_until_next_n_minutes_multiple import (
    sleep_until_next_n_minutes_multiple,
)
from irrigation.valve_manager import ValveManager


logger = logging.getLogger(__name__)


# TODO this class combines valves and pump
# this should be done by a watering process class or something similar
class WateringManager:
    def __init__(
        self,
        panic_led_pin=40,  # GPIO21
        system_running_led_pin=38,  # GPIO20
    ):
        self.min_moisture_increase_on_watering = 3
        self.panic_led_pin = panic_led_pin
        self.system_running_led_pin = system_running_led_pin
        self.moisture_sensor = MoistureSensorManager.create_asd7830_based_controller()
        self.pump = PumpManager(pump_pin=33)
        self.valves = ValveManager({0: 35, 1: 37})
        # Todo add plant collection that checks for ids
        self.plants = [
            Plant("Palm Tree", 0, watering_threshold=100, water_plant=False),
            Plant("Test Plant", 1, watering_threshold=100),
            Plant(
                "Test Plant",
                2,
                plant_id="Test Plant 1",
                water_plant=False,
            ),
            Plant(
                "Test Plant",
                3,
                valve=5,
                plant_id="Test Plant 2",
                water_plant=False,
            ),
            Plant(
                "Test Plant",
                4,
                valve=5,
                plant_id="Test Plant 3",
            ),
        ]

        self.button_manager = None

        GPIO.setup(self.panic_led_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.system_running_led_pin, GPIO.OUT, initial=GPIO.HIGH)
        logging.info("WateringManager instantiated")

    # this allows nothing but the WateringManager running
    # TODO might be a good idea to move one level up
    # for now it is fine
    def main_loop(self):
        while True:
            for plant in self.plants:
                self.check(plant)
            sleep_until_next_n_minutes_multiple(10)

    def check(self, plant: Plant) -> None:
        soil_moisture = self.moisture_sensor.check_single_sensor(plant.sensor)
        if soil_moisture < plant.irrigation_threshold and plant.irrigate_plant:
            logger.info(
                f"Plant moisture of {soil_moisture} is below threshold for {plant}, watering now."
            )
            self.water_and_check(plant, soil_moisture)

    def _log_moisture_measurements(self, soil_moisture_measurements):
        log_message = "Moisture: "
        for index, value in enumerate(soil_moisture_measurements):
            divider = "" if index == 0 else "|"
            log_message = f"{log_message} {divider} {index}: {value}"
        logger.info(log_message)

    def water_and_check(self, plant: Plant, initial_soil_moisture: int) -> None:
        if self.pump.is_locked:
            logger.warning("Tried to water but the pump is locked!")
            return
        if plant.irrigate_plant == False:
            logger.warning(f"Tried to water {Plant} which is set to non watering!")
            return
        self.water(plant.valve, time_in_s=3)
        # wait for a short while to let the water settle
        time.sleep(15)
        # check if some water reached the sensor
        watered_soil_moisture = self.moisture_sensor.check_single_sensor(0)
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

    # TODO this belongs in a separate class
    def water(self, valve, time_in_s):
        self.valves.open(valve)
        self.pump.pump(time_in_s)
        self.valves.close(valve)

    def panic(self):
        # makeshift warning LED
        GPIO.output(40, GPIO.HIGH)
        logger.error("WateringManager panicked!")
        self.pump.lock()
