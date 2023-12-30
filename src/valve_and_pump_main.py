import logging
import time
import RPi.GPIO as GPIO


from logging_definition import log_setup
from pump.pump_manager import PumpManager
from valve_manager import ValveManager

log_setup(f"valve_and_pump.log")
logger = logging.getLogger(__name__)


logging.info(">>>>>   Starting valve and pump testing   <<<<<")

if __name__ == "__main__":
    GPIO.setmode(GPIO.BOARD)
    pump = PumpManager(33)
    valves = ValveManager(35, 37)
    valves.open()
    pump.pump(3)
    valves.close()
    time.sleep(1)
    valves.open1()
    pump.pump(3)
    valves.close1()
