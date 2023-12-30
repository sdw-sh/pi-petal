import RPi.GPIO as GPIO
import logging
import sys
import threading
import time

logger = logging.getLogger(__name__)

# TODO add state of the app service to get locking everywhere
# should also include the shutdown

# This is basically just LOW and HIGH switcher, ponder adding an abstraction level, 
# where the names of the LOW and HIGH methods may be given freely

class ValveManager:
    def __init__(
        self,
        valve_dict,
    ):
        self.valve_dict = valve_dict
        if GPIO.getmode() != GPIO.BOARD:
            logger.critical("GPIO board mode not set, board not initiated, terminating")
            sys.exit(-1)
        for key, value in valve_dict.items():
            GPIO.setup(value, GPIO.OUT, initial=GPIO.LOW)
        logger.info(f"Instantiated  ValveManager (valve_dict {valve_dict})")

    def open(self, valve_key):
        GPIO.output(self.valve_dict[valve_key], GPIO.HIGH)

    def close(self, valve_key):
        GPIO.output(self.valve_dict[valve_key], GPIO.LOW)
