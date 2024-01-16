from signal_registry.register import Register
from signal_registry.events import (
    RequestMoistureMeasurementEvent,
    MoistureMeasurementResultEvent,
    IrrigateEvent,
    PanicEvent,
    UpdateDisplayEvent,
)


class SignalRegistry:
    CHECK_PLANTS = Register("check_plants", None)
    REQUEST_MOISTURE = Register(
        "REQUEST_MOISTURE_MEASUREMENTS", RequestMoistureMeasurementEvent
    )
    MOISTURE_MEASUREMENT_RESULTS = Register(
        "MOISTURE_MEASUREMENT_RESULTS", MoistureMeasurementResultEvent
    )
    UPDATE_DISPLAY = Register("UPDATE_DISPLAY", UpdateDisplayEvent)
    IRRIGATE = Register("IRRIGATE", IrrigateEvent)
    PANIC = Register("PANIC", PanicEvent)
    CALM = Register("CALM", None)
