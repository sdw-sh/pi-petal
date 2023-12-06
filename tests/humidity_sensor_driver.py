from ADCDevice import *
import sys
from collections import namedtuple
import logging

logger = logging.getLogger(__name__)

HumidityMeasurement = namedtuple("HumidityMeasurement", ["humidity", "requires_watering"]) 

# for 8 bit ADC
# currently maps the channel index to tthe channel on the board, not ideal but acceptable
class HumiditySensorDriver:

    def __init__(self, adc, number_of_channels, default_watering_threshold = 0.5):
        self.adc = adc
        self.humidity_thresholds = [default_watering_threshold] * number_of_channels

        print("__init__ HumiditySensorController")

    @staticmethod
    def create_asd7830_based_controller(number_of_channels, default_watering_threshold = 0.5):
        adc_device = ADCDevice()
        if adc_device.detectI2C(0x4b):                                                   
            adc = ADS7830()
            print("ADC found")
            return HumiditySensorDriver(adc, number_of_channels, default_watering_threshold = 0.5, )
        else:            
            print("ADC not found, critical error, terminating")
            sys.exit(-1)
        
    def set_humidity_threshold(self, channel, value):
        self.humidity_thresholds[channel] = value

    def get_humidity_threshold(self, channel):
        return self.humidity_thresholds[channel]
    
    def check_humidity(self, channel):
        """
        Check the humidity level for a specific channel.

        This method reads the digital value from the ADC, converts it to a humidity percentage,
        and determines if watering is required based on the set threshold.

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

        log_message = f'humidity: {humidity_value}'
        # print(f"requires watering: {requires_watering}, humidity: {humidity}")
        print(log_message)
        logger.info(log_message)

        return HumidityMeasurement(humidity_value, humidity_value < self.humidity_thresholds[channel])
    
    def destroy(self):
        """Clean up resources and close connections to the ADC device."""
        self.adc.close()
        print("\n*** Humidity sensor ADC terminated regularly ***")