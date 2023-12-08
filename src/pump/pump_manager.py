import RPi.GPIO as GPIO
import logging
import sys
import threading
import time

logger = logging.getLogger(__name__)


class PumpManager:
    critical_time_span_in_s = 4

    def __init__(self, pump_pin: int, on_on_callback=None, on_off_callback=None):
        self.pump_pin = pump_pin
        self.is_locked = False
        self.on_on_callback = on_on_callback
        self.on_off_callback = on_off_callback
        if GPIO.getmode() != GPIO.BOARD:
            logger.critical("GPIO board mode not set, board not initiated, terminating")
            sys.exit(-1)
        GPIO.setup(self.pump_pin, GPIO.OUT, initial=GPIO.LOW)
        logger.info(f"Instantiated  PumpManager (pin {self.pump_pin})")

    def on(self, seconds: float = 0, force: bool = False):
        if self.is_locked:
            logger.warning(
                f"PumpManager.on called on locked pump (pin {self.pump_pin})"
            )
            self.off()
            return
        if seconds > PumpManager.critical_time_span_in_s and force == False:
            logger.warning(
                f"To start the pump (pin {self.pump_pin}) with a longer runtime than {PumpManager.critical_time_span_in_s} set the force param to true"
            )
            return
        logger.info(f"Starting pump (pin {self.pump_pin}) for {seconds} s")
        if callable(self.on_on_callback):
            self.on_on_callback()
        GPIO.output(self.pump_pin, GPIO.HIGH)
        time.sleep(seconds)
        self.off()

    def off(self):
        GPIO.output(self.pump_pin, GPIO.LOW)
        if callable(self.on_off_callback):
            self.on_off_callback()
        logger.info(f"Stopped pump (pin {self.pump_pin})")

    def lock(self):
        self.is_locked = True
        logger.warning(f"LOCKED pump (pin {self.pump_pin})")
        self.off()

    def destroy(self):
        logger.critical(f"PumpManager.destroy() called (pin {self.pump_pin})")
        GPIO.cleanup()
        sys.exit(-1)
