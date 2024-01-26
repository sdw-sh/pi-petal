import os

from pydispatch import dispatcher

from signal_registry.signal_registry import SignalRegistry
from buttons.button_manager import ButtonManager
from buttons.buttons import Buttons
from control_state.control_state import ControlState


class ButtonConnector:
    def __init__(self, buttons: ButtonManager) -> None:
        self.buttons = buttons


def create_button_connector():
    button_definition = [
        {
            "pin": int(os.getenv("BUTTON_1_PIN")),  # 12
            "callback": lambda: dispatcher.send(
                signal=SignalRegistry.BUTTON.signal,
                # sender=,
                event=SignalRegistry.BUTTON.event(Buttons.BUTTON_1),
            ),
        },
        {
            "pin": int(os.getenv("BUTTON_2_PIN")),  # 16
            "callback": lambda: dispatcher.send(
                signal=SignalRegistry.BUTTON.signal,
                # sender=,
                event=SignalRegistry.BUTTON.event(Buttons.BUTTON_2),
            ),
        },
        {
            "pin": int(os.getenv("BUTTON_3_PIN")),  # 18
            "callback": lambda: dispatcher.send(
                signal=SignalRegistry.BUTTON.signal,
                # sender=,
                event=SignalRegistry.BUTTON.event(Buttons.BUTTON_3),
            ),
        },
    ]
    manager = ButtonManager(button_definition)
    connector = ButtonConnector(manager)
    return connector
