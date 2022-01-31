# SPDX-FileCopyrightText: 2021 Cedar Grove Maker Studios
# SPDX-License-Identifier: MIT

# cedargrove_scale.buttons.py  2022-01-29 v3.029  Cedar Grove Studios

import board
import time
import displayio
import adafruit_imageload
from adafruit_button import Button
from simpleio import tone
from cedargrove_scale.configuration import Colors, Display


class ScaleButtons(displayio.Group):
    def __init__(self, touchscreen=None, timeout=1.0, debug=False):
        """Instantiate the on-screen touch buttons. Builds the displayio
        button_group.

        :param class touchscreen: The touchscreen class. Defaults to None.
        :param float timeout: Button hold timeout in seconds. Defaults to 1.0.
        :param bool debug: Displays buttons with visible touch outlines.
        """

        display = Display()

        self._debug = debug
        self._timeout = timeout

        if touchscreen:
            self._ts = touchscreen
        else:
            raise RuntimeError("*** ERROR: Touchscreen NOT FOUND.")

        self._outline = Colors.BLACK
        if self._debug:
            self._outline = Colors.GRAY

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

        x0, y0 = display.screen_to_rect(0.25, 0.01)
        w, h = display.screen_to_rect(0.50, 0.15)
        reset_button = Button(
            x=x0,
            y=y0,
            height=h,
            width=w,
            style=Button.ROUNDRECT,
            fill_color=None,
            outline_color=self._outline,
            name="reset",
            selected_fill=Colors.RED,
            selected_outline=Colors.RED,
        )
        self._button_group.append(reset_button)
        self._buttons.append(reset_button)

        x0, y0 = display.screen_to_rect(0.01, 0.28)
        w, h = display.screen_to_rect(0.30, 0.18)
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

        x0, y0 = display.screen_to_rect(0.70, 0.28)
        w, h = display.screen_to_rect(0.30, 0.18)
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

        x0, y0 = display.screen_to_rect(0.01, 0.50)
        w, h = display.screen_to_rect(0.30, 0.19)
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

        x0, y0 = display.screen_to_rect(0.70, 0.50)
        w, h = display.screen_to_rect(0.30, 0.19)
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

        x0, y0 = display.screen_to_rect(0.01, 0.70)
        w, h = display.screen_to_rect(0.30, 0.20)
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

        x0, y0 = display.screen_to_rect(0.70, 0.70)
        w, h = display.screen_to_rect(0.30, 0.20)
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
        self.tare_1_icon.x, self.tare_1_icon.y = display.screen_to_rect(0.08, 0.50)
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
        self.alarm_1_icon.x, self.alarm_1_icon.y = display.screen_to_rect(0.08, 0.70)
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
        self.tare_2_icon.x, self.tare_2_icon.y = display.screen_to_rect(0.85, 0.50)
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
        self.alarm_2_icon.x, self.alarm_2_icon.y = display.screen_to_rect(0.85, 0.70)
        self.alarm_2_icon[0] = 6
        self._button_group.append(self.alarm_2_icon)

        super().__init__()
        self.append(self._button_group)
        return

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
