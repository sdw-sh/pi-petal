from ADCDevice import *
import sys
from collections import namedtuple
import logging

logger = logging.getLogger(__name__)


# for 8 bit ADC
# currently maps the channel index to tthe channel on the board, not ideal but acceptable
class MoistureSensorManager:
    def __init__(self, adc):
        self.adc = adc
        logger.info("HumiditySensorManager instantiated")

    @staticmethod
    def create_asd7830_based_controller():
        adc_device = ADCDevice()
        if adc_device.detectI2C(0x4B):
            adc = ADS7830()
            print("ADC found")
            return MoistureSensorManager(adc)
        else:
            logger.critical("ADC not found, critical error, terminating")
            # TODO throw an error to allow for clean up of other ressources
            sys.exit(-1)

    def check_humidity(self, channel) -> float:
        """
        Check the humidity level for a specific channel (0 - 7).

        This method reads the digital value from the ADC and converts it to a humidity percentage.

        Args:
            channel (int): The channel number to check the humidity for.

        Returns:
            HumidityMeasurement: A namedtuple containing humidity percentage and a boolean indicating if watering is required.
        """
        # TODO average over a few measurements
        # TODO check for floating values and add a warning
        # TODO check for 0 values and add a warning
        digital_value = self.adc.analogRead(channel)
        humidity_value = round((1 - digital_value / 255) * 100, 1)
        logger.info(f"humidity: {humidity_value}")
        return humidity_value

    def destroy(self):
        """Clean up resources and close connections to the ADC device."""
        self.adc.close()
        logger.info("Humidity sensor ADC terminated")
