from display.tft_display_manager import TftDisplayManager


display = TftDisplayManager()

display.update(
    "Small Palm Tree",
    [
        "threshold: 46",
        "measured: 52.6",
        "measurement time",
        "15:10 05.03.2024",
        "last irrigation",
        "05:21 03.03.2024",
    ],
)
