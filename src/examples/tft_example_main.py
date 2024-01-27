from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import st7735

disp = st7735.ST7735(
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
WIDTH = disp.width
HEIGHT = disp.height
img = Image.new("RGB", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(img)
# Load default font.
font = ImageFont.load_default(16)
# font2 = ImageFont.
# Write some text
draw.text(
    (2, 0),
    "Hello World! 123456789012345678901234567890",
    font=font,
    fill=(0, 255, 0),
)
draw.text(
    (2, 18),
    "Hello World! 123456789012345678901234567890",
    font=font,
    fill=(0, 0, 255),
)
draw.text(
    (2, 36),
    "Special Characters: öäüßáà",
    font=font,
    fill=(255, 0, 0),
)
# display!
disp.display(img)
