from signal_registry.register import Register
from signal_registry.events import (
    MoistureMeasurementResultEvent,
    RequestMoistureMeasurementEvent,
    MoistureMeasurementsResultEvent,
    IrrigationEvent,
    PanicEvent,
    UpdateDisplayEvent,
    ButtonEvent,
)


class SignalRegistry:
    CHECK_PLANTS = Register("check_plants", lambda: None)
    REQUEST_MOISTURE_MEASUREMENTS = Register(
        "REQUEST_MOISTURE_MEASUREMENTS", RequestMoistureMeasurementEvent
    )
    MOISTURE_MEASUREMENT_RESULT = Register(
        "MOISTURE_MEASUREMENT_RESULT", MoistureMeasurementResultEvent
    )
    UPDATE_DISPLAY = Register("UPDATE_DISPLAY", UpdateDisplayEvent)
    IRRIGATE = Register("IRRIGATE", IrrigationEvent)
    IRRIGATION_FINISHED = Register("IRRIGATION_FINISHED", IrrigationEvent)
    PANIC = Register("PANIC", PanicEvent)
    CALM = Register("CALM", lambda: None)
    BUTTON = Register("BUTTON", ButtonEvent)
