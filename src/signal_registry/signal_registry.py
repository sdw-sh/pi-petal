from signal_registry.register import Register
from signal_registry.events import (
    MoistureMeasurementResultEvent,
    RequestMoistureMeasurementEvent,
    MoistureMeasurementsResultEvent,
    IrrigateEvent,
    PanicEvent,
    UpdateDisplayEvent,
    ButtonEvent,
)


class SignalRegistry:
    CHECK_PLANTS = Register("check_plants", lambda: None)
    REQUEST_MOISTURE_MEASUREMENTS = Register(
        "REQUEST_MOISTURE_MEASUREMENTS", RequestMoistureMeasurementEvent
    )
    MOISTURE_MEASUREMENT_RESULTS = Register(
        "MOISTURE_MEASUREMENT_RESULTS", MoistureMeasurementsResultEvent
    )
    MOISTURE_MEASUREMENT_RESULT = Register(
        "MOISTURE_MEASUREMENT_RESULT", MoistureMeasurementResultEvent
    )
    UPDATE_DISPLAY = Register("UPDATE_DISPLAY", UpdateDisplayEvent)
    IRRIGATE = Register("IRRIGATE", IrrigateEvent)
    PANIC = Register("PANIC", PanicEvent)
    CALM = Register("CALM", lambda: None)
    BUTTON = Register("BUTTON", ButtonEvent)
