import time
import logging
import RPi.GPIO as GPIO


from plant import Plant
from moisture_sensor.moisture_sensor_manager import MoistureSensorManager
from pump.pump_manager import PumpManager
from moisture_sensor.sleep_until_next_n_minutes_multiple import (
    sleep_until_next_n_minutes_multiple,
)
from valve_manager import ValveManager


logger = logging.getLogger(__name__)


class WateringManager:
    def __init__(self):
        self.min_moisture_increase_on_watering = 3
        self.moisture_sensor = MoistureSensorManager.create_asd7830_based_controller()
        self.pump = PumpManager(pump_pin=33)
        self.valves = ValveManager({0: 35, 1: 37})
        # Todo add plant collection that checks for ids
        self.plants = [
            Plant("Palm Tree", 0, watering_threshold=100),
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
                valve_number=5,
                plant_id="Test Plant 2",
                water_plant=False,
            ),
            Plant(
                "Test Plant",
                4,
                valve_number=5,
                plant_id="Test Plant 3",
            ),
        ]
        # the panic LED
        GPIO.setup(40, GPIO.OUT, initial=GPIO.LOW)
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
        soil_moisture = self.moisture_sensor.check_moisture(plant.sensor_number)
        print(111)
        print(soil_moisture)
        print(plant.watering_threshold)
        print(soil_moisture < plant.watering_threshold)
        if soil_moisture < plant.watering_threshold and plant.water_plant:
            print(222)
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
        self.valves.open(plant.valve_number)
        self.pump.pump(seconds=3)
        self.valves.close(plant.valve_number)
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
        # makeshift warning LED
        GPIO.output(40, GPIO.HIGH)
        logger.error("WateringManager panicked!")
        self.pump.lock()
