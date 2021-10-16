# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# scale.py
# 2021-10-15 v1.0

import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.circle import Circle
from adafruit_display_text.label import Label
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle

from cedargrove_scale.configuration import Palette, Screen, Pointer
from cedargrove_scale.configuration import dial_to_rect, screen_to_rect
from scale_defaults import Defaults

FONT_0 = bitmap_font.load_font('/fonts/Helvetica-Bold-24.bdf')
FONT_1 = bitmap_font.load_font('/fonts/OpenSans-16.bdf')
FONT_2 = bitmap_font.load_font('/fonts/OpenSans-9.bdf')

class Case:
    def __init__(self, debug=False):
        """Instantiate the scale case graphic for PyPortal devices.
        Builds a displayio case group."""
        self._debug = debug

        self._case_group = displayio.Group()

        self._sx0, self._sy0 = screen_to_rect(0.50, 0.50)
        self._sx1, self._sy1 = screen_to_rect(0.65, 0.80)
        self._sx2, self._sy2 = screen_to_rect(0.35, 0.80)
        self._scale_base = Triangle(
            self._sx0, self._sy0, self._sx1, self._sy1, self._sx2, self._sy2,
            fill=Palette.GRAY,
            outline=Palette.BLACK,
        )
        self._case_group.append(self._scale_base)

        self._sx, self._sy = screen_to_rect(0.34, 0.80)
        self._sw, self._sh = screen_to_rect(0.32, 0.06)
        self._scale_foot = RoundRect(
            self._sx, self._sy, width=self._sw, height=self._sh,
            r=5,
            fill=Palette.GRAY,
            outline=Palette.BLACK,
        )
        self._case_group.append(self._scale_foot)
        return

    @property
    def display_group(self):
        """Displayio case group."""
        return self._case_group

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
    def display_group(self):
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

class Labels:
    def __init__(self, debug=False):
        """Instantiate the labels and values objects.
        Builds a displayio labels group."""
        self._debug = debug

        self._labels_group = displayio.Group()

        self.chan_1_name = Label(FONT_0, text=Defaults.CHAN_1_NAME, color=Palette.ORANGE)
        self.chan_1_name.anchor_point = (1.0, 0)
        self.chan_1_name.anchored_position = screen_to_rect(0.28, 0.10)
        self._labels_group.append(self.chan_1_name)

        self.chan_2_name = Label(FONT_0, text=Defaults.CHAN_2_NAME, color=Palette.GREEN)
        self.chan_2_name.anchor_point = (1.0, 0)
        self.chan_2_name.anchored_position = screen_to_rect(0.97, 0.10)
        self._labels_group.append(self.chan_2_name)

        self.chan_1_label = Label(FONT_0, text=Defaults.MASS_UNITS.lower(), color=Palette.BLUE)
        self.chan_1_label.anchor_point = (1.0, 0)
        self.chan_1_label.anchored_position = screen_to_rect(0.28, 0.38)
        self._labels_group.append(self.chan_1_label)

        self.chan_2_label = Label(FONT_0, text=Defaults.MASS_UNITS.lower(), color=Palette.BLUE)
        self.chan_2_label.anchor_point = (1.0, 0)
        self.chan_2_label.anchored_position = screen_to_rect(0.97, 0.38)
        self._labels_group.append(self.chan_2_label)

        self.chan_1_value = Label(FONT_0, text='0.0', color=Palette.WHITE)
        self.chan_1_value.anchor_point = (1.0, 1.0)
        self.chan_1_value.anchored_position = screen_to_rect(0.28, 0.38)
        self._labels_group.append(self.chan_1_value)

        self.chan_2_value = Label(FONT_0, text='0.0', color=Palette.WHITE)
        self.chan_2_value.anchor_point = (1.0, 1.0)
        self.chan_2_value.anchored_position = screen_to_rect(0.97, 0.38)
        self._labels_group.append(self.chan_2_value)

        self.tare_1_value = Label(FONT_2, text='0.0', color=Palette.GRAY)
        self.tare_1_value.anchor_point = (1.0, 0.5)
        self.tare_1_value.anchored_position = screen_to_rect(0.28, 0.56)
        self._labels_group.append(self.tare_1_value)

        self.tare_2_value = Label(FONT_2, text='0.0', color=Palette.GRAY)
        self.tare_2_value.anchor_point = (0.0, 0.5)
        self.tare_2_value.anchored_position = screen_to_rect(0.75, 0.56)
        self._labels_group.append(self.tare_2_value)

        self.alarm_1_value = Label(FONT_2, text='0.0', color=Palette.GRAY)
        self.alarm_1_value.anchor_point = (1.0, 0.5)
        self.alarm_1_value.anchored_position = screen_to_rect(0.28, 0.75)
        self._labels_group.append(self.alarm_1_value)

        self.alarm_2_value = Label(FONT_2, text='0.0', color=Palette.GRAY)
        self.alarm_2_value.anchor_point = (0.0, 0.5)
        self.alarm_2_value.anchored_position = screen_to_rect(0.75, 0.75)
        self._labels_group.append(self.alarm_2_value)

        self.status_label = Label(FONT_2, text=' ', color=None)
        self.status_label.anchor_point = (0.5, 0.5)
        self.status_label.anchored_position = screen_to_rect(0.50, 0.95)
        self._labels_group.append(self.status_label)

        return

    @property
    def display_group(self):
        """Displayio labels group."""
        return self._labels_group

class Plate:
    def __init__(self, debug=False):
        """Instantiate the plate and riser object.
        Builds a displayio plate group."""
        self._debug = debug

        self._plate_group = displayio.Group()

        self._sx, self._sy = screen_to_rect(0.46, 0.16)
        self._sw, self._sh = screen_to_rect(0.08, 0.25)
        self.riser = Rect(
            self._sx, self._sy, width=self._sw, height=self._sh,
            fill=Palette.GRAY,
            outline=Palette.BLACK,
        )
        self._plate_group.append(self.riser)

        self._sx, self._sy = screen_to_rect(0.34, 0.16)
        self._sw, self._sh = screen_to_rect(0.32, 0.06)
        self.plate = RoundRect(
            self._sx, self._sy, width=self._sw, height=self._sh,
            r=5,
            fill=Palette.GRAY,
            outline=Palette.BLACK,
        )
        self._plate_group.append(self.plate)
        return

    @property
    def display_group(self):
        """Displayio plate group."""
        return self._plate_group
