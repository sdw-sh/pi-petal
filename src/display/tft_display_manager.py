import time
import logging
import st7735

from typing import List
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

logger = logging.getLogger(__name__)


class Color:
    MAIN_FONT_COLOR = (0, 255, 0)


class TftDisplayManager:
    def __init__(self) -> None:
        self.display = st7735.ST7735(
            port=0,
            cs=0,
            dc="GPIO25",
            backlight=None,
            rst="GPIO24",
            width=128,
            height=160,
            rotation=-90,
            invert=False,
            spi_speed_hz=4000000,
            offset_left=0,
            offset_top=0,
        )
        self.width = self.display.width
        self.height = self.display.height
        # self.montserrat = ImageFont.truetype("../assets/fonts/Montserrat-Bold.ttf", 14)
        self.emphasized_font = ImageFont.truetype("./assets/fonts/B612-Bold.ttf", 14)
        self.regular_font = ImageFont.truetype("./assets/fonts/B612-Regular.ttf", 14)
        self.img = Image.new("RGB", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.img)

    def update(
        self,
        headline: str = "",
        lines: List[str] = [],
    ):
        if len(lines) > 6:
            logger.warning(
                "The TFT display can display a maximum of a headline and 6 lines."
            )
        # clear the screen
        self.draw.rectangle(
            (0, 0, self.width, self.height),
            # outline=(255, 255, 0),
            fill=(0, 0, 0),
        )
        self.draw.text(
            (2, 0),
            headline,
            font=self.emphasized_font,
            fill=Color.MAIN_FONT_COLOR,
        )
        line_x = 19
        self.draw.line(
            (5, line_x, self.width - 5, line_x),
            fill=(0, 200, 0),
        )
        height_offset = 21
        line_height = 17
        for index, line in enumerate(lines):
            self.draw.text(
                (2, height_offset + index * line_height),
                line,
                font=self.regular_font,
                fill=Color.MAIN_FONT_COLOR,
            )
        self.display.display(self.img)
