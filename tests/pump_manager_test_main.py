import time
import logging
import RPi.GPIO as GPIO

from pump_manager import PumpManager

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='pump.log',
    filemode='w',
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt = "%Y-%m-%d %H:%M:%S"
)

if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    pumpManager = PumpManager(pump_pin = 12)
    try:
        pumpManager.on(seconds = 1)
        time.sleep(1)
        pumpManager.on(seconds = 3)
        time.sleep(1)
        pumpManager.on(seconds = 7)
        time.sleep(1)
        pumpManager.on(seconds = 7, force = True)
        time.sleep(1)
        pumpManager.lock()
        pumpManager.on(2)
        time.sleep(1)
        pumpManager.destroy()
    except KeyboardInterrupt:
        pumpManager.destroy()