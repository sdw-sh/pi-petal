import os

from irrigation.pump_manager import PumpManager
from irrigation.valve_manager import ValveManager
from irrigation.irrigation_unit import IrrigationUnit

from dotenv import load_dotenv

# load_dotenv()


def create_pump_manager():
    pin = int(os.getenv("PUMP_PIN"))
    return PumpManager(pin)


def create_valve_manager():
    pin_str = os.getenv("VALVE_PINS")
    pin_list = [int(num.strip()) for num in pin_str.split(",")]
    return ValveManager(pin_list)


def create_irrigation_unit():
    return IrrigationUnit(
        create_pump_manager(),
        create_valve_manager(),
    )
