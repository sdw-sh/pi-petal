from moisture_sensor.moisture_sensor_manager import MoistureSensorManager
from moisture_sensor.moisture_sensor_connector import MoistureSensorConnector


def create_moisture_sensor_connector():
    manager = MoistureSensorManager.create_asd7830_based_controller()
    connector = MoistureSensorConnector(manager)
    return connector
