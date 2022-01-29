# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# scale_defaults.py  2022-01-28 v2.028  Cedar Grove Studios

class Defaults:

    NAME = "John's Espresso Bench"

    """
    DISPLAY -- choose unique descriptor string from:
      TFT FeatherWing - 2.4" 320x240 Touchscreen
      TFT FeatherWing - 3.5" 480x320 Touchscreen
      built-in
    CALIBRATION -- use touchscreen's zero-degree rotational measurement
    """
    DISPLAY = "3.5"
    CALIBRATION = ((357, 3812), (390, 3555))  # 3.5" FeatherWing touchscreen

    BRIGHTNESS = 0.5  # Display brightness, 0 to 1.0; 0.75 typical, 0.1 for photos

    MAX_GR = 100  # Maximum (full-scale) display range in grams

    CHAN_1_NAME = "beans"  # 6 characters maximum
    CHAN_2_NAME = "shots"  # 6 characters maximum

    TARE_1_MASS_GR = 70.0  # Channel 1 startup tare value; zero to disable
    TARE_2_MASS_GR = 35.0  # Channel 2 startup tare value; zero to disable
    ALARM_1_MASS_GR = 19.4  # Channel 1 startup alarm value; zero to disable
    ALARM_2_MASS_GR = 40.0  # Channel 2 startup alarm value; zero to disable

    TARE_1_ENABLE = True  # Channel 1 tare startup state
    TARE_2_ENABLE = True  # Channel 2 tare startup state
    ALARM_1_ENABLE = True  # Channel 1 alarm startup state
    ALARM_2_ENABLE = True  # Channel 2 alarm startup state

    MASS_UNITS = "GRAMS"  # Mass units of either GRAMS or OUNCES
