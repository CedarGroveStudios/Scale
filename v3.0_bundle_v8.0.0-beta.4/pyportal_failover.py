# SPDX-FileCopyrightText: Copyright (c) 2022 Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`pyportal_failover.py`
================================================================================

Used after a fatal error to dim the display to keep the board cooler. Flashes
the NeoPixel during a pre-reset delay. Microcontroller is reset after the delay.

pyportal_failover.py  2022-10-25 1.0.1  Cedar Grove Studios

* Author(s): JG for Cedar Grove Maker Studios
"""

# imports__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/CedarGroveStudios/Failover"


import board
immport time
import microcontroller
import neopixel

DELAY = 20  # seconds

status = neopixel.NeoPixel(board.NEOPIXEL, 1)
status[0] = 0x040000  # Glow red on exception
board.DISPLAY.brightness = 0.5  # Dim the REPL display to keep things cool

print("pyportal_failover: begin reset delay")
end_delay = time.monotonic() + DELAY
while time.monotonic() < end_delay:
    """Flash NeoPixel during delay period."""
    time.sleep(1)
    if status[0] != (0, 0, 0):
        status[0] = 0x000000
    else:
        status[0] = 0x040000

print("pyportal_failover: resetting microcontroller")
microcontroller.reset()
