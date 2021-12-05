# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# cedargrove_scale/configuration.py
# 2021-12-05 v1.2

import board
import busio
import digitalio
import storage
from math import cos, sin, pi
import adafruit_sdcard
from adafruit_bitmapsaver import save_pixels
from simpleio import tone


class SDCard:
    def __init__(self):
        """Instantiate and test for PyPortal SD card."""
        self._spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
        self._sd_cs = digitalio.DigitalInOut(board.SD_CS)
        self._has_card = False
        try:
            self._sdcard = adafruit_sdcard.SDCard(self._spi, self._sd_cs)
            self._vfs = storage.VfsFat(self._sdcard)
            storage.mount(self._vfs, '/sd')
            print('SD card FOUND')
            self._has_card = True
        except OSError as error:
            print('SD card NOT FOUND: ', error)

    @property
    def has_card(self):
        """True if SD card inserted."""
        return self._has_card

    def screenshot(self):
        if self._has_card:
            print('* Taking Screenshot...', end='')
            save_pixels('/sd/scale_screenshot.bmp')
            print(' STORED')
        else:
            print('* SCREENSHOT: NO SD CARD')

    def read_alarm_tare(self):
        """Read alarm and tare settings file from SD card. If SD card or
        file not found, provide the scale_defaults values."""
        if self._has_card:
            try:
                import sd.alarm_tare.py as settings
                print('  /sd/alarm_tare settings file FOUND')
                return settings.alarm_tare
            except:
                print('  /sd/alarm_tare settings file NOT FOUND')
        from scale_defaults import Defaults
        print('  using scale_defaults for alarm_tare settings')
        return (Defaults.ALARM_1_MASS_GR, Defaults.ALARM_2_MASS_GR, Defaults.TARE_1_MASS_GR, Defaults.TARE_2_MASS_GR)

    def write_alarm_tare(self, list=(None, None, None, None)):
        """Write configuration text file to SD card. List of values contains
        alarm_1, alarm_2, tare_1, tare_2."""
        if self._has_card:
            data_record = f'alarm_tare = {list}  # alarm_1, alarm_2, tare_1, tare_2'
            log_file = open('/sd/alarm_tare.py', 'w')
            log_file.write(data_record)
            log_file.close()
            return True
        return False


class Config:
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


class Screen:
    # Determine display and object sizes
    WIDTH = board.DISPLAY.width
    HEIGHT = board.DISPLAY.height
    CENTER = (WIDTH // 2, HEIGHT // 2)


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


def play_tone(note=None):
    if note == 'high':
        tone(board.A0, 880, 0.1)
    elif note == 'low':
        tone(board.A0, 440, 0.1)
    return


def screen_to_rect(width_factor=0, height_factor=0):
    """Convert normalized screen position input (0.0 to 1.0) to the display's
    rectangular pixel position."""
    return int(Screen.WIDTH * width_factor), int(Screen.HEIGHT * height_factor)


def dial_to_rect(scale_factor, center=Screen.CENTER, radius=0.25):
    """Convert normalized scale_factor input (-1.0 to 1.0) to a rectangular pixel
    position on the circumference of a circle with center (x,y pixels) and
    radius (pixels)."""
    radians = (-2 * pi) * (scale_factor)  # convert scale_factor to radians
    radians = radians + (pi / 2)  # rotate axis counterclockwise
    x = int(center[0] + (cos(radians) * radius))
    y = int(center[1] - (sin(radians) * radius))
    return x, y
