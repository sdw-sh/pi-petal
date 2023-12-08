import time
import sys
import logging
from moisture_sensor_manager import MoistureSensorManager
from sleep_until_next_n_minutes_multiple import sleep_until_next_n_minutes_multiple

logger = logging.getLogger(__name__)
logging.basicConfig(
    handlers=[
        logging.FileHandler("moisture.log", mode="w", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


logging.info("Log started")

################################################################################################################


def moisture_sensor_demo(sensor):
    while True:
        sensor.check_humidity(0)
        sleep_until_next_n_minutes_multiple(2)


if __name__ == "__main__":
    print("Starting")
    try:
        sensor = MoistureSensorManager.create_asd7830_based_controller()
        moisture_sensor_demo(sensor)
    except KeyboardInterrupt:
        sensor.destroy()
