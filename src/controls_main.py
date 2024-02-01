import logging
import time
import threading
import signal

from pydispatch import dispatcher
from dotenv import load_dotenv

from logging_definition import log_setup
from board_setup import initialize_board
from buttons.button_manager import ButtonManager
from control_state.control_state import ControlState, ControlElement
from plant_register.plant import Plant
from irrigation.pump_manager import PumpManager
from irrigation.valve_manager import ValveManager
from irrigation.create_irrigation_unit import create_irrigation_unit

load_dotenv()

log_setup(f"valve_and_pump.log")
logger = logging.getLogger(__name__)


logging.info(">>>>>   Starting controls testing   <<<<<")

plants = [
    Plant("Palme", 0, watering_threshold=60, water_plant=False),
    Plant("Kaktus", 1, watering_threshold=30),
    Plant(
        "Gummibaum",
        2,
        plant_id="Test Plant 1",
        water_plant=False,
    ),
    Plant(
        "Wasserpflanze",
        3,
        valve=5,
        plant_id="Test Plant 2",
        water_plant=False,
    ),
    Plant(
        "Geldbaum",
        4,
        valve=5,
        plant_id="Test Plant 3",
    ),
]

# plants = []


def map_plant_moisture_to_control(plant: Plant) -> ControlElement:
    return ControlElement(
        name=plant.plant_name,
        button_1=lambda *_: plant.change_irrigation_threshold(+2),
        button_2=lambda *_: plant.change_irrigation_threshold(-2),
        display=lambda *_: plant.get_plant_string(),
    )


def map_plant_Watering_to_control(plant: Plant) -> ControlElement:
    return ControlElement(
        name="",
        button_1=lambda *_: plant.change_irrigation_threshold(+2),
        button_2=lambda *_: plant.change_irrigation_threshold(-2),
        display=lambda *_: plant.get_plant_string(),
    )


control_elements = list(map(map_plant_moisture_to_control, plants))

if __name__ == "__main__":
    initialize_board()
    irrigationUnit = create_irrigation_unit()

    def eventCatcher(event):
        irrigationUnit.water(event["valve"], event["seconds"])

    dispatcher.connect(eventCatcher, "WaterPlant")

    control_elements.append(
        ControlElement(
            name="",
            button_1=lambda *_: dispatcher.send(
                "WaterPlant",
                event={"valve": 0, "seconds": 10},
            ),
            button_2=lambda *_: dispatcher.send(
                "WaterPlant",
                event={"valve": 0, "seconds": 1},
            ),
            display=lambda *_: "Water valve 0",
        )
    )

    control_elements.append(
        ControlElement(
            name="",
            button_1=lambda *_: irrigationUnit.water(1, 3),
            # dispatcher.send(
            #    "WaterPlant",
            #    event={"valve": 1, "seconds": 3},
            # ),
            button_2=lambda *_: dispatcher.send(
                "WaterPlant",
                event={"valve": 1, "seconds": 1},
            ),
            display=lambda *_: "Water valve 1",
        )
    )

    def map_plant_moisture_to_control(plant: Plant) -> ControlElement:
        return ControlElement(
            name=plant.plant_name,
            button_1=lambda *_: plant.change_irrigation_threshold(+2),
            button_2=lambda *_: plant.change_irrigation_threshold(-2),
            display=lambda *_: plant.get_plant_string(),
        )

    def map_plant_Watering_to_control(plant: Plant) -> ControlElement:
        return ControlElement(
            name="",
            button_1=lambda *_: plant.change_irrigation_threshold(+2),
            button_2=lambda *_: plant.change_irrigation_threshold(-2),
            display=lambda *_: plant.get_plant_string(),
        )

    control_state = ControlState(control_elements)
    ButtonManager(
        [
            {
                "pin": 18,  # 12,16,18
                "callback": control_state.button_2,
            },
            {
                "pin": 16,  # 12,16,18
                "callback": control_state.button_1,
            },
            {
                "pin": 12,  # 12,16,18
                "callback": control_state.change_active_selection,
            },
        ]
    )
    # TODO add sigterm handling
    # signal.signal(signal.SIGINT, self.exit_gracefully)
    # signal.signal(signal.SIGTERM, self.exit_gracefully)
    signal.pause()
