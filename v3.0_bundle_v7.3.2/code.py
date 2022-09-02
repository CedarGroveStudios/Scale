# SPDX-FileCopyrightText: Copyright (c) 2022 Cedar Grove Maker Studios
#
# SPDX-License-Identifier: MIT
"""
`code.py`
================================================================================

A "jumping-off" code.py for the Scale project.
code.py  2022-09-02 v2.0  Cedar Grove Studios

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

"""Set FAILOVER to True to fail to a dimmed display and flashing NeoPixel;
False to fail normally with error reporting via the REPL."""
FAILOVER = False

while True and FAILOVER:
    """Attempt to start the primary code module. Upon failure, execute the
    failover module."""

    try:
        import scale_code
    except Exception as e:
        import time
        print(f"pyportal failover: --{e}--  at time.monotonic: {time.monotonic()}")
        import pyportal_failover
else:
    import scale_code
