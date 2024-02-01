from display.tft_display_manager import TftDisplayManager


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
        "Sensor / Valve: 3",
    ],
)
