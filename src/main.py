import logging
import sys
import RPi.GPIO as GPIO

# TODO define aliasses

from watering_manager import WateringManager

logger = logging.getLogger(__name__)
logging.basicConfig(
    handlers=[
        logging.FileHandler("moisture.log", mode="a", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ],
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)-8s - %(message)-50s [%(name)s.%(funcName)s:%(lineno)d]",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logging.info("🏵️ 🏵️ 🏵️   Welcome to PiPetal   🏵️ 🏵️ 🏵️")

if __name__ == "__main__":
    print("Starting")
    try:
        GPIO.setmode(GPIO.BOARD)
        manager = WateringManager()
        manager.main_loop()
    except KeyboardInterrupt:
        # TODO release ressources upon any kind of shutdown
        logger.info("Have a nice day.")


#       (\__  |
#      :=)__)-|  __/)
#       (/    |-(__(=:
#             |   \)
