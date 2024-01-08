import threading
import datetime
import time
import logging

logger = logging.getLogger(__name__)


class IrrigationUnit:
    def __init__(self, pump_manager, valve_manager) -> None:
        self.pump = pump_manager
        self.valves = valve_manager
        self.last_watering_event = None
        self.watering_interval = datetime.timedelta(milliseconds=500)

    def _water(self, valve, time_in_s):
        threading.Thread(
            target=self._water_internal,
            args=(valve, time_in_s),
        ).start()

    def can_water(self):
        if self.last_watering_event is None:
            return True
        return (
            datetime.datetime.now() - self.last_watering_event > self.watering_interval
        )

    def water(self, valve, time_in_s):
        if not self.can_water():
            logger.warn("Irrigation cancelled, irrigation unit in refractory phase!")
            return
        self.valves.open(valve)
        self.pump.start()
        time.sleep(time_in_s)
        self.pump.stop()
        self.valves.close(valve)
        self.last_watering_event = datetime.datetime.now()
