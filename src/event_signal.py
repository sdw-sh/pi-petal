# Ponder putting signal and event creator together
# FOO = ("FOO_SIGNAL", Foo) # where Foo is the event creator class definition (not an instance)
# may use an named tuple with signal and event

class EventSignal:
    CHECK_PLANTS = "CHECK_PLANTS"
    REQUEST_MOISTURE_MEASUREMENTS = "REQUEST_MOISTURE_MEASUREMENTS"
    MOISTURE_MEASUREMENT_RESULTS = "MOISTURE_MEASUREMENT_RESULTS"
    UPDATE_DISPLAY = "UPDATE_DISPLAY"
    IRRIGATE = "IRRIGATE"
    PANIC = "PANIC"
    CALM = "CALM"
