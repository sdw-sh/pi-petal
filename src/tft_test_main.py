from display.plant_update import plant_update
from display.tft_display_manager import TftDisplayManager
from plant_register.plant import Plant


display = TftDisplayManager()

display.update(
    "Small Palm Tree",
    [
        "Threshold: 46",
        "Measured: 52.6",
        "Measurement Time:",
        "15:10 05.03.2024",
        "Last Irrigation:",
        "05:21 03.03.2024",
        "Sensor / Valve: 3 / 1",
    ],
)

plant = Plant("Geigenblattfeige", 2)

display.update(**plant_update(plant))
