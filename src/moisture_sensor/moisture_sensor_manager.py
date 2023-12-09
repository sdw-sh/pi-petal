from ADCDevice import *
import sys
import logging

logger = logging.getLogger(__name__)


# for 8 bit ADC
class MoistureSensorManager:
    def __init__(self, adc):
        self.adc = adc
        logger.info("HumiditySensorManager instantiated")

    @staticmethod
    def create_asd7830_based_controller():
        adc_device = ADCDevice()
        if adc_device.detectI2C(0x4B):
            adc = ADS7830()
            # TODO remove all print statement or replace with logging
            print("ADC found")
            return MoistureSensorManager(adc)
        else:
            logger.critical("ADC not found, critical error, terminating")
            # TODO throw an error to allow for clean up of other ressources
            sys.exit(-1)

    def check_humidity(self, channel: int) -> float:
        """
        Check the humidity level for a specific channel (0 - 7).

        This method reads the digital value from the ADC and converts it
        to a humidity arbitrary unit (AU),
        technically the percentage of max possible current coming from the sensor).

        Args:
            channel (int): The channel number to check the humidity for (0 - 7).

        Returns:
            float: The humidity level as a percentage in arbitrary units (AU).
        """
        # TODO average over a few measurements
        # TODO check for floating values and add a warning
        # TODO check for 0 values and add a warning
        digital_value = self.adc.analogRead(channel)
        humidity_value = round((1 - digital_value / 255) * 100, 1)
        logger.info(f"humidity: {humidity_value} AU")
        return humidity_value

    def destroy(self):
        """Clean up resources and close connections to the ADC device."""
        self.adc.close()
        logger.info("Humidity sensor ADC terminated")
