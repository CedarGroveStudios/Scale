# Scale -- dual channel version
# Cedar Grove NAU7802 FeatherWing
# scale_code.py  2022-01-28 v3.028  Cedar Grove Studios

# uncomment the following import line to run the calibration method
# (this may eventually become part of a built-in setup process)
# import cedargrove_scale.load_cell_calibrator

import board
import displayio
import gc
import time
from cedargrove_nau7802 import NAU7802
from cedargrove_fake_nau7802 import FakeNAU7802
import cedargrove_scale.graphics
import cedargrove_scale.buttons
from cedargrove_scale.configuration import play_tone
from cedargrove_scale.configuration import Config, Colors, Display, NVM
import cedargrove_widgets.scale
from scale_defaults import Defaults

gc.collect()

DEBUG = False  # True: display button outlines

# Instantiate display groups and graphics
display = Display()
scale_group = displayio.Group()

if display.size[0] < 330:
    dial_size=0.40
else:
    dial_size=0.52
dial = cedargrove_widgets.scale.Scale(num_hands=2, max_scale=100,
    center=(0.5,0.55), size=dial_size, display_size=display.size)

labels = cedargrove_scale.graphics.Labels(display=display)
panel = cedargrove_scale.buttons.ScaleButtons(touchscreen = display.ts, timeout=1.0, debug=DEBUG)

"""display.brightness = Defaults.BRIGHTNESS
display.rotation = 0)  # CONFIGURATION NEEDS SETTER/GETTER"""

# Instantiate Non-Volatile-Memory
nvm = NVM()

# Instantiate load cell ADC FeatherWing or fake if FeatherWing not found
try:
    nau7802 = NAU7802(board.I2C(), address=0x2A, active_channels=2)
    print("* NAU7802 FeatherWing FOUND")
except:
    nau7802 = FakeNAU7802(board.I2C(), address=0x2A, active_channels=2)
    print("*** NAU7802 FeatherWing NOT FOUND; random data will be displayed")


def read_settings():
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
    zero_offset = read(100)  # Average 100 samples to establish zero offset value
    print(" channel zeroed")
    labels.status_label.text = " "
    return zero_offset


def read(samples=Config.SAMPLE_AVG):
    """Read and average consecutive raw sample values for currently selected
    channel. Returns the average raw value."""
    sum = 0
    for i in range(0, samples):
        if nau7802.available:
            sum = sum + nau7802.read()
    return int(sum / samples)


def plot_tares():
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

nau7802.gain = Config.PGA_GAIN  # Use default gain
nau7802.channel = 1  # Set to second channel
chan_1_zero = chan_2_zero = 0
if not DEBUG:
    chan_1_zero = zero_channel()  # Re-calibrate and get raw zero offset value
nau7802.channel = 2  # Set to first channel
if not DEBUG:
    chan_2_zero = zero_channel()  # Re-calibrate and get raw zero offset value

# Get default or stored alarm and tare values
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
    t0 = time.monotonic()
    labels.heartbeat(None)  # Blank heartbeat indicator

    plot_tares()
    plot_alarms()

    if not alarm:
        labels.status_label.text = Defaults.NAME
        labels.status_label.color = Colors.CYAN

    nau7802.channel = 1
    value = read()
    if tare_1_enable:
        tare = tare_1_mass_gr
    else:
        tare = 0
    chan_1_mass_gr = round((value - chan_1_zero) * Config.CALIB_RATIO_1, 1) - tare
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
    chan_2_mass_gr = round((value - chan_2_zero) * Config.CALIB_RATIO_2, 1) - tare
    chan_2_mass_oz = round(chan_2_mass_gr * 0.03527, 2)
    if str(chan_2_mass_gr) == "-0.0":  # Filter -0.0 value
        chan_2_mass_gr = 0.0
    labels.chan_2_value.text = "%5.1f" % (chan_2_mass_gr)

    chan_1_mass_gr_norm = chan_1_mass_gr / Defaults.MAX_GR
    chan_2_mass_gr_norm = chan_2_mass_gr / Defaults.MAX_GR
    dial.hand1 = chan_1_mass_gr_norm
    dial.hand2 = chan_2_mass_gr_norm

    print("(%+5.1f, %+5.1f)" % (chan_1_mass_gr, chan_2_mass_gr))

    labels.heartbeat(0)  # Maroon heartbeat indicator

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
            chan_1_zero = zero_channel()
        else:
            chan_2_zero = zero_channel()

    if button_pressed in ("tare_1", "tare_2"):
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

    gc.collect()
    free_memory = gc.mem_free()
    frame = time.monotonic() - t0
    print(f"frame: {frame:5.2f} sec   free memory: {free_memory} bytes")
