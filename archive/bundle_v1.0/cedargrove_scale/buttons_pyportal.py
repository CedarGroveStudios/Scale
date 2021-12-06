# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# buttons_pyportal.py
# 2021-10-13 v1.0.1

import board
import time
import displayio
import adafruit_imageload
from adafruit_button import Button
import adafruit_touchscreen
from simpleio import tone

from cedargrove_scale.configuration import Palette as color
from cedargrove_scale.configuration import play_tone, dial_to_rect, screen_to_rect


class ScaleButtons:
    def __init__(self, disp_height=240, disp_width=320, timeout=1.0, debug=False):
        """Instantiate the scale buttons for PyPortal devices.
        Builds displayio button group."""

        self._debug = debug
        self._timeout = timeout
        self._WIDTH = board.DISPLAY.width
        self._HEIGHT = board.DISPLAY.height

        self._outline = color.BLACK
        if self._debug:
            self._outline = color.GRAY

        self._ts = adafruit_touchscreen.Touchscreen(
            board.TOUCH_XL,
            board.TOUCH_XR,
            board.TOUCH_YD,
            board.TOUCH_YU,
            calibration=((5200, 59000), (5800, 57000)),
            size=(self._WIDTH, self._HEIGHT),
        )

        # Tare and alarm tile grid
        self._sprite_sheet, self._palette = adafruit_imageload.load(
            '/cedargrove_scale/scale_sprite_sheet.bmp',
            bitmap=displayio.Bitmap,
            palette=displayio.Palette,
        )
        self._palette.make_transparent(3)

        # Build displayio button group #
        self._buttons = []
        self._button_group = displayio.Group()

        """self._sx, self._sy = screen_to_rect(0.01, 0.02)
        self._sw, self._sh = screen_to_rect(0.30, 0.20)
        self.setup_1_button = Button(
            x=self._sx, y=self._sy, height=self._sh, width=self._sw,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name='setup_1',
            selected_fill=color.BLUE,
            selected_outline=color.BLUE,
        )
        self._button_group.append(self.setup_1_button)
        self._buttons.append(self.setup_1_button)

        self._sx, self._sy = screen_to_rect(0.70, 0.02)
        self._sw, self._sh = screen_to_rect(0.30, 0.20)
        self.setup_2_button = Button(
            x=self._sx, y=self._sy, height=self._sh, width=self._sw,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name='setup_2',
            selected_fill=color.BLUE,
            selected_outline=color.BLUE,
        )
        self._button_group.append(self.setup_2_button)
        self._buttons.append(self.setup_2_button)"""

        self._sx, self._sy = screen_to_rect(0.01, 0.28)
        self._sw, self._sh = screen_to_rect(0.30, 0.18)
        self.zero_1_button = Button(
            x=self._sx,
            y=self._sy,
            height=self._sh,
            width=self._sw,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name='zero_1',
            selected_fill=color.RED,
            selected_outline=color.RED,
        )
        self._button_group.append(self.zero_1_button)
        self._buttons.append(self.zero_1_button)

        self._sx, self._sy = screen_to_rect(0.70, 0.28)
        self._sw, self._sh = screen_to_rect(0.30, 0.18)
        self.zero_2_button = Button(
            x=self._sx,
            y=self._sy,
            height=self._sh,
            width=self._sw,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name='zero_2',
            selected_fill=color.RED,
            selected_outline=color.RED,
        )
        self._button_group.append(self.zero_2_button)
        self._buttons.append(self.zero_2_button)

        self._sx, self._sy = screen_to_rect(0.01, 0.50)
        self._sw, self._sh = screen_to_rect(0.30, 0.19)
        self.tare_1_button = Button(
            x=self._sx,
            y=self._sy,
            height=self._sh,
            width=self._sw,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name='tare_1',
            selected_fill=color.BLUE,
            selected_outline=color.BLUE,
        )
        self._button_group.append(self.tare_1_button)
        self._buttons.append(self.tare_1_button)

        self._sx, self._sy = screen_to_rect(0.70, 0.50)
        self._sw, self._sh = screen_to_rect(0.30, 0.19)
        self.tare_2_button = Button(
            x=self._sx,
            y=self._sy,
            height=self._sh,
            width=self._sw,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name='tare_2',
            selected_fill=color.BLUE,
            selected_outline=color.BLUE,
        )
        self._button_group.append(self.tare_2_button)
        self._buttons.append(self.tare_2_button)

        self._sx, self._sy = screen_to_rect(0.01, 0.70)
        self._sw, self._sh = screen_to_rect(0.30, 0.20)
        self.alarm_1_button = Button(
            x=self._sx,
            y=self._sy,
            height=self._sh,
            width=self._sw,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name='alarm_1',
            selected_fill=color.BLUE,
            selected_outline=color.BLUE,
        )
        self._button_group.append(self.alarm_1_button)
        self._buttons.append(self.alarm_1_button)

        sx, sy = screen_to_rect(0.70, 0.70)
        sw, sh = screen_to_rect(0.30, 0.20)
        self.alarm_2_button = Button(
            x=sx,
            y=sy,
            height=sh,
            width=sw,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name='alarm_2',
            selected_fill=color.BLUE,
            selected_outline=color.BLUE,
        )
        self._button_group.append(self.alarm_2_button)
        self._buttons.append(self.alarm_2_button)

        self.tare_1_icon = displayio.TileGrid(
            self._sprite_sheet,
            pixel_shader=self._palette,
            width=1,
            height=1,
            tile_width=32,
            tile_height=48,
        )
        self.tare_1_icon.x, self.tare_1_icon.y = screen_to_rect(0.08, 0.50)
        self.tare_1_icon[0] = 3
        self._button_group.append(self.tare_1_icon)

        self.alarm_1_icon = displayio.TileGrid(
            self._sprite_sheet,
            pixel_shader=self._palette,
            width=1,
            height=1,
            tile_width=32,
            tile_height=48,
        )
        self.alarm_1_icon.x, self.alarm_1_icon.y = screen_to_rect(0.08, 0.70)
        self.alarm_1_icon[0] = 2
        self._button_group.append(self.alarm_1_icon)

        self.tare_2_icon = displayio.TileGrid(
            self._sprite_sheet,
            pixel_shader=self._palette,
            width=1,
            height=1,
            tile_width=32,
            tile_height=48,
        )
        self.tare_2_icon.x, self.tare_2_icon.y = screen_to_rect(0.85, 0.50)
        self.tare_2_icon[0] = 7
        self._button_group.append(self.tare_2_icon)

        self.alarm_2_icon = displayio.TileGrid(
            self._sprite_sheet,
            pixel_shader=self._palette,
            width=1,
            height=1,
            tile_width=32,
            tile_height=48,
        )
        self.alarm_2_icon.x, self.alarm_2_icon.y = screen_to_rect(0.85, 0.70)
        self.alarm_2_icon[0] = 6
        self._button_group.append(self.alarm_2_icon)

        return

    @property
    def button_group(self):
        """Displayio button group."""
        return self._button_group

    @property
    def timeout(self):
        """Button timeout duration setting."""
        return self._timeout

    @timeout.setter
    def timeout(self, hold_time=1.0):
        """Select timeout duration value in seconds, positive float value."""
        if hold_time < 0 or hold_time >= 10:
            print('Invalid button timeout duration value. Must be between 0 and 10 seconds.')
            return
        self._timeout = hold_time
        return

    def read_buttons(self):
        self._button_pressed = None
        self._hold_time = 0
        self._touch = self._ts.touch_point
        if self._touch:
            for self._button in self._buttons:
                if self._button.contains(self._touch):
                    self._button.selected = True
                    tone(board.A0, 1319, 0.030)  # E6
                    self._button_pressed = self._button.name
                    self._timeout_beep = False
                    while self._ts.touch_point:
                        time.sleep(0.1)
                        self._hold_time += 0.1
                        if self._hold_time >= self._timeout and not self._timeout_beep:
                            tone(board.A0, 1175, 0.030)  # D6
                            self._timeout_beep = True
                    self._button.selected = False
        return self._button_pressed, self._hold_time
