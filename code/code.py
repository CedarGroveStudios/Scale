# PyPortal Scale -- dual channel version
# Cedar Grove NAU7802 FeatherWing
# 2021-10-15 v21 Cedar Grove Studios

# uncomment the following import line to run the calibration method
# (this will eventually be put into the setup process)
# import cedargrove_scale.load_cell_calibrator

import board
import time
import displayio
from simpleio import tone
from adafruit_bitmapsaver import save_pixels
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.triangle import Triangle

from cedargrove_scale.buttons_pyportal import ScaleButtons
from cedargrove_nau7802 import NAU7802

from cedargrove_scale.configuration import play_tone, dial_to_rect, screen_to_rect
from cedargrove_scale.configuration import (
    Configuration as config,
    Palette as color,
    Screen as screen,
    SDcard as sd,
)
from cedargrove_scale.display_graphics import Case, Dial, Labels, Plate
from scale_defaults import Defaults as default

debug = False

panel = ScaleButtons(timeout=0.5, debug=debug)
dial = Dial(debug=debug)
labels = Labels(debug=debug)
case = Case(debug=debug)
plate = Plate(debug=debug)

# Instantiate load sensor ADC wing
nau7802 = NAU7802(board.I2C(), address=0x2A, active_channels=2)


def zero_channel():
    """Initiate internal calibration for current channel, return raw zero
    offset value. Use when scale is started, a new channel is selected, or
    to adjust for measurement drift. Remove weight and tare from load cell
    before executing."""
    labels.status_label.text = " "
    labels.status_label.text = "ZERO LOAD CELL " + str(nau7802.channel)
    labels.status_label.color = color.YELLOW
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
    labels.status_label.text = " "
    return zero_offset


def read(samples=config.SAMPLE_AVG):
    """Read and average consecutive raw sample values for currently selected
    channel. Returns the average raw value."""
    sum = 0
    for i in range(0, samples):
        if nau7802.available:
            sum = sum + nau7802.read()
    return int(sum / samples)


def flash_status(text="", duration=0.05):
    """Flash a status message once."""
    labels.status_label.text = " "
    labels.status_label.text = text
    labels.status_label.color = color.YELLOW
    time.sleep(duration)
    labels.status_label.color = color.BLACK
    time.sleep(duration)
    labels.status_label.text = " "
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
    plate.plate.y = int(sy0 + (sy1 * min(2, max(-2, (scale_1 + scale_2)))))
    plate.riser.y = plate.plate.y

    x0, y0 = dial_to_rect(scale_2, radius=dial.RADIUS)
    x1, y1 = dial_to_rect(scale_2 - 0.25, radius=base // 2)
    x2, y2 = dial_to_rect(scale_2 + 0.25, radius=base // 2)
    hand_2 = Triangle(x0, y0, x1, y1, x2, y2, fill=color.GREEN, outline=hand_2_outline)
    needles_group.append(hand_2)

    x0, y0 = dial_to_rect(scale_1, radius=dial.RADIUS)
    x1, y1 = dial_to_rect(scale_1 - 0.25, radius=base // 2)
    x2, y2 = dial_to_rect(scale_1 + 0.25, radius=base // 2)
    hand_1 = Triangle(x0, y0, x1, y1, x2, y2, fill=color.ORANGE, outline=hand_1_outline)
    needles_group.append(hand_1)

    x0, y0 = screen_to_rect(dial.center[0], dial.center[1])
    pivot = Circle(x0, y0, base // 2, fill=color.WHITE)
    needles_group.append(pivot)

    return scale_1, scale_2


def erase_needles():
    needles_group.remove(needles_group[len(needles_group) - 1])
    needles_group.remove(needles_group[len(needles_group) - 1])
    needles_group.remove(needles_group[len(needles_group) - 1])
    return


def plot_tares():
    if tare_1_enable:
        labels.tare_1_value.color = color.ORANGE
        panel.tare_1_icon[0] = 1
    else:
        labels.tare_1_value.color = color.GRAY
        panel.tare_1_icon[0] = 3

    if tare_2_enable:
        labels.tare_2_value.color = color.GREEN
        panel.tare_2_icon[0] = 5
    else:
        labels.tare_2_value.color = color.GRAY
        panel.tare_2_icon[0] = 7
    return


def plot_alarms():
    if alarm_1_enable:
        dial.chan_1_alarm.x0, dial.chan_1_alarm.y0 = dial_to_rect(
            alarm_1_mass_gr / default.MAX_GR, radius=dial.RADIUS
        )
        labels.alarm_1_value.color = color.ORANGE
        panel.alarm_1_icon[0] = 0
    else:
        dial.chan_1_alarm.x0, dial.chan_1_alarm.y0 = (-50, -50)  # Make dot disappear
        labels.alarm_1_value.color = color.GRAY
        panel.alarm_1_icon[0] = 2

    if alarm_2_enable:
        dial.chan_2_alarm.x0, dial.chan_2_alarm.y0 = dial_to_rect(
            alarm_2_mass_gr / default.MAX_GR, radius=dial.RADIUS
        )
        labels.alarm_2_value.color = color.GREEN
        panel.alarm_2_icon[0] = 4
    else:
        dial.chan_2_alarm.x0, dial.chan_2_alarm.y0 = (-50, -50)  # Make dot disappear
        labels.alarm_2_value.color = color.GRAY
        panel.alarm_2_icon[0] = 6
    return


# Instantiate display and fonts
# print('*** Instantiate the display and fonts')
display = board.DISPLAY
display.brightness = default.BRIGHTNESS
scale_group = displayio.Group()

# Define displayio background and group elements
print("*** Define displayio background and group elements")

"""# Bitmap background -- FUTURE FEATURE?
_bkg = displayio.OnDiskBitmap("/sd/background.bmp")
background = displayio.TileGrid(_bkg, pixel_shader=displayio.ColorConverter(), x=0, y=0)
scale_group.append(background)"""

# -- DISPLAY ELEMENTS -- #
scale_group.append(panel.button_display_group)
scale_group.append(labels.display_group)
scale_group.append(plate.display_group)
scale_group.append(case.display_group)
scale_group.append(dial.display_group)

# Create group for needle indicators
needles_group = displayio.Group()
scale_group.append(needles_group)

display.show(scale_group)

if sd.has_card:
    flash_status("SD CARD FOUND", 0.5)
else:
    flash_status("NO SD CARD", 0.5)

# Instantiate and calibrate load cell inputs
print("*** Instantiate and calibrate load cells")
print(" enable NAU7802 digital and analog power: %5s" % (nau7802.enable(True)))

nau7802.gain = config.PGA_GAIN  # Use default gain
nau7802.channel = 1  # Set to second channel
chan_1_zero = chan_2_zero = 0
if not debug:
    chan_1_zero = zero_channel()  # Re-calibrate and get raw zero offset value
nau7802.channel = 2  # Set to first channel
if not debug:
    chan_2_zero = zero_channel()  # Re-calibrate and get raw zero offset value

tare_1_mass_gr = round(default.TARE_1_MASS_GR, 1)
labels.tare_1_value.text = str(tare_1_mass_gr)
tare_1_enable = default.TARE_1_ENABLE
tare_2_mass_gr = round(default.TARE_2_MASS_GR, 1)
labels.tare_2_value.text = str(tare_2_mass_gr)
tare_2_enable = default.TARE_2_ENABLE
alarm_1_mass_gr = round(default.ALARM_1_MASS_GR, 1)
labels.alarm_1_value.text = str(alarm_1_mass_gr)
alarm_1_enable = default.ALARM_1_ENABLE
alarm_2_mass_gr = round(default.ALARM_2_MASS_GR, 1)
labels.alarm_2_value.text = str(alarm_2_mass_gr)
alarm_2_enable = default.ALARM_2_ENABLE
alarm = False

plot_needles()
plot_tares()
plot_alarms()

if sd.has_card:
    print("Taking Screenshot...", end="")
    flash_status("SCREENSHOT...", 0.8)
    labels.status_label.text = default.NAME
    labels.status_label.color = color.CYAN
    save_pixels("/sd/screenshot.bmp")
    print(" Screenshot stored")
    flash_status("... STORED", 0.8)
else:
    flash_status("SCREENSHOT: NO SD CARD", 1.0)

flash_status("READY", 0.5)
play_tone("high")
play_tone("low")

# -- Main loop: Read sample, move bubble, and display values
while True:
    if not alarm:
        labels.status_label.text = default.NAME
        labels.status_label.color = color.CYAN

    nau7802.channel = 1
    value = read()
    if tare_1_enable:
        tare = tare_1_mass_gr
    else:
        tare = 0
    chan_1_mass_gr = round((value - chan_1_zero) * config.CALIB_RATIO_1, 1) - tare
    chan_1_mass_oz = round(chan_1_mass_gr * 0.03527, 2)
    if str(chan_1_mass_gr) == "-0.0":  # Filter -0.0 value
        chan_1_mass_gr = 0.0
    labels.chan_1_value.text = "%5.1f" % (chan_1_mass_gr)

    nau7802.channel = 2
    value = read()
    if tare_2_enable:
        tare = tare_2_mass_gr
    else:
        tare = 0
    chan_2_mass_gr = round((value - chan_2_zero) * config.CALIB_RATIO_2, 1) - tare
    chan_2_mass_oz = round(chan_2_mass_gr * 0.03527, 2)
    if str(chan_2_mass_gr) == "-0.0":  # Filter -0.0 value
        chan_2_mass_gr = 0.0
    labels.chan_2_value.text = "%5.1f" % (chan_2_mass_gr)

    chan_1_mass_gr_norm = chan_1_mass_gr / default.MAX_GR
    chan_2_mass_gr_norm = chan_2_mass_gr / default.MAX_GR

    erase_needles()
    plot_needles(chan_1_mass_gr_norm, chan_2_mass_gr_norm)

    print("(%+5.1f, %+5.1f)" % (chan_1_mass_gr, chan_2_mass_gr))

    a1 = a2 = False
    if alarm_1_enable and chan_1_mass_gr >= alarm_1_mass_gr:
        a1 = True
        play_tone("low")
        dial.chan_1_alarm.fill = labels.status_label.color = color.RED
    else:
        dial.chan_1_alarm.fill = color.ORANGE

    if alarm_2_enable and chan_2_mass_gr >= default.ALARM_2_MASS_GR:
        a2 = True
        play_tone("high")
        dial.chan_2_alarm.fill = labels.status_label.color = color.RED
    else:
        dial.chan_2_alarm.fill = color.GREEN

    if a1 and a2:
        labels.status_label.text = (
            "ALARM: " + default.CHAN_1_NAME + " and " + default.CHAN_2_NAME
        ).upper()
        # labels.status_label.color = color.RED
    elif a1:
        labels.status_label.text = ("ALARM: " + default.CHAN_1_NAME).upper()
        # labels.status_label.color = color.RED
    elif a2:
        labels.status_label.text = ("ALARM: " + default.CHAN_2_NAME).upper()
        # labels.status_label.color = color.RED
    alarm = a1 or a2

    button_pressed, hold_time = panel.read_buttons()
    if button_pressed in ("zero_1", "zero_2"):
        # Zero and recalibrate channel
        channel = int(button_pressed[5])
        play_tone("high")
        nau7802.channel = channel

        if channel == 1:
            chan_1_zero = zero_channel()
        else:
            chan_2_zero = zero_channel()

    if button_pressed in ("tare_1", "tare_2"):
        # Enable/disable tares
        channel = int(button_pressed[5])
        play_tone("high")
        nau7802.channel = channel

        if channel == 1:
            tare_1_enable = not tare_1_enable  # toggle tare 1 state
            if tare_1_enable:
                # flash_status('TARE 1 ENABLE', 0.5)
                if str(tare_1_mass_gr) == "-0.0":  # Filter -0.0 value
                    tare_1_mass_gr = 0.0
                labels.tare_1_value.color = color.ORANGE
                panel.tare_1_icon[0] = 1
            else:
                # flash_status('TARE 1 DISABLE', 0.5)
                labels.tare_1_value.color = color.GRAY
                panel.tare_2_icon[0] = 3
        else:
            tare_2_enable = not tare_2_enable  # toggle tare 2 state
            if tare_2_enable:
                # flash_status('TARE 2 ENABLE', 0.5)
                if str(tare_2_mass_gr) == "-0.0":  # Filter -0.0 value
                    tare_2_mass_gr = 0.0
                labels.tare_1_value.color = color.ORANGE
                panel.tare_1_icon[0] = 5
            else:
                # flash_status('TARE 2 DISABLE', 0.5)
                labels.tare_2_value.color = color.GRAY
                panel.tare_2_icon[0] = 7
        plot_tares()

    if button_pressed in ("alarm_1", "alarm_2"):
        # Enable/disable alarms
        channel = int(button_pressed[6])
        play_tone("high")

        if channel == 1:
            alarm_1_enable = not alarm_1_enable  # toggle alarm 1 state
            if alarm_1_enable:
                # flash_status('ALARM 1 ENABLE', 0.5)
                labels.alarm_1_value.color = color.ORANGE
                panel.alarm_1_icon[0] = 0
            else:
                # flash_status('ALARM 1 DISABLE', 0.5)
                labels.alarm_1_value.color = color.GRAY
                panel.alarm_1_icon[0] = 2
        else:
            alarm_2_enable = not alarm_2_enable  # toggle alarm 1 state
            if alarm_2_enable:
                # flash_status('ALARM 2 ENABLE', 0.5)
                labels.alarm_2_value.color = color.GREEN
                panel.alarm_2_icon[0] = 4
            else:
                # flash_status('ALARM 2 DISABLE', 0.5)
                labels.alarm_2_value.color = color.GRAY
                panel.alarm_2_icon[0] = 6
        plot_alarms()

    """if button.name in ('setup_1', 'setup_2'):
        # Initiate the setup process for a channel
        channel = int(button.name[6])
        play_tone('high')

        if channel == 1:
            flash_status('SETUP 1', 0.5)
            pass
        else:
            flash_status('SETUP 2', 0.5)
            pass"""
