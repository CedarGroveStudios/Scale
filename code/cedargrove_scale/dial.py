# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# dial.py
# 2021-10-13 v1.0

import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.circle import Circle

from cedargrove_scale.configuration import Palette, Screen, Pointer
from cedargrove_scale.configuration import dial_to_rect, screen_to_rect
from scale_defaults import Defaults

FONT_2 = bitmap_font.load_font('/fonts/OpenSans-9.bdf')

class Dial:
    def __init__(self, center=(0.50, 0.50), radius=0.25, debug=False):
        """Instantiate the dial graphic for PyPortal devices.
        Builds a displayio dial group."""

        self._debug = debug

        # Normalized screen values
        self._center_norm = center
        self._radius_norm = radius

        # Pixel screen values
        self.CENTER = int(center[0] * Screen.WIDTH), int(center[1] * Screen.HEIGHT)
        self.RADIUS = int(radius * min(Screen.WIDTH, Screen.HEIGHT))

        self._dial_group = displayio.Group()

        # Define primary dial graphic
        self._sx, self._sy = screen_to_rect(self._center_norm[0], self._center_norm[1])
        self._ry, self._ry = screen_to_rect(0.00, self._radius_norm)
        self.scale_dial = Circle(
            self._sx, self._sy, self._ry,
            fill=Palette.BLUE_DK,
            outline=Palette.WHITE,
            stroke=1,
        )
        self._dial_group.append(self.scale_dial)

        # Define hash marks
        for i in range(0, Defaults.MAX_GR, Defaults.MAX_GR // 10):
            self._hash_value = Label(FONT_2, text=str(i), color=Palette.CYAN)
            self._hash_value.anchor_point = (0.5, 0.5)
            self._hash_value.anchored_position = dial_to_rect(
                i / Defaults.MAX_GR, radius=Pointer.IN_PATH_RADIUS
            )
            self._dial_group.append(self._hash_value)

            self._x0, self._y0 = dial_to_rect(i / Defaults.MAX_GR, radius=Pointer.OUT_PATH_RADIUS)
            self._x1, self._y1 = dial_to_rect(i / Defaults.MAX_GR, radius=self.RADIUS)
            self._hash_mark_a = Line(self._x0, self._y0, self._x1, self._y1, Palette.CYAN)
            self._dial_group.append(self._hash_mark_a)

            self._x0, self._y0 = dial_to_rect(
                (i + Defaults.MAX_GR / 20) / Defaults.MAX_GR,
                radius=Pointer.OUT_PATH_RADIUS + Pointer.RADIUS,
            )
            self._x1, self._y1 = dial_to_rect((i + Defaults.MAX_GR / 20) / Defaults.MAX_GR, radius=self.RADIUS)
            self._hash_mark_b = Line(self._x0, self._y0, self._x1, self._y1, Palette.CYAN)
            self._dial_group.append(self._hash_mark_b)
        return


    @property
    def dial_display_group(self):
        """Displayio dial group."""
        return self._dial_group

    @property
    def center(self):
        """Dial center normalized screen coordinates."""
        return self._center_norm

    @property
    def radius(self):
        """Dial radius normalized screen value."""
        return self._radius_norm
