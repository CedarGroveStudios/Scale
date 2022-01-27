# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# cedargrove_scale.configuration.py  2022-01-27 v3.027  Cedar Grove Studios

import board
import busio
import digitalio
import displayio
import storage
from math import cos, sin, pi
import adafruit_sdcard
from adafruit_bitmap_font import bitmap_font
from adafruit_bitmapsaver import save_pixels
from simpleio import tone
import foamyguy_nvm_helper as nvm_helper

class NVM:
    """Store settings in nonvolatile memory (NVM)."""
    def __init__(self):
        pass

    def write_settings(self, list=[None, None, None, None, False, False, False, False]):
        """Write settings data to NVM.
        Order of values and enables is alarm_1, alarm_2, tare_1, tare_2."""
        list.insert(0, '')
        nvm_helper.save_data(list, test_run=False, verbose=False)
        return True

    def restore_defaults(self):
        """Clear NVM settings data."""
        from scale_defaults import Defaults
        print("  restore default settings")
        settings = [
            Defaults.ALARM_1_MASS_GR,
            Defaults.ALARM_2_MASS_GR,
            Defaults.TARE_1_MASS_GR,
            Defaults.TARE_2_MASS_GR,
            Defaults.ALARM_1_ENABLE,
            Defaults.ALARM_2_ENABLE,
            Defaults.TARE_1_ENABLE,
            Defaults.TARE_2_ENABLE,
        ]
        self.write_settings(list=settings)
        return True

    def fetch_settings(self):
        """Fetch alarm and tare settings data from NVM. If empty, provide
        the scale_defaults values."""
        try:
            nvm_data = nvm_helper.read_data()
        except:
            print("  NVM not supported on microprocessor")
            nvm_data = "x"

        if nvm_data[0] == '':  # If settings valid, first entry in list should be ''
            print("  settings data FOUND")
            return nvm_data[1:]
        else:
            print("  settings data NOT FOUND")
            self.restore_defaults()
        return nvm_helper.read_data()[1:]


class SDCard:
    def __init__(self):
        """Instantiate and test for PyPortal SD card."""
        self._spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        self._sd_cs = digitalio.DigitalInOut(board.SD_CS)
        self._has_card = False
        try:
            self._sdcard = adafruit_sdcard.SDCard(self._spi, self._sd_cs)
            self._vfs = storage.VfsFat(self._sdcard)
            storage.mount(self._vfs, "/sd")
            print("SD card FOUND")
            self._has_card = True
        except OSError as error:
            print("SD card NOT FOUND: ", error)

    @property
    def has_card(self):
        """True if SD card inserted."""
        return self._has_card

    def screenshot(self):
        if self._has_card:
            print("* Taking Screenshot...", end="")
            save_pixels("/sd/scale_screenshot.bmp")
            print(" STORED")
        else:
            print("* SCREENSHOT: NO SD CARD")


class Config:
    """Load cell measurement configuration."""
    SAMPLE_AVG = 100  # Number of samples to average per measurement

    PGA_GAIN = 128  # Default gain for internal PGA

    # Load cell calibration ratio; ADC_raw_measurement
    # Obtained emperically; individual load cell dependent
    _CHAN_1_RAW_VALUE = 215300  # 100g at gain x128 for load cell serial#4540-01
    _CHAN_1_TEST_MASS_GR = 100

    _CHAN_2_RAW_VALUE = 215300  # 100g at gain x128 for load cell serial#4540-02
    _CHAN_2_TEST_MASS_GR = 100

    CALIB_RATIO_1 = _CHAN_1_TEST_MASS_GR / _CHAN_1_RAW_VALUE
    CALIB_RATIO_2 = _CHAN_2_TEST_MASS_GR / _CHAN_2_RAW_VALUE


class Display:
    """Detect display and touchscreen. Appear as built-in display."""

    # TEST FOR BUILT-IN DISPLAY AND TOUCHSCREEN VIA BOARD
    # USE DICTIONARY FOR OTHER DISPLAY/TOUCHSCREEN COMBINATIONS

    from adafruit_hx8357 import HX8357
    #from adafruit_ili9341 import ILI9341
    import adafruit_stmpe610

    # Previously measured raw zero-rotation touchscreen calibration tuple.
    CALIBRATION = ((357, 3812), (390, 3555))

    # Release any resources currently in use for the displays
    displayio.release_displays()

    # Define the display's SPI bus connection
    disp_bus = displayio.FourWire(board.SPI(), command=board.D10,
        chip_select=board.D9, reset=None)

    """# Instantiate the 2.4" 320x240 TFT FeatherWing (#3315).
    display = ILI9341(disp_bus, width=320, height=240)
    _touch_flip = (False, False)"""

    # Instantiate the 3.5" 480x320 TFT FeatherWing (#3651).
    display = HX8357(disp_bus, width=480, height=320)
    _touch_flip = (False, True)

    # Instantiate touchscreen.
    ts_cs = digitalio.DigitalInOut(board.D6)
    # Update the raw calibration tuple with previously measured values.
    ts = adafruit_stmpe610.Adafruit_STMPE610_SPI(
        board.SPI(),
        ts_cs,
        calibration=CALIBRATION,
        size=(display.width, display.height),
        disp_rotation=display.rotation,
        touch_flip=_touch_flip,
    )

    # Determine display and object sizes
    width = display.width
    height = display.height
    center = (width // 2, height // 2)
    size = (display.width, display.height)
    try:
        brightness = display.brightness
    except:
        brightness = 1.0
    rotation = display.rotation

    if display.height < 300:
        FONT_0 = bitmap_font.load_font("/fonts/Helvetica-Bold-24.bdf")
        FONT_1 = bitmap_font.load_font("/fonts/OpenSans-9.bdf")
    else:
        FONT_0 = bitmap_font.load_font("/fonts/Helvetica-Bold-36.bdf")
        FONT_1 = bitmap_font.load_font("/fonts/OpenSans-16.bdf")

    def show(group):
        Display.display.show(group)
        return


class Colors:
    # Define a few colors (https://en.wikipedia.org/wiki/Web_colors)
    BLACK = 0x000000
    CYAN = 0x00FFFF
    BLUE = 0x0000FF
    BLUE_DK = 0x000080
    GRAY = 0x508080
    GREEN = 0x00FF00
    MAROON = 0x800000
    ORANGE = 0xFFA500
    PURPLE = 0x800080
    RED = 0xFF0000
    RED_DK = 0xA00000
    YELLOW = 0xFFFF00
    YELLOW_DK = 0x202000
    WHITE = 0xFFFFFF


def play_tone(note=None, count=1):
    for i in range(0, count):
        if note == "high":
            tone(board.A0, 880, 0.1)
        elif note == "low":
            tone(board.A0, 440, 0.1)
    return


def screen_to_rect(width_factor=0, height_factor=0):
    """Convert normalized screen position input (0.0 to 1.0) to the display's
    rectangular pixel position."""
    return int(Display.width * width_factor), int(Display.height * height_factor)


def dial_to_rect(scale_factor, center=Display.center, radius=0.25):
    """Convert normalized scale_factor input (-1.0 to 1.0) to a rectangular pixel
    position on the circumference of a circle with center (x,y pixels) and
    radius (pixels)."""
    radians = (-2 * pi) * (scale_factor)  # convert scale_factor to radians
    radians = radians + (pi / 2)  # rotate axis counterclockwise
    x = int(center[0] + (cos(radians) * radius))
    y = int(center[1] - (sin(radians) * radius))
    return x, y
