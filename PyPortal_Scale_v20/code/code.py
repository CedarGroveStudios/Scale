# PyPortal Scale -- dual channel version
# Cedar Grove NAU7802 FeatherWing
# 2021-10-10 v20 Cedar Grove Studios

# uncomment the following import line to run the calibration method
# (this will eventually be put into the setup process)
# import cedargrove_scale.load_cell_calibrator

import board
import busio
import time
from math import cos, sin, pi
import storage
import digitalio
import displayio
from simpleio import tone

import adafruit_imageload
from adafruit_bitmapsaver import save_pixels
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle

import adafruit_sdcard
import adafruit_touchscreen
from adafruit_button import Button
from cedargrove_nau7802 import NAU7802

from scale_config import Configuration as config
from cedargrove_scale.defaults import (
    Defaults as default,
    Dial as dial,
    Palette as color,
    Pointer as point,
    Screen as screen,
)

debug = False

# Determine screen size
WIDTH = screen.WIDTH
HEIGHT = screen.HEIGHT

# Instantiate touch screen
ts = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL,
    board.TOUCH_XR,
    board.TOUCH_YD,
    board.TOUCH_YU,
    calibration=((5200, 59000), (5800, 57000)),
    size=(WIDTH, HEIGHT),
)

# Instantiate load sensor ADC wing
nau7802 = NAU7802(board.I2C(), address=0x2A, active_channels=2)

# Instantiate SD card
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
sd_cs = digitalio.DigitalInOut(board.SD_CS)
has_sd_card = False
try:
    sdcard = adafruit_sdcard.SDCard(spi, sd_cs)
    vfs = storage.VfsFat(sdcard)
    storage.mount(vfs, "/sd")
    print("SD card found")
    has_sd_card = True
except OSError as error:
    print("SD card NOT found:", error)


def zero_channel():
    """Initiate internal calibration for current channel, return raw zero
    offset value. Use when scale is started, a new channel is selected, or
    to adjust for measurement drift. Remove weight and tare from load cell
    before executing."""
    status_label.text = "ZERO LOAD CELL " + str(nau7802.channel)
    status_label.color = color.YELLOW
    print(
        "channel %1d calibrate.INTERNAL: %5s"
        % (nau7802.channel, nau7802.calibrate("INTERNAL"))
    )
    print(
        "channel %1d calibrate.OFFSET:   %5s"
        % (nau7802.channel, nau7802.calibrate("OFFSET"))
    )
    zero_offset = read(100)  # Average of 100 samples to establish zero offset
    print("...channel zeroed")
    status_label.text = ""
    return zero_offset


def read(samples=default.SAMPLE_AVG):
    """Read and average consecutive raw sample values for currently selected
    channel. Returns the average raw value."""
    sum = 0
    for i in range(0, samples):
        if nau7802.available:
            sum = sum + nau7802.read()
    return int(sum / samples)


def play_tone(note=None):
    if note == "high":
        tone(board.A0, 880, 0.1)
    elif note == "low":
        tone(board.A0, 440, 0.1)
    return


def screen_to_rect(width_factor=0, height_factor=0):
    """Convert normalized screen position input (0.0 to 1.0) to the display's
    rectangular pixel position."""
    return int(WIDTH * width_factor), int(HEIGHT * height_factor)


def dial_to_rect(scale_factor, center=dial.CENTER, radius=dial.RADIUS):
    """Convert normalized scale_factor input (-1.0 to 1.0) to a rectangular pixel
    position on the circumference of a circle with center (x,y pixels) and
    radius (pixels)."""
    radians = (-2 * pi) * (scale_factor)  # convert scale_factor to radians
    radians = radians + (pi / 2)  # rotate axis counterclockwise
    x = int(center[0] + (cos(radians) * radius))
    y = int(center[1] - (sin(radians) * radius))
    return x, y


def take_screenshot():
    if has_sd_card:
        print("Taking Screenshot...", end="")
        flash_status("SCREENSHOT...", 0.8)
        save_pixels("/sd/screenshot.bmp")
        print(" Screenshot stored")
        flash_status("... STORED", 0.8)
    else:
        flash_status("SCREENSHOT: NO SD CARD", 1.0)
    return


def flash_status(text="", duration=0.05):
    """Flash a status message once."""
    status_label.text = text
    status_label.color = color.WHITE
    time.sleep(duration)
    status_label.color = color.BLACK
    time.sleep(duration)
    status_label.text = ""
    return


def plot_needles(scale_1=0, scale_2=0):
    """Display channel 1 and 2 indicator needles. Input is normalized for
    0.0 to 1.0 (minimum and maximum range), but accepts any floating point value."""
    if scale_1 != min(1.0, max(scale_1, 0.0)):
        hand_1_outline = color.RED
    else:
        hand_1_outline = color.ORANGE

    if scale_2 != min(1.0, max(scale_2, 0.0)):
        hand_2_outline = color.RED
    else:
        hand_2_outline = color.GREEN

    base = dial.RADIUS // 10
    sx0, sy0 = screen_to_rect(0.00, 0.16)
    sx1, sy1 = screen_to_rect(0.00, 0.03)
    scale_plate.y = int(
        sy0 + (sy1 * min(2, max(-2, (scale_1 + scale_2))))
    )
    scale_riser.y = scale_plate.y

    x0, y0 = dial_to_rect(scale_2, radius=dial.RADIUS)
    x1, y1 = dial_to_rect(scale_2 - 0.25, radius=base // 2)
    x2, y2 = dial_to_rect(scale_2 + 0.25, radius=base // 2)
    hand_2 = Triangle(x0, y0, x1, y1, x2, y2, fill=color.GREEN, outline=hand_2_outline)
    indicator_group.append(hand_2)

    x0, y0 = dial_to_rect(scale_1, radius=dial.RADIUS)
    x1, y1 = dial_to_rect(scale_1 - 0.25, radius=base // 2)
    x2, y2 = dial_to_rect(scale_1 + 0.25, radius=base // 2)
    hand_1 = Triangle(x0, y0, x1, y1, x2, y2, fill=color.ORANGE, outline=hand_1_outline)
    indicator_group.append(hand_1)

    x0, y0 = dial.CENTER
    pivot = Circle(x0, y0, base // 2, fill=color.WHITE)
    indicator_group.append(pivot)

    return scale_1, scale_2


def erase_needles():
    indicator_group.remove(indicator_group[len(indicator_group) - 1])
    indicator_group.remove(indicator_group[len(indicator_group) - 1])
    indicator_group.remove(indicator_group[len(indicator_group) - 1])
    return


# Instantiate display and fonts
# print('*** Instantiate the display and fonts')
display = board.DISPLAY
display.brightness = config.BRIGHTNESS
scale_group = displayio.Group()

FONT_0 = bitmap_font.load_font("/fonts/Helvetica-Bold-24.bdf")
FONT_1 = bitmap_font.load_font("/fonts/OpenSans-16.bdf")
FONT_2 = bitmap_font.load_font("/fonts/OpenSans-9.bdf")

# Define displayio background and group elements
print("*** Define displayio background and group elements")

# Tare and alarm tile grid
sprite_sheet, palette = adafruit_imageload.load(
    "/cedargrove_scale/scale_sprite_sheet.bmp",
    bitmap=displayio.Bitmap,
    palette=displayio.Palette,
)
palette.make_transparent(3)

# Bitmap background
"""_bkg = open('/sd/screenshot.bmp', 'rb')
bkg = displayio.OnDiskBitmap(_bkg)
try:
    _background = displayio.TileGrid(bkg,
                                     pixel_shader=displayio.ColorConverter(),
                                     x=0, y=0)
except TypeError:
    _background = displayio.TileGrid(bkg,
                                     pixel_shader=displayio.ColorConverter(),
                                     x=0, y=0)
scale_group.append(_background)"""

# -- BUTTONS -- #
buttons = []
sx, sy = screen_to_rect(0.01, 0.02)
sw, sh = screen_to_rect(0.30, 0.20)
setup_1_button = Button(
    x=sx, y=sy, height=sh, width=sw,
    style=Button.ROUNDRECT,
    fill_color=None,
    outline_color=color.GRAY,
    name="setup_1",
    selected_fill=color.RED,
    selected_outline=color.RED,
)
scale_group.append(setup_1_button)
buttons.append(setup_1_button)

sx, sy = screen_to_rect(0.70, 0.02)
sw, sh = screen_to_rect(0.30, 0.20)
setup_2_button = Button(
    x=sx, y=sy, height=sh, width=sw,
    style=Button.ROUNDRECT,
    fill_color=None,
    outline_color=color.GRAY,
    name="setup_2",
    selected_fill=color.RED,
    selected_outline=color.RED,
)
scale_group.append(setup_2_button)
buttons.append(setup_2_button)

sx, sy = screen_to_rect(0.01, 0.25)
sw, sh = screen_to_rect(0.30, 0.20)
zero_1_button = Button(
    x=sx, y=sy, height=sh, width=sw,
    style=Button.ROUNDRECT,
    fill_color=None,
    outline_color=color.GRAY,
    name="zero_1",
    selected_fill=color.RED,
    selected_outline=color.RED,
)
scale_group.append(zero_1_button)
buttons.append(zero_1_button)

sx, sy = screen_to_rect(0.70, 0.25)
sw, sh = screen_to_rect(0.30, 0.20)
zero_2_button = Button(
    x=sx, y=sy, height=sh, width=sw,
    style=Button.ROUNDRECT,
    fill_color=None,
    outline_color=color.GRAY,
    name="zero_2",
    selected_fill=color.RED,
    selected_outline=color.RED,
)
scale_group.append(zero_2_button)
buttons.append(zero_2_button)

sx, sy = screen_to_rect(0.01, 0.50)
sw, sh = screen_to_rect(0.30, 0.19)
tare_1_button = Button(
    x=sx, y=sy, height=sh, width=sw,
    style=Button.ROUNDRECT,
    fill_color=None,
    outline_color=color.GRAY,
    name="tare_1",
    selected_fill=color.BLUE,
    selected_outline=color.BLUE,
)
scale_group.append(tare_1_button)
buttons.append(tare_1_button)

sx, sy = screen_to_rect(0.70, 0.50)
sw, sh = screen_to_rect(0.30, 0.19)
tare_2_button = Button(
    x=sx, y=sy, height=sh, width=sw,
    style=Button.ROUNDRECT,
    fill_color=None,
    outline_color=color.GRAY,
    name="tare_2",
    selected_fill=color.BLUE,
    selected_outline=color.BLUE,
)
scale_group.append(tare_2_button)
buttons.append(tare_2_button)

sx, sy = screen_to_rect(0.01, 0.70)
sw, sh = screen_to_rect(0.30, 0.20)
alarm_1_button = Button(
    x=sx, y=sy, height=sh, width=sw,
    style=Button.ROUNDRECT,
    fill_color=None,
    outline_color=color.GRAY,
    name="alarm_1",
    selected_fill=color.BLUE,
    selected_outline=color.BLUE,
)
scale_group.append(alarm_1_button)
buttons.append(alarm_1_button)

sx, sy = screen_to_rect(0.70, 0.70)
sw, sh = screen_to_rect(0.30, 0.20)
alarm_2_button = Button(
    x=sx, y=sy, height=sh, width=sw,
    style=Button.ROUNDRECT,
    fill_color=None,
    outline_color=color.GRAY,
    name="alarm_2",
    selected_fill=color.BLUE,
    selected_outline=color.BLUE,
)
scale_group.append(alarm_2_button)
buttons.append(alarm_2_button)

tare_1_icon = displayio.TileGrid(
    sprite_sheet, pixel_shader=palette, width=1, height=1, tile_width=32, tile_height=48
)
sx, sy = screen_to_rect(0.08, 0.50)
tare_1_icon.x = sx
tare_1_icon.y = sy
tare_1_icon[0] = 3
scale_group.append(tare_1_icon)

alarm_1_icon = displayio.TileGrid(
    sprite_sheet, pixel_shader=palette, width=1, height=1, tile_width=32, tile_height=48
)
sx, sy = screen_to_rect(0.08, 0.70)
alarm_1_icon.x = sx
alarm_1_icon.y = sy
alarm_1_icon[0] = 2
scale_group.append(alarm_1_icon)


tare_2_icon = displayio.TileGrid(
    sprite_sheet, pixel_shader=palette, width=1, height=1, tile_width=32, tile_height=48
)
sx, sy = screen_to_rect(0.85, 0.50)
tare_2_icon.x = sx
tare_2_icon.y = sy
tare_2_icon[0] = 7
scale_group.append(tare_2_icon)

alarm_2_icon = displayio.TileGrid(
    sprite_sheet, pixel_shader=palette, width=1, height=1, tile_width=32, tile_height=48
)
sx, sy = screen_to_rect(0.85, 0.70)
alarm_2_icon.x = sx
alarm_2_icon.y = sy
alarm_2_icon[0] = 6
scale_group.append(alarm_2_icon)

# -- DISPLAY ELEMENTS -- #
chan_1_name = Label(FONT_0, text=config.CHAN_1_NAME, color=color.ORANGE)
chan_1_name.anchor_point = (1.0, 0)
chan_1_name.anchored_position = (screen_to_rect(0.28, 0.10))
scale_group.append(chan_1_name)

chan_2_name = Label(FONT_0, text=config.CHAN_2_NAME, color=color.GREEN)
chan_2_name.anchor_point = (1.0, 0)
chan_2_name.anchored_position = (screen_to_rect(0.97, 0.10))
scale_group.append(chan_2_name)


chan_1_label = Label(FONT_0, text=config.MASS_UNITS.lower(), color=color.BLUE)
chan_1_label.anchor_point = (1.0, 0)
chan_1_label.anchored_position = (screen_to_rect(0.28, 0.38))
scale_group.append(chan_1_label)

chan_2_label = Label(FONT_0, text=config.MASS_UNITS.lower(), color=color.BLUE)
chan_2_label.anchor_point = (1.0, 0)
chan_2_label.anchored_position = (screen_to_rect(0.97, 0.38))
scale_group.append(chan_2_label)

chan_1_value = Label(FONT_0, text="0.0", color=color.WHITE)
chan_1_value.anchor_point = (1.0, 1.0)
chan_1_value.anchored_position = (screen_to_rect(0.28, 0.38))
scale_group.append(chan_1_value)

chan_2_value = Label(FONT_0, text="0.0", color=color.WHITE)
chan_2_value.anchor_point = (1.0, 1.0)
chan_2_value.anchored_position = (screen_to_rect(0.97, 0.38))
scale_group.append(chan_2_value)

tare_1_value = Label(FONT_2, text="0.0", color=color.GRAY)
tare_1_value.anchor_point = (1.0, 0.5)
tare_1_value.anchored_position = (screen_to_rect(0.28, 0.56))
scale_group.append(tare_1_value)

tare_2_value = Label(FONT_2, text="0.0", color=color.GRAY)
tare_2_value.anchor_point = (0.0, 0.5)
tare_2_value.anchored_position = (screen_to_rect(0.75, 0.56))
scale_group.append(tare_2_value)

alarm_1_value = Label(FONT_2, text="0.0", color=color.GRAY)
alarm_1_value.anchor_point = (1.0, 0.5)
alarm_1_value.anchored_position = (screen_to_rect(0.28, 0.75))
scale_group.append(alarm_1_value)

alarm_2_value = Label(FONT_2, text="0.0", color=color.GRAY)
alarm_2_value.anchor_point = (0.0, 0.5)
alarm_2_value.anchored_position = (screen_to_rect(0.75, 0.75))
scale_group.append(alarm_2_value)

# Define scale graphic
sx, sy = screen_to_rect(0.46, 0.16)
sw, sh = screen_to_rect(0.08, 0.25)
scale_riser = Rect(
    sx, sy, width=sw, height=sh,
    fill=color.GRAY,
    outline=color.BLACK,
)
scale_group.append(scale_riser)

sx, sy = screen_to_rect(0.34, 0.16)
sw, sh = screen_to_rect(0.32, 0.06)
scale_plate = RoundRect(
    sx, sy, width=sw, height=sh,
    r=5,
    fill=color.GRAY,
    outline=color.BLACK,
)
scale_group.append(scale_plate)

sx0, sy0 = screen_to_rect(0.50, 0.50)
sx1, sy1 = screen_to_rect(0.65, 0.80)
sx2, sy2 = screen_to_rect(0.35, 0.80)
scale_base = Triangle(
    sx0, sy0, sx1, sy1, sx2, sy2,
    fill=color.GRAY,
    outline=color.BLACK,
)
scale_group.append(scale_base)

sx, sy = screen_to_rect(0.34, 0.80)
sw, sh = screen_to_rect(0.32, 0.06)
scale_foot = RoundRect(
    sx, sy, width=sw, height=sh,
    r=5,
    fill=color.GRAY,
    outline=color.BLACK,
)
scale_group.append(scale_foot)

sx, sy = screen_to_rect(0.50, 0.50)
ry, ry = screen_to_rect(0.00, 0.25)
scale_dial = Circle(
    sx, sy, ry,
    fill=color.BLUE_DK,
    outline=color.WHITE,
    stroke=1,
)
scale_group.append(scale_dial)

for i in range(0, config.MAX_GR, config.MAX_GR // 10):
    hash_value = Label(FONT_2, text=str(i), color=color.CYAN)
    hash_value.anchor_point = (0.5, 0.5)
    hash_value.anchored_position = dial_to_rect(
        i / config.MAX_GR, radius=point.IN_PATH_RADIUS
    )
    scale_group.append(hash_value)

    x0, y0 = dial_to_rect(i / config.MAX_GR, radius=point.OUT_PATH_RADIUS)
    x1, y1 = dial_to_rect(i / config.MAX_GR, radius=dial.RADIUS)
    hash_mark_a = Line(x0, y0, x1, y1, color.CYAN)
    scale_group.append(hash_mark_a)

    x0, y0 = dial_to_rect(
        (i + config.MAX_GR / 20) / config.MAX_GR,
        radius=point.OUT_PATH_RADIUS + point.RADIUS,
    )
    x1, y1 = dial_to_rect((i + config.MAX_GR / 20) / config.MAX_GR, radius=dial.RADIUS)
    hash_mark_b = Line(x0, y0, x1, y1, color.CYAN)
    scale_group.append(hash_mark_b)

status_label = Label(FONT_2, text=" ", color=None)
status_label.anchor_point = (0.5, 0.5)
sx, sy = screen_to_rect(WIDTH // 2, 0.94)
status_label.anchored_position = (sx, sy)
scale_group.append(status_label)

# Define moveable bubble and alarm pointers in the indicator group
indicator_group = displayio.Group()

chan_1_alarm = Circle(
    -50, -50, point.RADIUS, fill=color.ORANGE, outline=color.ORANGE, stroke=point.STROKE
)
indicator_group.append(chan_1_alarm)

chan_2_alarm = Circle(
    -50, -50, point.RADIUS, fill=color.GREEN, outline=color.GREEN, stroke=point.STROKE
)
indicator_group.append(chan_2_alarm)

# Place the indicators into the scale group
scale_group.append(indicator_group)
display.show(scale_group)

plot_needles(0, 0)

if has_sd_card:
    flash_status("SD CARD FOUND", 0.5)
else:
    flash_status("NO SD CARD", 0.5)

# Instantiate and calibrate load cell inputs
print("*** Instantiate and calibrate load cells")
print(" enable NAU7802 digital and analog power: %5s" % (nau7802.enable(True)))

nau7802.gain = default.PGA_GAIN  # Use default gain
nau7802.channel = 1  # Set to second channel
chan_1_zero = chan_2_zero = 0
if not debug:
    chan_1_zero = zero_channel()  # Re-calibrate and get raw zero offset value
nau7802.channel = 2  # Set to first channel
if not debug:
    chan_2_zero = zero_channel()  # Re-calibrate and get raw zero offset value

tare_1_mass_gr = round(config.TARE_1_MASS_GR, 1)
tare_2_mass_gr = round(config.TARE_2_MASS_GR, 1)
alarm_1_mass_gr = round(config.ALARM_1_MASS_GR, 1)
alarm_2_mass_gr = round(config.ALARM_2_MASS_GR, 1)

if tare_1_mass_gr != 0:
    tare_1_enable = True
    tare_1_value.color = color.ORANGE
    tare_1_icon[0] = 1
else:
    tare_1_enable = False
    tare_1_value.color = color.GRAY
    tare_1_mass_gr = 0.0
    tare_1_icon[0] = 3
tare_1_value.text = str(tare_1_mass_gr)

if tare_2_mass_gr != 0:
    tare_2_enable = True
    tare_2_value.color = color.GREEN
    tare_2_icon[0] = 5
else:
    tare_2_enable = False
    tare_2_value.color = color.GRAY
    tare_2_mass_gr = 0.0
    tare_2_icon[0] = 7
tare_2_value.text = str(tare_2_mass_gr)

if alarm_1_mass_gr != 0:
    alarm_1_enable = True
    alarm_1_value.color = color.ORANGE
    alarm_1_icon[0] = 0
else:
    alarm_1_enable = False
    alarm_1_value.color = color.GRAY
    alarm_1_mass_gr = 0.0
    alarm_1_icon[0] = 2
alarm_1_value.text = str(alarm_1_mass_gr)

if alarm_2_mass_gr != 0:
    alarm_2_enable = True
    alarm_2_value.color = color.GREEN
    alarm_2_icon[0] = 4
else:
    alarm_2_enable = False
    alarm_2_value.color = color.GRAY
    alarm_2_mass_gr = 0.0
    alarm_2_icon[0] = 6
alarm_2_value.text = str(alarm_2_mass_gr)

take_screenshot()

flash_status("READY", 0.5)
play_tone("high")
play_tone("low")

# -- Main loop: Read sample, move bubble, and display values
while True:
    nau7802.channel = 1
    value = read()
    chan_1_mass_gr = (
        round((value - chan_1_zero) * default.CALIB_RATIO_1, 1) - tare_1_mass_gr
    )
    chan_1_mass_oz = round(chan_1_mass_gr * 0.03527, 2)
    if str(chan_1_mass_gr) == "-0.0":  # Filter -0.0 value
        chan_1_mass_gr = 0.0
    chan_1_value.text = "%5.1f" % (chan_1_mass_gr)

    nau7802.channel = 2
    value = read()
    chan_2_mass_gr = (
        round((value - chan_2_zero) * default.CALIB_RATIO_2, 1) - tare_2_mass_gr
    )
    chan_2_mass_oz = round(chan_2_mass_gr * 0.03527, 2)
    if str(chan_2_mass_gr) == "-0.0":  # Filter -0.0 value
        chan_2_mass_gr = 0.0
    chan_2_value.text = "%5.1f" % (chan_2_mass_gr)

    chan_1_mass_gr_norm = chan_1_mass_gr / config.MAX_GR
    chan_2_mass_gr_norm = chan_2_mass_gr / config.MAX_GR

    erase_needles()
    plot_needles(chan_1_mass_gr_norm, chan_2_mass_gr_norm)

    print("(%+5.1f, %+5.1f)" % (chan_1_mass_gr, chan_2_mass_gr))

    touch = ts.touch_point
    if touch:
        for button in buttons:
            if button.contains(touch):
                button.selected = True
                if button.name in ('zero_1', 'zero_2'):
                    # Zero and recalibrate channel
                    channel = int(button.name[5])
                    play_tone('high')
                    nau7802.channel = channel

                    if channel == 1:
                        chan_1_zero = zero_channel()
                    else:
                        chan_2_zero = zero_channel()

                    while ts.touch_point:
                        time.sleep(0.5)
                    play_tone('low')

                if button.name in ('tare_1', 'tare_2'):
                    # get tare value for channel
                    channel = int(button.name[5])
                    play_tone('high')
                    nau7802.channel = channel
                    value = read()

                    if channel == 1:
                        tare_1_enable = not tare_1_enable  # toggle tare 1 state
                        if tare_1_enable:
                            tare_1_icon[0] = 1
                            tare_1_mass_gr = round((value - chan_1_zero) * default.CALIB_RATIO_1, 1)
                            if str(tare_1_mass_gr) == '-0.0':  # Filter -0.0 value
                                tare_1_mass_gr = 0.0
                        else:
                            tare_1_icon[0] = 3
                    else:
                        tare_2_enable = not tare_2_enable  # toggle tare 2 state
                        if tare_2_enable:
                            tare_2_value.color = color.GREEN
                            tare_2_icon[0] = 5
                            tare_2_mass_gr = round((value - chan_2_zero) * default.CALIB_RATIO_1, 1)
                            if str(tare_2_mass_gr) == '-0.0':  # Filter -0.0 value
                                tare_2_mass_gr = 0.0
                        else:
                            tare_2_value.color = color.GRAY
                            tare_2_mass_gr = 0.0
                            tare_2_icon[0] = 7

                    while ts.touch_point:
                        time.sleep(0.5)
                    play_tone('low')

    zero_1_button.selected = False
    zero_2_button.selected = False
    tare_1_button.selected = False
    tare_2_button.selected = False
