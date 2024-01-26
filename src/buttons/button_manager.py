import RPi.GPIO as GPIO
import logging
import sys
import threading

logger = logging.getLogger(__name__)


class ButtonManager:
    def __init__(self, buttons) -> None:
        if GPIO.getmode() != GPIO.BOARD:
            logger.critical("GPIO board mode not set, board not initiated, terminating")
            sys.exit(-1)
        for button_definition in buttons:
            GPIO.setup(
                button_definition["pin"],
                GPIO.IN,
                pull_up_down=GPIO.PUD_UP,
            )
            GPIO.add_event_detect(
                button_definition["pin"],
                GPIO.FALLING,
                callback=lambda *_, bd=button_definition: threading.Thread(
                    target=bd["callback"],
                ).start(),
                bouncetime=200,
            )


# button_definition["callback"],
