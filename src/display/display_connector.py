from pydispatch import dispatcher

from signal_registry.signal_registry import SignalRegistry
from display.display_manager import DisplayManager


class DisplayConnector:
    def __init__(self, display: DisplayManager) -> None:
        self.display = display
        dispatcher.connect(
            self.update,
            SignalRegistry.UPDATE_DISPLAY.signal,
        )

    def update(self, event):
        self.display.update(event[0], event[1])


def create_display_connector():
    manager = DisplayManager()
    connector = DisplayConnector(manager)
    return connector
