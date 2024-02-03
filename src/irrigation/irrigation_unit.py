import threading
import datetime
import time
import logging

from typing import List, Callable
from irrigation.pump_manager import PumpManager
from irrigation.valve_manager import ValveManager

from signal_registry.events import IrrigationEvent

logger = logging.getLogger(__name__)


class IrrigationUnit:
    def __init__(self, pump: PumpManager, valves: ValveManager) -> None:
        self.pump = pump
        self.valves = valves
        self.last_watering_event = None
        # self.watering_interval = datetime.timedelta(milliseconds=500)
        self.irrigation_queue: List[IrrigationEvent] = []
        self.irrigation_in_process = False
        self.irrigation_finished_callback: Callable[[IrrigationEvent], None]

    # def can_water(self):
    #    if self.last_watering_event is None:
    #        return True
    #    return (
    #        datetime.datetime.now() - self.last_watering_event > self.watering_interval
    #    )

    def irrigate(self, event: IrrigationEvent):
        self.irrigation_queue.append(event)
        self._start_irrigation()

    def _start_irrigation(self):
        if self.irrigation_in_process:
            return
        if len(self.irrigation_queue) == 0:
            return
        self.irrigation_in_process = True
        irrigation_event = self.irrigation_queue.pop(0)
        logger.info(f"Irrigating {irrigation_event.valve}")
        self._irrigate(irrigation_event.valve, irrigation_event.time_in_s)
        self.irrigation_finished_callback(irrigation_event)
        self.irrigation_in_process = False
        self._start_irrigation()

    def _irrigate(self, valve, time_in_s):
        # if not self.can_water():
        #    logger.warn("Irrigation cancelled, irrigation unit in refractory phase!")
        #    return
        valve_open = self.valves.open(valve)
        if not valve_open:
            return
        self.pump.start()
        time.sleep(time_in_s)
        self.pump.stop()
        self.valves.close(valve)
        # self.last_watering_event = datetime.datetime.now()
