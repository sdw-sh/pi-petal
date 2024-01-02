import logging
import time
from pydispatch import dispatcher
import threading
import signal


from logging_definition import log_setup
from board_setup import initialize_board
from button_manager import ButtonManager
from control_state import ControlState, ControlElement
from plant import Plant
from pump.pump_manager import PumpManager
from valve_manager import ValveManager


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

# plants = []


def map_plant_moisture_to_control(plant: Plant) -> ControlElement:
    return ControlElement(
        name=plant.plant_name,
        button_1=lambda *_: plant.change_watering_threshold(+2),
        button_2=lambda *_: plant.change_watering_threshold(-2),
        display=lambda *_: plant.get_plant_string(),
    )


def map_plant_Watering_to_control(plant: Plant) -> ControlElement:
    return ControlElement(
        name="",
        button_1=lambda *_: plant.change_watering_threshold(+2),
        button_2=lambda *_: plant.change_watering_threshold(-2),
        display=lambda *_: plant.get_plant_string(),
    )


control_elements = list(map(map_plant_moisture_to_control, plants))

if __name__ == "__main__":
    initialize_board()
    pump = PumpManager(
        pump_pin=33,
        on_on_callback=None,
        on_off_callback=None,
    )
    valves = ValveManager({0: 35, 1: 37})

    def water_valve(valve, seconds):
        valves.open(valve)
        pump.start()

        def stop():
            pump.stop()
            valves.close(valve)

        timer = threading.Timer(seconds, stop)
        timer.start()
        # print(f"seconds: {seconds}")
        # time.sleep(seconds)
        # pump.pump(seconds)
        # valves.close(valve)

    def water_valve_t(valve, seconds):
        valves.open(valve)
        pump.start()
        time.sleep(seconds)
        pump.stop()
        valves.close(valve)

    def eventCatcher(event):
        threading.Thread(
            target=water_valve_t,
            args=(event["valve"], event["seconds"]),
        ).start()
        # water_valve(event["valve"], event["seconds"])

    dispatcher.connect(eventCatcher, "MyKey")

    control_elements.append(
        ControlElement(
            name="",
            button_1=lambda *_: dispatcher.send(
                "MyKey",
                event={"valve": 0, "seconds": 3},
            ),
            button_2=lambda *_: dispatcher.send(
                "MyKey",
                event={"valve": 0, "seconds": 1},
            ),
            display=lambda *_: "Water valve 0",
        )
    )

    #    control_elements.append(
    #        ControlElement(
    #            name="",
    #            button_1=lambda *_: water_valve(valve=1, seconds=0.5),
    #            button_2=lambda *_: water_valve(valve=1, seconds=1),
    #            display=lambda *_: "Water valve 1",
    #        )
    #    )

    def map_plant_moisture_to_control(plant: Plant) -> ControlElement:
        return ControlElement(
            name=plant.plant_name,
            button_1=lambda *_: plant.change_watering_threshold(+2),
            button_2=lambda *_: plant.change_watering_threshold(-2),
            display=lambda *_: plant.get_plant_string(),
        )

    def map_plant_Watering_to_control(plant: Plant) -> ControlElement:
        return ControlElement(
            name="",
            button_1=lambda *_: plant.change_watering_threshold(+2),
            button_2=lambda *_: plant.change_watering_threshold(-2),
            display=lambda *_: plant.get_plant_string(),
        )

    control_state = ControlState(control_elements)
    ButtonManager(
        [
            {
                "pin": 12,  # 12,16,18
                "callback": control_state.change_active_selection,
            },
            {
                "pin": 18,  # 12,16,18
                "callback": control_state.button_2,
            },
            {
                "pin": 16,  # 12,16,18
                "callback": control_state.button_1,
            },
        ]
    )
    signal.pause()
