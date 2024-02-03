from pydispatch import dispatcher
from irrigation.create_irrigation_unit import create_irrigation_unit
from irrigation.irrigation_unit import IrrigationUnit

from irrigation.pump_manager import PumpManager
from irrigation.valve_manager import ValveManager
from signal_registry.events import IrrigationEvent
from signal_registry.signal_registry import SignalRegistry


class IrrigationUnitConnector:
    def __init__(self, irrigationUnit: IrrigationUnit) -> None:
        self.irrigationUnit = irrigationUnit

        self.irrigationUnit.irrigation_finished_callback = self.irrigation_finished

        dispatcher.connect(
            self.irrigationUnit.irrigate,
            SignalRegistry.IRRIGATE.signal,
        )

    def irrigation_finished(self, event: IrrigationEvent):
        dispatcher.send(
            signal=SignalRegistry.IRRIGATION_FINISHED.signal,
            sender=self,
            event=event,
        )


def create_irrigation_unit_connector():
    unit = create_irrigation_unit()
    return IrrigationUnitConnector(unit)
