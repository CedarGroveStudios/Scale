# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# cedargrove_scale.configuration.py  2022-08-25 v3.03  Cedar Grove Studios

import board
import busio
import digitalio
import displayio
from adafruit_bitmap_font import bitmap_font
from simpleio import tone
from scale_defaults import Defaults
import foamyguy_nvm_helper as nvm_helper


class Config:
    """Load cell measurement configuration."""

    SAMPLE_AVG = 100  # Number of samples to average per measurement
    PGA_GAIN = 128  # Default gain for internal PGA

    # Load cell calibration ratio
    CALIB_RATIO_1 = Defaults.LOADCELL_1_CALIBRATION
    CALIB_RATIO_2 = Defaults.LOADCELL_2_CALIBRATION


class Display:
    """Instantiate the display and touchscreen as specified by the DISPLAY_NAME
    string and the touchscreen zero-rotation CALIBRATION value in the Defaults
    class (scale_defaults.py). The Display class permits add-on displays to
    appear and act the same as built-in displays."""
    def __init__(self):
        pass

    if "DISPLAY" and "TOUCH" in dir(board):
        display_name = "built-in"
    else:
        display_name = Defaults.DISPLAY_NAME

    # Landscape orientation only for now. Would need to fix built-in
    # touchscreen instantiation if rotation is needed in the future.
    rotation = 0

    # Instantiate the screen
    print(f"* Instantiate the {display_name} display")
    if display_name in "built-in":
        import adafruit_touchscreen
        display = board.DISPLAY
        display.rotation = rotation
        display.brightness = Defaults.BRIGHTNESS

        # add rotation stuff here
        ts = adafruit_touchscreen.Touchscreen(
            board.TOUCH_XL,
            board.TOUCH_XR,
            board.TOUCH_YD,
            board.TOUCH_YU,
            calibration=Defaults.CALIBRATION,
            size=(display.width, display.height),
        )

    elif display_name in 'TFT FeatherWing - 2.4" 320x240 Touchscreen':
        import adafruit_ili9341
        import adafruit_stmpe610
        displayio.release_displays()  # Release display resources
        display_bus = displayio.FourWire(board.SPI(), command=board.D10, chip_select=board.D9, reset=None)
        display = adafruit_ili9341.ILI9341(display_bus, width=320, height=240)
        display.rotation = rotation
        ts_cs = digitalio.DigitalInOut(board.D6)
        ts = adafruit_stmpe610.Adafruit_STMPE610_SPI(board.SPI(), ts_cs,
            calibration=Defaults.CALIBRATION, size=(display.width, display.height),
            disp_rotation=rotation, touch_flip=(False, False))

    elif display_name in 'TFT FeatherWing - 3.5" 480x320 Touchscreen':
        import adafruit_hx8357
        import adafruit_stmpe610
        displayio.release_displays()  # Release display resources
        display_bus = displayio.FourWire(board.SPI(), command=board.D10, chip_select=board.D9, reset=None)
        display = adafruit_hx8357.HX8357(display_bus, width=480, height=320)
        display.rotation = rotation
        ts_cs = digitalio.DigitalInOut(board.D6)
        ts = adafruit_stmpe610.Adafruit_STMPE610_SPI(board.SPI(), ts_cs,
            calibration=Defaults.CALIBRATION, size=(display.width, display.height),
            disp_rotation=rotation, touch_flip=(False, True))
    else:
        print(f"*** ERROR: display {display_name} not defined")

    if display.width < 330:
        FONT_0 = bitmap_font.load_font("/fonts/Helvetica-Bold-24.bdf")
        FONT_1 = bitmap_font.load_font("/fonts/OpenSans-9.bdf")
    else:
        FONT_0 = bitmap_font.load_font("/fonts/Helvetica-Bold-36.bdf")
        FONT_1 = bitmap_font.load_font("/fonts/OpenSans-16.bdf")

    # Determine display and object sizes
    width = display.width
    height = display.height
    center = (width // 2, height // 2)
    size = (display.width, display.height)
    rotation = display.rotation

    @property
    def brightness(self):
        try:
            level = self.display.brightness
        except:
            level = 1.0
        return level

    @brightness.setter
    def brightness(self, level):
        try:
            self.display.brightness = level
        except:
            print("** WARNING: Display brightness not adjustable")


    def show(self, group):
        Display.display.show(group)
        return


    def screen_to_rect(self, width_factor=0, height_factor=0):
        """Convert normalized screen position input (0.0 to 1.0) to the display's
        rectangular pixel position."""
        return int(self.width * width_factor), int(self.height * height_factor)


def play_tone(note=None, count=1):
    for i in range(0, count):
        if note == "high":
            tone(board.A0, 880, 0.1)
        elif note == "low":
            tone(board.A0, 440, 0.1)
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


class NVM:
    """Store settings in nonvolatile memory (NVM)."""

    def __init__(self):
        pass

    def write_settings(self, list=[None, None, None, None, False, False, False, False]):
        """Write settings data to NVM.
        Order of values and enables is alarm_1, alarm_2, tare_1, tare_2."""
        list.insert(0, "")
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
            print("** WARNING: NVM not supported on microprocessor")
            print("   Settings will not be stored")
            nvm_data = "x"

        if nvm_data[0] == "":  # If settings valid, first entry in list should be ''
            print("  settings data FOUND")
            return nvm_data[1:]
        else:
            print("** WARNING: settings data NOT FOUND")
            self.restore_defaults()
        return nvm_helper.read_data()[1:]
