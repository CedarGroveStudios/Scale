# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# buttons_pyportal.py
# 2021-12-01 v1.1

import board
import time
import displayio
import adafruit_imageload
from adafruit_button import Button
import adafruit_touchscreen
from simpleio import tone

from cedargrove_scale.configuration import Colors
from cedargrove_scale.configuration import screen_to_rect


class ScaleButtons:
    def __init__(self, disp_height=240, disp_width=320, timeout=1.0, debug=False):
        """Instantiate the scale buttons for PyPortal devices.
        Builds displayio button group."""

        self._debug = debug
        self._timeout = timeout
        self._WIDTH = board.DISPLAY.width
        self._HEIGHT = board.DISPLAY.height

        self._outline = Colors.BLACK
        if self._debug:
            self._outline = Colors.GRAY

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
            "/cedargrove_scale/scale_sprite_sheet.bmp",
            bitmap=displayio.Bitmap,
            palette=displayio.Palette,
        )
        self._palette.make_transparent(3)

        # Build displayio button group #
        self._buttons = []
        self._button_group = displayio.Group()

        """x0, y0 = screen_to_rect(0.01, 0.02)
        w, h = screen_to_rect(0.30, 0.20)
        setup_1_button = Button(
            x=x0, y=y0, height=h, width=w,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name='setup_1',
            selected_fill=Colors.BLUE,
            selected_outline=Colors.BLUE,
        )
        self._button_group.append(setup_1_button)
        self._buttons.append(setup_1_button)

        x0, y0 = screen_to_rect(0.70, 0.02)
        w, h = screen_to_rect(0.30, 0.20)
        setup_2_button = Button(
            x=x0, y=y0, height=h, width=w,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name='setup_2',
            selected_fill=Colors.BLUE,
            selected_outline=Colors.BLUE,
        )
        self._button_group.append(setup_2_button)
        self._buttons.append(setup_2_button)"""

        x0, y0 = screen_to_rect(0.01, 0.28)
        w, h = screen_to_rect(0.30, 0.18)
        zero_1_button = Button(
            x=x0,
            y=y0,
            height=h,
            width=w,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name="zero_1",
            selected_fill=Colors.RED,
            selected_outline=Colors.RED,
        )
        self._button_group.append(zero_1_button)
        self._buttons.append(zero_1_button)

        x0, y0 = screen_to_rect(0.70, 0.28)
        w, h = screen_to_rect(0.30, 0.18)
        zero_2_button = Button(
            x=x0,
            y=y0,
            height=h,
            width=w,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name="zero_2",
            selected_fill=Colors.RED,
            selected_outline=Colors.RED,
        )
        self._button_group.append(zero_2_button)
        self._buttons.append(zero_2_button)

        x0, y0 = screen_to_rect(0.01, 0.50)
        w, h = screen_to_rect(0.30, 0.19)
        tare_1_button = Button(
            x=x0,
            y=y0,
            height=h,
            width=w,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name="tare_1",
            selected_fill=Colors.BLUE,
            selected_outline=Colors.BLUE,
        )
        self._button_group.append(tare_1_button)
        self._buttons.append(tare_1_button)

        x0, y0 = screen_to_rect(0.70, 0.50)
        w, h = screen_to_rect(0.30, 0.19)
        tare_2_button = Button(
            x=x0,
            y=y0,
            height=h,
            width=w,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name="tare_2",
            selected_fill=Colors.BLUE,
            selected_outline=Colors.BLUE,
        )
        self._button_group.append(tare_2_button)
        self._buttons.append(tare_2_button)

        x0, y0 = screen_to_rect(0.01, 0.70)
        w, h = screen_to_rect(0.30, 0.20)
        alarm_1_button = Button(
            x=x0,
            y=y0,
            height=h,
            width=w,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name="alarm_1",
            selected_fill=Colors.BLUE,
            selected_outline=Colors.BLUE,
        )
        self._button_group.append(alarm_1_button)
        self._buttons.append(alarm_1_button)

        x0, y0 = screen_to_rect(0.70, 0.70)
        w, h = screen_to_rect(0.30, 0.20)
        alarm_2_button = Button(
            x=x0,
            y=y0,
            height=h,
            width=w,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name="alarm_2",
            selected_fill=Colors.BLUE,
            selected_outline=Colors.BLUE,
        )
        self._button_group.append(alarm_2_button)
        self._buttons.append(alarm_2_button)

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
            print(
                "Invalid button timeout duration value. Must be between 0 and 10 seconds."
            )
            return
        self._timeout = hold_time
        return

    def read_buttons(self):
        button_pressed = None
        hold_time = 0
        touch = self._ts.touch_point
        if touch:
            for self._button in self._buttons:
                if self._button.contains(touch):
                    self._button.selected = True
                    tone(board.A0, 1319, 0.030)  # E6
                    button_pressed = self._button.name
                    timeout_beep = False
                    while self._ts.touch_point:
                        time.sleep(0.1)
                        hold_time += 0.1
                        if hold_time >= self._timeout and not timeout_beep:
                            tone(board.A0, 1175, 0.030)  # D6
                            timeout_beep = True
                    self._button.selected = False
        return button_pressed, hold_time
