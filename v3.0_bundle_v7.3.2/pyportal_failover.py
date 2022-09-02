# SPDX-FileCopyrightText: Copyright (c) 2022 Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`pyportal_failover.py`
================================================================================

Used after a fatal error to dim the display to keep the board cooler and flash
the NeoPixel for attention.

pyportal_failover.py  2022-09-02 v1.0  Cedar Grove Studios

* Author(s): JG for Cedar Grove Maker Studios
"""

# imports__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/CedarGroveStudios/Failover"


import board
import neopixel
import time

status = neopixel.NeoPixel(board.NEOPIXEL, 1)
status[0] = 0x040000  # Glow red on exception
board.DISPLAY.brightness = 0.5  # Dim the REPL display to keep things cool

while True:
    """Flash the NeoPixel red forever."""
    time.sleep(1)
    if status[0] != (0, 0, 0):
        status[0] = 0x000000
    else:
        status[0] = 0x040000
