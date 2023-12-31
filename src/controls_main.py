import logging
import time
import RPi.GPIO as GPIO


from logging_definition import log_setup
from board_setup import initialize_board
from button_manager import ButtonManager
from control_state import ControlState, ControlElement
from plant import Plant

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
        valve_number=5,
        plant_id="Test Plant 2",
        water_plant=False,
    ),
    Plant(
        "Geldbaum",
        4,
        valve_number=5,
        plant_id="Test Plant 3",
    ),
]


def map_plant_to_control(plant: Plant):
    return ControlElement(
        name=plant.plant_name,
        button_1=lambda *_: plant.change_watering_threshold(+2),
        button_2=lambda *_: plant.change_watering_threshold(-2),
        display=lambda *_: plant.get_plant_string(),
    )


control_elements = list(map(map_plant_to_control, plants))

if __name__ == "__main__":
    initialize_board()
    control_state = ControlState(control_elements)
    ButtonManager(
        [
            {
                "pin": 12,  # 12,16,18
                "callback": control_state.change_active_selection,
            },
            {
                "pin": 16,  # 12,16,18
                "callback": control_state.button_1,
            },
            {
                "pin": 18,  # 12,16,18
                "callback": control_state.button_2,
            },
        ]
    )
    while True:
        time.sleep(60)
