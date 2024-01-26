import threading

from pydispatch import dispatcher

from event_signal import EventSignal
from external_scripts.repeat_timer import RepeatTimer


class Scheduler:
    def __init__(self) -> None:
        self.moisture_measurement_interval = 100  # 60 * 5

    def start(self, run_immidiately=False):
        if run_immidiately:
            self.request_moisture_measurement()
        timer = RepeatTimer(
            self.moisture_measurement_interval,
            self.request_moisture_measurement,
        )
        timer.start()

    def request_moisture_measurement(self):
        dispatcher.send(
            signal=EventSignal.CHECK_PLANTS,
            sender=self,
            event=None,
        )
