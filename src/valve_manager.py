import RPi.GPIO as GPIO
import logging
import sys
import threading
import time

logger = logging.getLogger(__name__)

# TODO add state of the app service to get locking everywhere
# should also include the shutdown


class ValveManager:
    def __init__(
        self,
        valve_0_pin: int,
        valve_1_pin: int,
        # valve_2_pin: int,
        # valve_3_pin: int,
    ):
        self.valve_0_pin = valve_0_pin
        self.valve_1_pin = valve_1_pin
        # self.valve_2_pin = valve_2_pin
        # self.valve_3_pin = valve_3_pin
        if GPIO.getmode() != GPIO.BOARD:
            logger.critical("GPIO board mode not set, board not initiated, terminating")
            sys.exit(-1)
        GPIO.setup(self.valve_0_pin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.valve_1_pin, GPIO.OUT, initial=GPIO.LOW)
        logger.info(
            f"Instantiated  ValveManager (pins {self.valve_0_pin}, {self.valve_1_pin})"
        )

    def open(self):
        GPIO.output(self.valve_0_pin, GPIO.HIGH)

    def close(self):
        GPIO.output(self.valve_0_pin, GPIO.LOW)

    def open1(self):
        GPIO.output(self.valve_1_pin, GPIO.HIGH)

    def close1(self):
        GPIO.output(self.valve_1_pin, GPIO.LOW)
