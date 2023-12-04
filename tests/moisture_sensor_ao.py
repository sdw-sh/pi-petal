import time
from ADCDevice import *
import sys
from collections import namedtuple

HumidityMeasurement = namedtuple("HumidityMeasurement", ["humidity", "requires_watering"]) 

# for 8 bit ADC
# currently maps the channel index to tthe channel on the board, not ideal but acceptable
class HumidityController:

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
            return HumidityController(adc, number_of_channels, default_watering_threshold = 0.5, )
        else:            
            print("ADC not found, critical error, terminating")
            sys.exit(-1)
        
    def set_humidity_threshold(self, channel, value):
        self.humidity_thresholds[channel] = value
    def get_humidity_threshold(self, channel):
        return self.humidity_thresholds[channel]
    def check_humidity(self, channel):
        # TODO average over a few measurements
        # TODO check for floating values and add a warning
        # TODO check for 0 values and add a warning
        digital_value = self.adc.analogRead(channel)
        humidity_value = (1 - digital_value / 255) * 100
        return HumidityMeasurement(humidity_value, humidity_value < self.humidity_thresholds[channel])
    
    def destroy(self):
        self.adc.close()
        print("\n*** Humidity sensor ADC terminated regularly ***")





################################################################################################################

def humidity_sensor_demo(sensor):
    while True:
        humidity, requires_watering = sensor.check_humidity(0)
        print(f"requires watering: {requires_watering}, humidity: {humidity}")
        time.sleep(0.2)

if __name__ == '__main__':
    print ("Starting")
    try:
        sensor = HumidityController.create_asd7830_based_controller(1)
        sensor.set_humidity_threshold(0, 0.4)
        humidity_sensor_demo(sensor)
    except KeyboardInterrupt:
        sensor.destroy()
