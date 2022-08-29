# SPDX-FileCopyrightText: Copyright (c) 2022 Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`code.py`
================================================================================

A "jumping-off" code.py for the Scale project.
code.py  2022-08-26 v2.0  Cedar Grove Studios

* Author(s): JG for Cedar Grove Maker Studios
"""

# imports__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/CedarGroveStudios/Scale"


# Uncomment the following to calibrate touch screen for a built-in display
# import touch_calibrator_built_in

# Uncomment the following to calibrate touch screen for an attached display
# import touch_calibrator_stmpe610

# Uncomment the following to run the load cell calibration method
# import cedargrove_scale.load_cell_calibrator


while True:
    """Attempt to start the primary code module. Upon failure, dim the display
    to keep the board cooler and flash the NeoPixel for attention."""

    try:
        import scale_code
    except Exception as e:
        import board
        import neopixel
        import time

        status = neopixel.NeoPixel(board.NEOPIXEL, 1)
        status[0] = 0x040000  # Glow red on exception
        board.DISPLAY.brightness = 0.5  # Dim the REPL display to keep things cool

        print(f"scale_code.py: {e}  time.monotonic: {time.monotonic()}")

        while True:
            """Flash the NeoPixel red forever."""
            time.sleep(1)
            if status[0] != (0, 0, 0):
                status[0] = 0x000000  # Flash red on exception
            else:
                status[0] = 0x040000  # Flash red on exception
