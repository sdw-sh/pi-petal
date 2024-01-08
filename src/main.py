import logging
import sys
import RPi.GPIO as GPIO

# TODO define aliasses

from watering_manager import WateringManager
from board_setup import initialize_board

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
    try:
        initialize_board()
        manager = WateringManager()
        manager.main_loop()
    except KeyboardInterrupt:
        # TODO release ressources upon any kind of shutdown
        GPIO.cleanup()
        logger.info("Have a nice day.")


#       (\__  |
#      :=)__)-|  __/)
#       (/    |-(__(=:
#             |   \)
