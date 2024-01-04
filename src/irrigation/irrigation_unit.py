import threading
import time


class IrrigationUnit:
    def __init__(self, pump_manager, valve_manager) -> None:
        self.pump = pump_manager
        self.valves = valve_manager

    def water(self, valve, time_in_s):
        threading.Thread(
            target=self._water_internal,
            args=(valve, time_in_s),
        ).start()

    def _water_internal(self, valve, time_in_s):
        self.valves.open(valve)
        self.pump.start()
        time.sleep(time_in_s)
        self.pump.stop()
        self.valves.close(valve)
