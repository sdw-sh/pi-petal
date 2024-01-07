import logging
import signal

from pydispatch import dispatcher
from dotenv import load_dotenv

from logging_definition import log_setup
from board_setup import initialize_board
from scheduler import Scheduler
from display.display_connector import create_display_connector
from plant_register.plant_register_connector import create_plant_register_connector
from moisture_sensor.create_moisture_sensor_connector import (
    create_moisture_sensor_connector,
)

load_dotenv()

log_setup(f"messaging.log")
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    initialize_board()

    def eventCatcher(event, *args, **kwargs):
        logger.debug("event")
        logger.debug(event)
        logger.debug("args")
        logger.debug(args)
        logger.debug("kwargs")
        logger.debug(kwargs)

    dispatcher.connect(eventCatcher)

    scheduler = Scheduler()
    plant_register_connector = create_plant_register_connector()
    moisture_sensor_connector = create_moisture_sensor_connector()
    display_connector = create_display_connector()
    scheduler.start()

    signal.pause()
