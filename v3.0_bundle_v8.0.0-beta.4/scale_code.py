# SPDX-FileCopyrightText: Copyright (c) 2022 Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`scale_code.py`
================================================================================

The primary code.py module for the dual-channel Scale project.
scale_code.py  2022-07-25 v3.3  Cedar Grove Studios

A configurable dual loadcell scale utilizing the CedarGrove NAU7802 FeatherWing.
Mass measurements from two loadcell sensors are processed by the CedarGrove
NAU7802 precision ADC FeatherWing and displayed graphically on an Adafruit
PyPortal, PyPortal Pynt, PyPortal Titano, or RP2040 Feather + TFT FeatherWing.
Each channel's display mass values within the range of the loadcell are
displayed in Grams, including negative values. Tare and alarm levels are
user-specified and selectively enabled as needed.

Default operational parameters are specified in the scale_defaults.py file in
the microcontroller's root directory. Scale’s graphics and touchscreen zones
are display size independent. Built-in board size is automatically detected;
other displays are user-specified in the scale_defaults.py file. Font sizes do
not scale proportionally but adjust somewhat to display size. Tare and alarm
settings are stored in the microcontroller's non-volatile memory (NVM) to be
recalled upon power-up. To facilitate testing, the code will simulate a missing
custom loadcell FeatherWing board.

* Author(s): JG for Cedar Grove Maker Studios

Implementation Notes
--------------------
**Hardware:**
* Cedar Grove NAU7802 Feather Wing

**Software and Dependencies:**

* Cedar Grove NAU7802 CircuitPython library:
  https://github.com/CedarGroveStudios/CircuitPython_NAU7802

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""

# imports__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/CedarGroveStudios/Scale"


import board
import displayio
import gc
import time
from cedargrove_nau7802 import NAU7802
from cedargrove_fake_nau7802 import FakeNAU7802
import cedargrove_scale.graphics
import cedargrove_scale.buttons
from cedargrove_scale.configuration import play_tone
from cedargrove_scale.configuration import LoadCellConfig, Colors, Display, NVM
import cedargrove_widgets.scale
from scale_defaults import Defaults

gc.collect()

DEBUG = False  # True: button outlines will display

# Instantiate display groups and graphics
display = Display()
scale_group = displayio.Group()

if display.size[0] < 320:
    dial_size = 0.40
else:
    dial_size = 0.52
dial = cedargrove_widgets.scale.Scale(
    num_hands=2,
    max_scale=100,
    center=(0.5, 0.55),
    size=dial_size,
    display_size=display.size,
)

# Incorporate scale labels and buttons classes
labels = cedargrove_scale.graphics.Labels(display=display)
panel = cedargrove_scale.buttons.ScaleButtons(
    touchscreen=display.ts, timeout=1.0, debug=DEBUG
)

display.brightness = Defaults.BRIGHTNESS

# Instantiate Non-Volatile-Memory (NVM) for storing tare and alarm parameters
nvm = NVM()

# Instantiate load cell ADC FeatherWing or fake if FeatherWing not found
try:
    nau7802 = NAU7802(board.I2C(), address=0x2A, active_channels=2)
    print("* NAU7802 FeatherWing FOUND")
except:
    nau7802 = FakeNAU7802(None, address=0x2A, active_channels=2)
    print("*** ERROR: NAU7802 FeatherWing NOT FOUND; random data will be displayed")


def read_settings():
    """Read settings from NVM."""
    global alarm_1_mass_gr, alarm_2_mass_gr, tare_1_mass_gr, tare_2_mass_gr, alarm_1_enable, alarm_2_enable, tare_1_enable, tare_2_enable

    settings = nvm.fetch_settings()

    alarm_1_mass_gr = round(settings[0], 1)
    labels.alarm_1_value.text = str(alarm_1_mass_gr)
    alarm_2_mass_gr = round(settings[1], 1)
    labels.alarm_2_value.text = str(alarm_2_mass_gr)
    tare_1_mass_gr = round(settings[2], 1)
    labels.tare_1_value.text = str(tare_1_mass_gr)
    tare_2_mass_gr = round(settings[3], 1)
    labels.tare_2_value.text = str(tare_2_mass_gr)

    alarm_1_enable = bool(settings[4])
    alarm_2_enable = bool(settings[5])
    tare_1_enable = bool(settings[6])
    tare_2_enable = bool(settings[7])
    return


def zero_channel():
    """Initiate internal calibration for currently enabled channel. Returns
    a raw zero offset value. Use when scale is started, a new channel is
    selected, or to adjust for measurement drift. NOTE: Remove weight and tare
    from load cell before executing."""
    labels.status_label.text = " "
    labels.status_label.text = "ZERO LOAD CELL " + str(nau7802.channel)
    labels.status_label.color = Colors.YELLOW
    print(
        "  channel %1d calibrate.INTERNAL: %5s"
        % (nau7802.channel, nau7802.calibrate("INTERNAL"))
    )
    print(
        "  channel %1d calibrate.OFFSET:   %5s ..."
        % (nau7802.channel, nau7802.calibrate("OFFSET")),
        end="",
    )
    print(" channel zeroed")
    labels.status_label.text = " "
    return


def read(samples=LoadCellConfig.SAMPLE_AVG):
    """Read and average consecutive raw sample values for currently selected
    channel. Returns the average raw value."""
    sample_sum = 0
    sample_count = samples
    while sample_count > 0:
        while not nau7802.available():
            pass
        sample_sum = sample_sum + nau7802.read()
        sample_count -= 1
    return int(sample_sum / samples)


def plot_tares():
    """Display the tare graphics."""
    if tare_1_enable:
        labels.tare_1_value.color = Colors.ORANGE
        panel.tare_1_icon[0] = 1
    else:
        labels.tare_1_value.color = Colors.GRAY
        panel.tare_1_icon[0] = 3

    if tare_2_enable:
        labels.tare_2_value.color = Colors.GREEN
        panel.tare_2_icon[0] = 5
    else:
        labels.tare_2_value.color = Colors.GRAY
        panel.tare_2_icon[0] = 7
    return


def plot_alarms():
    """Display the alarms graphics."""
    if alarm_1_enable:
        dial.alarm1 = alarm_1_mass_gr / Defaults.MAX_GR
        labels.alarm_1_value.color = Colors.ORANGE
        panel.alarm_1_icon[0] = 0
    else:
        dial.alarm1 = None
        labels.alarm_1_value.color = Colors.GRAY
        panel.alarm_1_icon[0] = 2

    if alarm_2_enable:
        dial.alarm2 = alarm_2_mass_gr / Defaults.MAX_GR
        labels.alarm_2_value.color = Colors.GREEN
        panel.alarm_2_icon[0] = 4
    else:
        dial.alarm2 = None
        labels.alarm_2_value.color = Colors.GRAY
        panel.alarm_2_icon[0] = 6
    return


# Define display background and displayio group elements
print("* Define display background and displayio group elements")

# -- DISPLAY ELEMENTS -- #
scale_group.append(panel)
scale_group.append(labels)
scale_group.append(dial)

# Zero the hand positions and activate the display
dial.hand1 = dial.hand2 = 0
display.show(scale_group)

# Instantiate and calibrate load cell inputs
print("* Instantiate and calibrate load cells")
print("  enable NAU7802 digital and analog power: %5s" % (nau7802.enable(True)))

nau7802.gain = LoadCellConfig.PGA_GAIN  # Use default gain
nau7802.channel = 1  # Set to first channel
if not DEBUG:
    zero_channel()  # Re-calibrate and zero
nau7802.channel = 2  # Set to second channel
if not DEBUG:
    zero_channel()  # Re-calibrate and zero

# Get default or stored alarm and tare values from NVM
print("* Read default or stored alarm and tare settings")
read_settings()
plot_tares()
plot_alarms()

alarm = False

print("*** READY ***")
labels.flash_status("READY", 0.5)
play_tone("high")
play_tone("low")

# -- Main loop: Read sample, move bubble, and display values
while True:
    t0 = time.monotonic()  # Initiate the display frame rate clock
    labels.heartbeat(None)  # Blank the heartbeat indicator

    plot_tares()
    plot_alarms()

    if not alarm:
        labels.status_label.text = Defaults.NAME
        labels.status_label.color = Colors.CYAN

    # Read channel 1 and update display
    nau7802.channel = 1
    value = read()
    if tare_1_enable:
        tare = tare_1_mass_gr
    else:
        tare = 0
    chan_1_mass_gr = round(value * LoadCellConfig.CALIB_RATIO_1, 1) - tare
    chan_1_mass_oz = round(chan_1_mass_gr * 0.03527, 2)
    if str(chan_1_mass_gr) == "-0.0":  # Filter -0.0 value
        chan_1_mass_gr = 0.0
    labels.chan_1_value.text = "%5.1f" % (chan_1_mass_gr)

    # Read channel 2 and update display
    nau7802.channel = 2
    value = read()
    if tare_2_enable:
        tare = tare_2_mass_gr
    else:
        tare = 0
    chan_2_mass_gr = round(value * LoadCellConfig.CALIB_RATIO_2, 1) - tare
    chan_2_mass_oz = round(chan_2_mass_gr * 0.03527, 2)
    if str(chan_2_mass_gr) == "-0.0":  # Filter -0.0 value
        chan_2_mass_gr = 0.0
    labels.chan_2_value.text = "%5.1f" % (chan_2_mass_gr)

    chan_1_mass_gr_norm = chan_1_mass_gr / Defaults.MAX_GR
    chan_2_mass_gr_norm = chan_2_mass_gr / Defaults.MAX_GR
    dial.hand1 = chan_1_mass_gr_norm
    dial.hand2 = chan_2_mass_gr_norm

    print("(%+5.1f, %+5.1f)" % (chan_1_mass_gr, chan_2_mass_gr))

    time.sleep(1)

    labels.heartbeat(0)  # Set heartbeat indicator to Maroon

    # Check alarms
    a1 = a2 = False
    if alarm_1_enable and chan_1_mass_gr >= alarm_1_mass_gr:
        a1 = True
        play_tone("low")
        labels.status_label.color = Colors.RED

    if alarm_2_enable and chan_2_mass_gr >= Defaults.ALARM_2_MASS_GR:
        a2 = True
        play_tone("high")
        labels.status_label.color = Colors.RED

    if a1 and a2:
        labels.status_label.text = (
            "ALARM: " + Defaults.CHAN_1_NAME + " and " + Defaults.CHAN_2_NAME
        ).upper()
        # labels.status_label.color = Colors.RED
    elif a1:
        labels.status_label.text = ("ALARM: " + Defaults.CHAN_1_NAME).upper()
        # labels.status_label.color = Colors.RED
    elif a2:
        labels.status_label.text = ("ALARM: " + Defaults.CHAN_2_NAME).upper()
        # labels.status_label.color = Colors.RED
    alarm = a1 or a2

    # Check touchscreen for button presses
    button_pressed, hold_time = panel.read_buttons()
    if button_pressed == "reset":
        if hold_time > panel.timeout:
            print("* RESTORE default settings")
            nvm.restore_defaults()
            read_settings()
            play_tone("low", 3)
            labels.flash_status("SETTINGS RESTORED", 1.0)

    if button_pressed in ("zero_1", "zero_2"):
        # Zero and recalibrate channel
        channel = int(button_pressed[5])
        play_tone("high")
        nau7802.channel = channel

        if channel == 1:
            zero_channel()
        else:
            zero_channel()

    if button_pressed in ("tare_1", "tare_2"):
        # Enable or disable tares; hold to set new tare value
        channel = int(button_pressed[5])
        play_tone("high")
        if hold_time <= panel.timeout:
            # Enable/disable tares
            nau7802.channel = channel

            if channel == 1:
                tare_1_enable = not tare_1_enable  # toggle tare 1 state
                if tare_1_enable:
                    # labels.flash_status('TARE 1 ENABLE', 0.5)
                    if str(tare_1_mass_gr) == "-0.0":  # Filter -0.0 value
                        tare_1_mass_gr = 0.0
            else:
                tare_2_enable = not tare_2_enable  # toggle tare 2 state
                if tare_2_enable:
                    # labels.flash_status('TARE 2 ENABLE', 0.5)
                    if str(tare_2_mass_gr) == "-0.0":  # Filter -0.0 value
                        tare_2_mass_gr = 0.0
            plot_tares()
        else:
            if channel == 1:
                tare_1_mass_gr = chan_1_mass_gr
                labels.tare_1_value.text = str(tare_1_mass_gr)
            if channel == 2:
                tare_2_mass_gr = chan_2_mass_gr
                labels.tare_2_value.text = str(tare_2_mass_gr)
            print("* Set tare", channel)

        # Store updated settings in NVM
        settings = [
            alarm_1_mass_gr,
            alarm_2_mass_gr,
            tare_1_mass_gr,
            tare_2_mass_gr,
            alarm_1_enable,
            alarm_2_enable,
            tare_1_enable,
            tare_2_enable,
        ]
        nvm.write_settings(list=settings)
        play_tone("high")
        labels.flash_status("STORED", 0.5)

    if button_pressed in ("alarm_1", "alarm_2"):
        # Enable/disable alarms
        channel = int(button_pressed[6])
        play_tone("high")
        if hold_time <= panel.timeout:
            if channel == 1:
                alarm_1_enable = not alarm_1_enable  # toggle alarm 1 state
            else:
                alarm_2_enable = not alarm_2_enable  # toggle alarm 1 state
            plot_alarms()
        else:
            if channel == 1:
                alarm_1_mass_gr = chan_1_mass_gr
                labels.alarm_1_value.text = str(alarm_1_mass_gr)
            if channel == 2:
                alarm_2_mass_gr = chan_2_mass_gr
                labels.alarm_2_value.text = str(alarm_2_mass_gr)
            print("* Set alarm", channel)

        # Store updated settings in NVM
        settings = [
            alarm_1_mass_gr,
            alarm_2_mass_gr,
            tare_1_mass_gr,
            tare_2_mass_gr,
            alarm_1_enable,
            alarm_2_enable,
            tare_1_enable,
            tare_2_enable,
        ]
        nvm.write_settings(list=settings)
        play_tone("high")
        labels.flash_status("STORED", 0.5)

    # End of display frame cleanup
    gc.collect()
    free_memory = gc.mem_free()
    frame = time.monotonic() - t0
    print(f"frame: {frame:5.2f} sec   free memory: {free_memory} bytes")
