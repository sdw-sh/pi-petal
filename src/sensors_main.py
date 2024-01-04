import logging
import time

from dotenv import load_dotenv

from moisture_sensor.moisture_sensor_manager import MoistureSensorManager
from logging_definition import log_setup
from moisture_sensor.sleep_until_next_n_minutes_multiple import (
    sleep_until_next_n_minutes_multiple,
)

load_dotenv()

log_setup("sensors.log")
logger = logging.getLogger(__name__)


logging.info(">>>>>   Starting sensor only testing   <<<<<")

if __name__ == "__main__":
    try:
        sensor_manager = MoistureSensorManager.create_asd7830_based_controller()
        i = 30
        while i > 0:
            i = i - 1
            measured_values = []
            for channel in range(0, 5):
                value = sensor_manager.check_moisture(
                    channel,
                    warnings=False,
                    logging=False,
                )
                measured_values.append(f"{value:>4}")
            logger.info(" | ".join(measured_values))
            sleep_until_next_n_minutes_multiple(1)
        while True:
            measured_values = []
            for channel in range(0, 5):
                value = sensor_manager.check_moisture(
                    channel,
                    warnings=False,
                    logging=False,
                )
                measured_values.append(f"{value:>4}")
            logger.info(" | ".join(measured_values))
            sleep_until_next_n_minutes_multiple(5)

    except KeyboardInterrupt:
        # TODO release ressources upon any kind of shutdown
        logger.info("\nDid it work as expected?\n")
