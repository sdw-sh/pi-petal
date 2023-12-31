import logging
import time
import RPi.GPIO as GPIO


from logging_definition import log_setup
from board_setup import initialize_board
from button_manager import ButtonManager

log_setup(f"button.log")
logger = logging.getLogger(__name__)


logging.info(">>>>>   Starting button testing   <<<<<")

if __name__ == "__main__":
    initialize_board()
    ButtonManager()
    while True:
        time.sleep(60)
        logger.debug("A minute has passed")
