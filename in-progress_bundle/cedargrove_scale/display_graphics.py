# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# display_graphics.py
# 2021-12-05 v1.3

import time
import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from adafruit_display_shapes.circle import Circle

from cedargrove_scale.configuration import Colors, Screen, screen_to_rect
from scale_defaults import Defaults

if Screen.HEIGHT < 300:
    FONT_0 = bitmap_font.load_font("/fonts/Helvetica-Bold-24.bdf")
    FONT_1 = bitmap_font.load_font("/fonts/OpenSans-9.bdf")
    FONT_2 = bitmap_font.load_font("/fonts/OpenSans-9.bdf")
else:
    FONT_0 = bitmap_font.load_font("/fonts/Helvetica-Bold-36.bdf")
    FONT_1 = bitmap_font.load_font("/fonts/OpenSans-16.bdf")
    FONT_2 = bitmap_font.load_font("/fonts/OpenSans-9.bdf")


class Labels:
    def __init__(self):
        """Instantiate the labels and values objects.
        Builds a displayio labels group."""
        self._labels_group = displayio.Group()

        self.chan_1_name = Label(FONT_0, text=Defaults.CHAN_1_NAME, color=Colors.ORANGE)
        self.chan_1_name.anchor_point = (0, 0)
        self.chan_1_name.anchored_position = screen_to_rect(0.03, 0.10)
        self._labels_group.append(self.chan_1_name)

        self.chan_2_name = Label(FONT_0, text=Defaults.CHAN_2_NAME, color=Colors.GREEN)
        self.chan_2_name.anchor_point = (1.0, 0)
        self.chan_2_name.anchored_position = screen_to_rect(0.97, 0.10)
        self._labels_group.append(self.chan_2_name)

        self.chan_1_label = Label(
            FONT_0, text=Defaults.MASS_UNITS.lower(), color=Colors.BLUE
        )
        self.chan_1_label.anchor_point = (1.0, 0)
        self.chan_1_label.anchored_position = screen_to_rect(0.28, 0.38)
        self._labels_group.append(self.chan_1_label)

        self.chan_2_label = Label(
            FONT_0, text=Defaults.MASS_UNITS.lower(), color=Colors.BLUE
        )
        self.chan_2_label.anchor_point = (1.0, 0)
        self.chan_2_label.anchored_position = screen_to_rect(0.97, 0.38)
        self._labels_group.append(self.chan_2_label)

        self.chan_1_value = Label(FONT_0, text="0.0", color=Colors.WHITE)
        self.chan_1_value.anchor_point = (1.0, 1.0)
        self.chan_1_value.anchored_position = screen_to_rect(0.28, 0.38)
        self._labels_group.append(self.chan_1_value)

        self.chan_2_value = Label(FONT_0, text="0.0", color=Colors.WHITE)
        self.chan_2_value.anchor_point = (1.0, 1.0)
        self.chan_2_value.anchored_position = screen_to_rect(0.97, 0.38)
        self._labels_group.append(self.chan_2_value)

        self.tare_1_value = Label(FONT_1, text="0.0", color=Colors.GRAY)
        self.tare_1_value.anchor_point = (1.0, 0.5)
        self.tare_1_value.anchored_position = screen_to_rect(0.28, 0.56)
        self._labels_group.append(self.tare_1_value)

        self.tare_2_value = Label(FONT_1, text="0.0", color=Colors.GRAY)
        self.tare_2_value.anchor_point = (0.0, 0.5)
        self.tare_2_value.anchored_position = screen_to_rect(0.75, 0.56)
        self._labels_group.append(self.tare_2_value)

        self.alarm_1_value = Label(FONT_1, text="0.0", color=Colors.GRAY)
        self.alarm_1_value.anchor_point = (1.0, 0.5)
        self.alarm_1_value.anchored_position = screen_to_rect(0.28, 0.75)
        self._labels_group.append(self.alarm_1_value)

        self.alarm_2_value = Label(FONT_1, text="0.0", color=Colors.GRAY)
        self.alarm_2_value.anchor_point = (0.0, 0.5)
        self.alarm_2_value.anchored_position = screen_to_rect(0.75, 0.75)
        self._labels_group.append(self.alarm_2_value)

        self.status_label = Label(FONT_1, text=" ", color=None)
        self.status_label.anchor_point = (0.5, 0.5)
        self.status_label.anchored_position = screen_to_rect(0.50, 0.92)
        self._labels_group.append(self.status_label)

        x0, y0 = screen_to_rect(0.05, 0.95)
        w, h = screen_to_rect(0.025, 0.025)
        self._heartbeat = Circle(
            x0, y0, min(w, h), fill=Colors.MAROON, outline=None, stroke=0
        )
        self._labels_group.append(self._heartbeat)
        return

    @property
    def display_group(self):
        """Displayio labels group."""
        return self._labels_group

    def heartbeat(self, color_index=0):
        """Set heartbeat indicator color."""
        if color_index == None:
            self._heartbeat.fill = None
        elif color_index == 0:
            self._heartbeat.fill = Colors.MAROON
        elif color_index == 1:
            self._heartbeat.fill = Colors.YELLOW
        return

    def flash_status(self, text=" ", duration=0.05):
        """Flash a text message once in the stats message area.
        param: text: The text to be displayed.
        param: duration: The display duration in seconds."""

        self.status_label.text = " "
        self.status_label.text = text
        self.status_label.color = Colors.YELLOW
        time.sleep(duration)
        self.status_label.color = Colors.BLACK
        time.sleep(duration)
        self.status_label.text = " "
        return
