import time
import logging
from humidity_sensor_driver import HumiditySensorDriver

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename='moisture.log',
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt = "%Y-%m-%d %H:%M:%S"
)

logging.info('Log started')

################################################################################################################

def humidity_sensor_demo(sensor):
    while True:
        humidity, requires_watering = sensor.check_humidity(0)
        time.sleep(10*60)

if __name__ == '__main__':
    print ("Starting")
    try:
        sensor = HumiditySensorDriver.create_asd7830_based_controller(1)
        sensor.set_humidity_threshold(0, 0.4)
        humidity_sensor_demo(sensor)
    except KeyboardInterrupt:
        sensor.destroy()
