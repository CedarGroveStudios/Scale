# SPDX-FileCopyrightText: Copyright (c) 2022 Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`graphics.py`
================================================================================

The Defaults class for the dual-channel Scale project.
scale_defaults.py  2022-08-25 v2.08  Cedar Grove Studios

A collection of initial scale parameters including project and channel names,
touchscreen and load cell calibration values, the display selection, tare and
alarm values, and the initial active state of the tares and alarms.

* Author(s): JG for Cedar Grove Maker Studios

Implementation Notes
--------------------
**Hardware:**

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases
"""

# imports__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/CedarGroveStudios/Scale"


class Defaults:

    NAME = "John's Espresso Bench"
    CHAN_1_NAME = "beans"  # 6 characters maximum
    CHAN_2_NAME = "shots"  # 6 characters maximum

    """Enter the calibration ratio for the individual load cell in-use. The
    ratio is composed of the reference weight in grams divided by the raw
    reading. For example, a raw reading of 215300 for a 100 gram weight results
    in a calibration ratio of 100 / 215300. Use the clue_scale_single_calibrate
    method to obtain the raw value.
    FYI: A US dime coin weighs 2.268 grams or 0.079 ounces."""

    LOADCELL_1_CALIBRATION = 100 / 215300  # channel 1 load cell serial#4540-01
    LOADCELL_2_CALIBRATION = 100 / 215300  # channel 2 load cell serial#4540-02

    """DISPLAY_NAME -- choose unique descriptor string from:
      TFT FeatherWing - 2.4" 320x240 Touchscreen
      TFT FeatherWing - 3.5" 480x320 Touchscreen
      built-in

    CALIBRATION -- use touchscreen's zero-degree rotational measurement"""

    DISPLAY_NAME = "built-in"
    CALIBRATION = ((8567, 58264), (9216, 55479))  # "built-in"; PyPortal Pynt
    # CALIBRATION = ((8567, 58264), (9216, 55479))  # "built-in"; PyPortal
    # CALIBRATION = ((8567, 58264), (9216, 55479))  # "built-in"; PyPortal Titano
    # CALIBRATION = ((357, 3812), (390, 3555))  # 2.4" FeatherWing touchscreen
    # CALIBRATION = ((357, 3812), (390, 3555))  # 3.5" FeatherWing touchscreen

    BRIGHTNESS = 0.75  # Display brightness, 0 to 1.0; 0.75 typical, 0.1 for photos

    MAX_GR = 100  # Maximum (full-scale) display range in grams

    TARE_1_MASS_GR = 68.0  # Channel 1 startup tare value; zero to disable
    TARE_2_MASS_GR = 78.0  # Channel 2 startup tare value; zero to disable
    ALARM_1_MASS_GR = 19.4  # Channel 1 startup alarm value; zero to disable
    ALARM_2_MASS_GR = 40.0  # Channel 2 startup alarm value; zero to disable

    TARE_1_ENABLE = True  # Channel 1 tare startup state
    TARE_2_ENABLE = True  # Channel 2 tare startup state
    ALARM_1_ENABLE = True  # Channel 1 alarm startup state
    ALARM_2_ENABLE = True  # Channel 2 alarm startup state

    MASS_UNITS = "GRAMS"  # Mass units of either GRAMS or OUNCES; OUNCES not supported in this version
