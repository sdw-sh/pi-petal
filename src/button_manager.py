import RPi.GPIO as GPIO
import logging
import sys

logger = logging.getLogger(__name__)


class ButtonManager:
    def __init__(
        self,
        buttons=[
            {
                "pin": 12,  # 12,16,18
                "callback": lambda _: logger.info("pin 12"),
            },
            {
                "pin": 16,  # 12,16,18
                "callback": lambda _: logger.info("pin 16"),
            },
            {
                "pin": 18,  # 12,16,18
                "callback": lambda _: logger.info("pin 18"),
            },
        ],
    ) -> None:
        if GPIO.getmode() != GPIO.BOARD:
            logger.critical("GPIO board mode not set, board not initiated, terminating")
            sys.exit(-1)
        for button_definition in buttons:
            GPIO.setup(
                button_definition["pin"],
                GPIO.IN,
                pull_up_down=GPIO.PUD_UP,
            )
        for button_definition in buttons:
            GPIO.add_event_detect(
                button_definition["pin"],
                GPIO.FALLING,
                callback=button_definition["callback"],
                bouncetime=200,
            )
