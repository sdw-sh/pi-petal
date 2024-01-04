import RPi.GPIO as GPIO
import logging
import sys

from typing import List

logger = logging.getLogger(__name__)

# TODO add state of the app service to get locking everywhere
# should also include the shutdown

# This is basically just LOW and HIGH switcher, ponder adding an abstraction level,
# where the names of the LOW and HIGH methods may be given freely


class ValveManager:
    def __init__(
        self,
        valves: List[int],
    ):
        self.valves = valves
        if GPIO.getmode() != GPIO.BOARD:
            logger.critical("GPIO board mode not set, board not initiated, terminating")
            sys.exit(-1)
        for value in valves:
            GPIO.setup(value, GPIO.OUT, initial=GPIO.LOW)
        logger.info(f"Instantiated  ValveManager (List: {valves})")

    def open(self, valve_index):
        GPIO.output(self.valves[valve_index], GPIO.HIGH)

    def close(self, valve_index):
        GPIO.output(self.valves[valve_index], GPIO.LOW)
