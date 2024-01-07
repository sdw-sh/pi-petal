import logging
import time
from external_scripts.PCF8574 import PCF8574_GPIO
from external_scripts.Adafruit_LCD1602 import Adafruit_CharLCD

from dotenv import load_dotenv

from moisture_sensor.moisture_sensor_manager import MoistureSensorManager
from logging_definition import log_setup
from moisture_sensor.sleep_until_next_n_minutes_multiple import (
    sleep_until_next_n_minutes_multiple,
)

load_dotenv()

log_setup("sensors.log")
logger = logging.getLogger(__name__)


logging.info(">>>>>   Starting sensor only testing   <<<<<")


def initialize_display():
    PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
    PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
    try:
        mcp = PCF8574_GPIO(PCF8574_address)
    except:
        try:
            mcp = PCF8574_GPIO(PCF8574A_address)
        except:
            print("I2C Address Error !")
            exit(1)
    # Create LCD, passing in MCP GPIO adapter.
    lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4, 5, 6, 7], GPIO=mcp)
    mcp.output(3, 1)  # turn on LCD backlight
    lcd.begin(16, 2)  # set number of LCD lines and columns

    def update_display(line1="Well hello!", line2="Splendid!"):
        lcd.setCursor(0, 0)
        lcd.message(line1 + "\n")
        lcd.message(line2)

    return update_display


if __name__ == "__main__":
    try:
        update_display = initialize_display()
        sensor_manager = MoistureSensorManager.create_asd7830_based_controller()
        i = 30
        while i > 0:
            i = i - 1
            measured_values = []
            for channel in range(0, 5):
                value = sensor_manager.check_single_sensor(
                    channel,
                    warnings=False,
                    logging=False,
                )
                measured_values.append(f"{value:>4}")
            info_message = " | ".join(measured_values)
            logger.info(info_message)
            update_display(
                f"{measured_values[0]}|{measured_values[1]}",
                f"{measured_values[2]}|{measured_values[3]}|{measured_values[4]}",
            )
            sleep_until_next_n_minutes_multiple(1)
        while True:
            measured_values = []
            for channel in range(0, 5):
                value = sensor_manager.check_single_sensor(
                    channel,
                    warnings=False,
                    logging=False,
                )
                measured_values.append(f"{value:>4}")
            logger.info(" | ".join(measured_values))
            sleep_until_next_n_minutes_multiple(5)

    except KeyboardInterrupt:
        # TODO release ressources upon any kind of shutdown
        logger.info("\nDid it work as expected?\n")
