import RPi.GPIO as GPIO
import logging
import sys

from typing import List

from utilities.functions import index_exists

logger = logging.getLogger(__name__)


# This is basically a LOW and HIGH switcher
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
        logger.info(f"Instantiated ValveManager (valve pins: {valves})")

    def open(self, valve_index):
        GPIO.output(self.valves[valve_index], GPIO.HIGH)

    def close(self, valve_index):
        logger.warn(f"Non existent index {valve_index} requested in ValveManager.")
        logger.warn(f"Existing indices are {self.valves}")
        if not index_exists(self.valves, valve_index):
            return
        GPIO.output(self.valves[valve_index], GPIO.LOW)
