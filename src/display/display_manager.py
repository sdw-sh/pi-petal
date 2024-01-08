import logging

from external_scripts.PCF8574 import PCF8574_GPIO
from external_scripts.Adafruit_LCD1602 import Adafruit_CharLCD


logger = logging.getLogger(__name__)


class DisplayManager:
    def __init__(self) -> None:
        PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
        PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
        self.mcp = None
        try:
            self.mcp = PCF8574_GPIO(PCF8574_address)
        except:
            try:
                self.mcp = PCF8574_GPIO(PCF8574A_address)
            except:
                logger.critical("I2C Address Error !")
                exit(1)
        # Create LCD, passing in MCP GPIO adapter.
        self.lcd = Adafruit_CharLCD(
            pin_rs=0,
            pin_e=2,
            pins_db=[4, 5, 6, 7],
            GPIO=self.mcp,
        )
        self.mcp.output(3, 1)  # turn on LCD backlight
        self.lcd.begin(16, 2)  # set number of LCD lines and columns
        self.update(
            line1="Display working.",
            line2="Splendid!",
        )

    def update(
        self,
        line1="",
        line2="",
    ):
        self.lcd.setCursor(0, 0)
        self.lcd.message(line1 + "\n")
        self.lcd.message(line2)
