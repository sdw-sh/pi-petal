import logging
import time
import RPi.GPIO as GPIO


from logging_definition import log_setup
from board_setup import initialize_board
from button_manager import ButtonManager
from control_state import ControlState

log_setup(f"valve_and_pump.log")
logger = logging.getLogger(__name__)


logging.info(">>>>>   Starting controls testing   <<<<<")

if __name__ == "__main__":
    initialize_board()
    control_state = ControlState()
    ButtonManager(
        [
            {
                "pin": 12,  # 12,16,18
                "callback": control_state.change_active_selection,
            },
            {
                "pin": 16,  # 12,16,18
                "callback": control_state.button_1,
            },
            {
                "pin": 18,  # 12,16,18
                "callback": control_state.button_2,
            },
        ]
    )
    while True:
        time.sleep(60)
