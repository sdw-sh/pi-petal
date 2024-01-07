import threading

from pydispatch import dispatcher

from event_signal import EventSignal


class Scheduler:
    def __init__(self) -> None:
        # how often the moisture of the plants should be measured
        self.moisture_measurement_interval = 60 * 0.00010

    def start(self):
        threading.Timer(
            self.moisture_measurement_interval,
            self.request_moisture_measurement,
        ).start()

    def request_moisture_measurement(self):
        dispatcher.send(
            signal=EventSignal.CHECK_PLANTS,
            sender=self,
            event=None,
        )
