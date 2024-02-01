import time

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

disp.begin()

width = disp.width
height = disp.height

if 0:
    image = Image.open("deployrainbows.gif")
    frame = 0
    while True:
        try:
            image.seek(frame)
            disp.display(image.resize((width, height)))
            frame += 1
            time.sleep(0.05)
        except EOFError:
            frame = 0

img = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(img)

# Draw a purple rectangle with yellow outline.
# draw.rectangle(
#    (10, 10, width - 10, height - 10), outline=(255, 255, 0), fill=(255, 0, 255)
# )

# Draw some shapes.
# Draw a blue ellipse with a green outline.
# draw.ellipse((10, 10, width - 10, height - 10), outline=(0, 255, 0), fill=(0, 0, 255))

line_height = 18

# Draw a white X.
draw.line(
    (0, line_height, width, line_height),
    fill=(0, 200, 0),
)
# draw.line((10, height - 10, width - 10, 10), fill=(255, 255, 255))

# Draw a cyan triangle with a black outline.
# draw.polygon(
#    [(width / 2, 10), (width - 10, height - 10), (10, height - 10)],
#    outline=(0, 0, 0),
#    fill=(0, 255, 255),
# )

font_montserrat = ImageFont.truetype("../assets/fonts/Montserrat-Bold.ttf", 14)
font_b612_bold = ImageFont.truetype("../assets/fonts/B612-Bold.ttf", 14)
font_b612_regular = ImageFont.truetype("../assets/fonts/B612-Regular.ttf", 14)

# Write some text
draw.text(
    (2, 0),
    "Hello World! 123456789012345678901234567890",
    font=font_b612_bold,
    fill=(0, 255, 0),
)
draw.text(
    (2, line_height),
    "Hello World! 123456789012345678901234567890",
    font=font_b612_regular,
    fill=(0, 255, 0),
)
draw.text(
    (2, line_height * 2),
    "Hello World! 123456789012345678901234567890",
    font=font_b612_bold,
    fill=(0, 255, 0),
)
draw.text(
    (2, line_height * 3),
    "Hello World! 123456789012345678901234567890",
    font=font_montserrat,
    fill=(255, 0, 255),
)
draw.text(
    (2, line_height * 4),
    "Hello World! 123456789012345678901234567890",
    font=font_montserrat,
    fill=(0, 255, 255),
)
draw.text(
    (2, line_height * 5),
    "Special Characters:",
    font=font_montserrat,
    fill=(255, 255, 0),
)
draw.text(
    (2, line_height * 6),
    "öäüßáà",
    font=font_b612_regular,
    fill=(255, 255, 255),
)
# display!
disp.display(img)

i = 0

while False:
    i += 1
    draw.rectangle(
        (0, 0, disp.width, disp.height),
        # outline=(255, 255, 0),
        fill=(0, 0, 0),
    )
    draw.text(
        (2, line_height * 6),
        str(i),
        font=font_b612_regular,
        fill=(255, 255, 255),
    )
    disp.display(img)
