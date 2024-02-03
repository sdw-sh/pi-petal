import logging
import signal

from pydispatch import dispatcher
from dotenv import load_dotenv
from irrigation.irrigation_unit_connector import create_irrigation_unit_connector

from logging_definition import log_setup
from board_setup import initialize_board
from scheduler import Scheduler
from display.lcd_display_connector import create_display_connector
from plant_register.plant_registry_connector import create_plant_registry_connector
from moisture_sensor.create_moisture_sensor_connector import (
    create_moisture_sensor_connector,
)
from buttons.button_connector import create_button_connector

load_dotenv()

log_setup(f"messaging.log")
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    initialize_board()

    def eventCatcher(event, *args, **kwargs):
        logger.debug(f"SIGNAL: \"{kwargs['signal']}\" | EVENT: {event}")

    scheduler = Scheduler()
    plant_registry = create_plant_registry_connector()
    moisture_sensor = create_moisture_sensor_connector()
    # display = create_display_connector()
    # buttons = create_button_connector()
    dispatcher.connect(eventCatcher)
    irrigation_unit = create_irrigation_unit_connector()
    scheduler.start()

    signal.pause()
