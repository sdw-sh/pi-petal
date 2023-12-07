import RPi.GPIO as GPIO
import logging
import sys
import threading
import time

logger = logging.getLogger(__name__)

class PumpManager:
    
    critical_time_span_in_s = 4

    def __init__(self, pump_pin: int):
        self.pump_pin = pump_pin
        self.is_locked = False
        # @see https://raspi.tv/2015/rpi-gpio-function-gpio-getmodev2
        if (GPIO.getmode() != GPIO.BOARD):
            logger.critical("GPIO board mode not set, board not initiated, terminating");
            sys.exit(-1)
        GPIO.setup(self.pump_pin, GPIO.OUT, initial = GPIO.LOW)
        logger.info(f"Instantiated  PumpManager (pin {self.pump_pin})")
        
        # set up pin
    
    def on(self, seconds : float = 0, force : bool = False):
        if (self.is_locked):
            logger.warning(f"PumpManager.on called on locked pump (pin {self.pump_pin})")
            self.off()
            return
        if (seconds > PumpManager.critical_time_span_in_s and force == False):
            logger.warning(f"To start the pump (pin {self.pump_pin}) with a longer runtime than {PumpManager.critical_time_span_in_s} set the force param to true")
            return;
        logger.info(f"Starting pump (pin {self.pump_pin}) for {seconds} s")
        GPIO.output(self.pump_pin, GPIO.HIGH)
        time.sleep(seconds)
        self.off()

    def off(self):
        GPIO.output(self.pump_pin, GPIO.LOW)
        logger.info(f"Pump (pin {self.pump_pin}) stopped")

    def lock(self):
        self.is_locked = True
        self.off()
        logger.warning(f"Pump (pin {self.pump_pin}) is locked")

    def destroy(self):
        logger.critical(f"PumpManager.destroy() called (pin {self.pump_pin})")
        GPIO.cleanup()
        sys.exit(-1)