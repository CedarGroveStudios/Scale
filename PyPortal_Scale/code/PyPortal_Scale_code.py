# PyPortal Scale -- dual channel version
# Cedar Grove NAU7802 FeatherWing
# 2021-04-23 v04 Cedar Grove Studios

# import load_cell_calibrator  # uncomment to run calibration method

import board
import time
import displayio

from adafruit_bitmapsaver import save_pixels

from simpleio import map_range
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_text.label import Label
from adafruit_bitmap_font import bitmap_font
from adafruit_pyportal import PyPortal
from adafruit_button import Button
from cedargrove_nau7802 import NAU7802
from scale_setup import Defaults as default
from scale_setup import ScalePalette as color

# Determine display size and calculate plot offsets
WIDTH = board.DISPLAY.width
HEIGHT = board.DISPLAY.height
DISP_X_OFFSET = (WIDTH - 240) // 2
DISP_Y_OFFSET = (HEIGHT - 240) // 2
BKG_X_OFFSET = (WIDTH - 480) // 2
BKG_Y_OFFSET = DISP_Y_OFFSET

# Instantiate PyPortal platform and load sensor ADC
pyportal = PyPortal()
nau7802 = NAU7802(board.I2C(), address=0x2A, active_channels=2)

# Instantiate display and fonts
# print('*** Instantiate the display and fonts')
display = board.DISPLAY
#scale_group = displayio.Group(max_size=19)
scale_group = displayio.Group()

FONT_0 = bitmap_font.load_font('/fonts/Helvetica-Bold-24.bdf')
FONT_1 = bitmap_font.load_font('/fonts/OpenSans-16.bdf')
FONT_2 = bitmap_font.load_font('/fonts/OpenSans-9.bdf')

# Define displayio background and group elements
print('*** Define displayio background and group elements')
# Bitmap background
_bkg = open('/scale_dual_chan_bkg.bmp', 'rb')
bkg = displayio.OnDiskBitmap(_bkg)
try:
    _background = displayio.TileGrid(bkg,
                                     pixel_shader=displayio.ColorConverter(),
                                     x=0+BKG_X_OFFSET, y=0+BKG_Y_OFFSET)
except TypeError:
    _background = displayio.TileGrid(bkg,
                                     pixel_shader=displayio.ColorConverter(),
                                     x=0+BKG_X_OFFSET, y=0+BKG_Y_OFFSET)
scale_group.append(_background)

# -- BUTTONS -- #
buttons = []
zero_1_button = Button(x=0+DISP_X_OFFSET, y=180+DISP_Y_OFFSET, height=58,
                       width=90, style=Button.ROUNDRECT, fill_color=None,
                       outline_color=color.BLACK, name='zero_1',
                       selected_fill=color.RED, selected_outline=color.RED)
scale_group.append(zero_1_button)
buttons.append(zero_1_button)

zero_2_button = Button(x=149+DISP_X_OFFSET, y=180+DISP_Y_OFFSET, height=58,
                       width=90, style=Button.ROUNDRECT, fill_color=None,
                       outline_color=color.BLACK, name='zero_2',
                       selected_fill=color.RED, selected_outline=color.RED)
scale_group.append(zero_2_button)
buttons.append(zero_2_button)

tare_1_button = Button(x=0+DISP_X_OFFSET, y=100+DISP_Y_OFFSET, height=58,
                       width=90, style=Button.ROUNDRECT, fill_color=None,
                       outline_color=color.BLACK, name='tare_1',
                       selected_fill=color.BLUE, selected_outline=color.BLUE)
scale_group.append(tare_1_button)
buttons.append(tare_1_button)

tare_2_button = Button(x=149+DISP_X_OFFSET, y=100+DISP_Y_OFFSET, height=58,
                       width=90, style=Button.ROUNDRECT, fill_color=None,
                       outline_color=color.BLACK, name='tare_2',
                       selected_fill=color.BLUE, selected_outline=color.BLUE)
scale_group.append(tare_2_button)
buttons.append(tare_2_button)

up_button = Button(x=240+DISP_X_OFFSET, y=70+DISP_Y_OFFSET, height=40,
                       width=40, style=Button.ROUNDRECT, fill_color=None,
                       outline_color=color.BLACK, name='up',
                       selected_fill=color.GREEN, selected_outline=color.GREEN)
scale_group.append(up_button)
buttons.append(up_button)

save_button = Button(x=240+DISP_X_OFFSET, y=115+DISP_Y_OFFSET, height=40,
                       width=40, style=Button.ROUNDRECT, fill_color=None,
                       outline_color=color.RED, name='save',
                       label='save', label_font=FONT_2, label_color=color.RED,
                       selected_fill=color.RED, selected_outline=color.RED)
scale_group.append(save_button)
buttons.append(save_button)

down_button = Button(x=240+DISP_X_OFFSET, y=160+DISP_Y_OFFSET, height=40,
                       width=40, style=Button.ROUNDRECT, fill_color=None,
                       outline_color=color.BLACK, name='down',
                       selected_fill=color.GREEN, selected_outline=color.GREEN)
scale_group.append(down_button)
buttons.append(down_button)

# -- DISPLAY ELEMENTS -- #
chan_1_label = Label(FONT_1, text=default.CHAN_1_LABEL, color=color.CYAN,
                     max_glyphs=10)
chan_1_label.anchor_point = (0.5, 0.5)
chan_1_label.anchored_position = (40+DISP_X_OFFSET, 75+DISP_Y_OFFSET)
scale_group.append(chan_1_label)

chan_2_label = Label(FONT_1, text=default.CHAN_2_LABEL, color=color.CYAN,
                     max_glyphs=10)
chan_2_label.anchor_point = (0.5, 0.5)
chan_2_label.anchored_position = (199+DISP_X_OFFSET, 75+DISP_Y_OFFSET)
scale_group.append(chan_2_label)

zero_value = Label(FONT_2, text='0', color=color.CYAN, max_glyphs=1)
zero_value.anchor_point = (1.0, 0.5)
zero_value.anchored_position = (97+DISP_X_OFFSET, 200+DISP_Y_OFFSET)
scale_group.append(zero_value)

min_value = Label(FONT_2, text=str(default.MIN_GR), color=color.CYAN, max_glyphs=6)
min_value.anchor_point = (1.0, 1.0)
min_value.anchored_position = (99+DISP_X_OFFSET, 239+DISP_Y_OFFSET)
scale_group.append(min_value)

max_value = Label(FONT_2, text=str(default.MAX_GR), color=color.CYAN, max_glyphs=6)
max_value.anchor_point = (1.0, 0)
max_value.anchored_position = (99+DISP_X_OFFSET, 0+DISP_Y_OFFSET)
scale_group.append(max_value)

plus_1_value = Label(FONT_2, text=str(1 * (default.MAX_GR // 5)), color=color.CYAN,
                     max_glyphs=6)
plus_1_value.anchor_point = (1.0, 0.5)
plus_1_value.anchored_position = (99+DISP_X_OFFSET, 160+DISP_Y_OFFSET)
scale_group.append(plus_1_value)

plus_2_value = Label(FONT_2, text=str(2 * (default.MAX_GR // 5)), color=color.CYAN,
                     max_glyphs=6)
plus_2_value.anchor_point = (1.0, 0.5)
plus_2_value.anchored_position = (99+DISP_X_OFFSET, 120+DISP_Y_OFFSET)
scale_group.append(plus_2_value)

plus_3_value = Label(FONT_2, text=str(3 * (default.MAX_GR // 5)), color=color.CYAN,
                     max_glyphs=6)
plus_3_value.anchor_point = (1.0, 0.5)
plus_3_value.anchored_position = (99+DISP_X_OFFSET, 80+DISP_Y_OFFSET)
scale_group.append(plus_3_value)

plus_4_value = Label(FONT_2, text=str(4 * (default.MAX_GR // 5)), color=color.CYAN,
                     max_glyphs=6)
plus_4_value.anchor_point = (1.0, 0.5)
plus_4_value.anchored_position = (99+DISP_X_OFFSET, 40+DISP_Y_OFFSET)
scale_group.append(plus_4_value)

chan_1_label = Label(FONT_0, text='grams', color=color.BLUE, max_glyphs=6)
chan_1_label.anchor_point = (1.0, 0)
chan_1_label.anchored_position = (80+DISP_X_OFFSET, 216+DISP_Y_OFFSET)
scale_group.append(chan_1_label)

chan_2_label = Label(FONT_0, text='grams', color=color.BLUE, max_glyphs=6)
chan_2_label.anchor_point = (1.0, 0)
chan_2_label.anchored_position = (230+DISP_X_OFFSET, 216+DISP_Y_OFFSET)
scale_group.append(chan_2_label)

chan_1_value = Label(FONT_0, text='0.0', color=color.WHITE, max_glyphs=10)
chan_1_value.anchor_point = (1.0, 0.5)
chan_1_value.anchored_position = (80+DISP_X_OFFSET, 200+DISP_Y_OFFSET)
scale_group.append(chan_1_value)

chan_2_value = Label(FONT_0, text='0.0', color=color.WHITE, max_glyphs=10)
chan_2_value.anchor_point = (1.0, 0.5)
chan_2_value.anchored_position = (230+DISP_X_OFFSET, 200+DISP_Y_OFFSET)
scale_group.append(chan_2_value)

tare_1_label = Label(FONT_2, text='TARE', color=color.GRAY, max_glyphs=4)
tare_1_label.anchor_point = (1.0, 0)
tare_1_label.anchored_position = (80+DISP_X_OFFSET, 166+DISP_Y_OFFSET)
scale_group.append(tare_1_label)

tare_2_label = Label(FONT_2, text='TARE', color=color.GRAY, max_glyphs=4)
tare_2_label.anchor_point = (1.0, 0)
tare_2_label.anchored_position = (230+DISP_X_OFFSET, 166+DISP_Y_OFFSET)
scale_group.append(tare_2_label)

tare_1_value = Label(FONT_1, text='0.0', color=color.GRAY, max_glyphs=10)
tare_1_value.anchor_point = (1.0, 0.5)
tare_1_value.anchored_position = (80+DISP_X_OFFSET, 150+DISP_Y_OFFSET)
scale_group.append(tare_1_value)

tare_2_value = Label(FONT_1, text='0.0', color=color.GRAY, max_glyphs=10)
tare_2_value.anchor_point = (1.0, 0.5)
tare_2_value.anchored_position = (230+DISP_X_OFFSET, 150+DISP_Y_OFFSET)
scale_group.append(tare_2_value)


alarm_1_label = Label(FONT_2, text='ALARM', color=color.GRAY, max_glyphs=4)
alarm_1_label.anchor_point = (1.0, 0)
alarm_1_label.anchored_position = (80+DISP_X_OFFSET, 116+DISP_Y_OFFSET)
scale_group.append(alarm_1_label)

alarm_2_label = Label(FONT_2, text='ALARM', color=color.GRAY, max_glyphs=4)
alarm_2_label.anchor_point = (1.0, 0)
alarm_2_label.anchored_position = (230+DISP_X_OFFSET, 116+DISP_Y_OFFSET)
scale_group.append(alarm_2_label)

alarm_1_value = Label(FONT_1, text='0.0', color=color.GRAY, max_glyphs=10)
alarm_1_value.anchor_point = (1.0, 0.5)
alarm_1_value.anchored_position = (80+DISP_X_OFFSET, 100+DISP_Y_OFFSET)
scale_group.append(alarm_1_value)

alarm_2_value = Label(FONT_1, text='0.0', color=color.GRAY, max_glyphs=10)
alarm_2_value.anchor_point = (1.0, 0.5)
alarm_2_value.anchored_position = (230+DISP_X_OFFSET, 100+DISP_Y_OFFSET)
scale_group.append(alarm_2_value)

up_graphic = Triangle(240+DISP_X_OFFSET, 110+DISP_Y_OFFSET, 260+DISP_X_OFFSET, 70+DISP_Y_OFFSET, 280+DISP_X_OFFSET, 110+DISP_Y_OFFSET,
                       fill=None, outline=color.GREEN)
scale_group.append(up_graphic)

down_graphic = Triangle(240+DISP_X_OFFSET, 160+DISP_Y_OFFSET, 260+DISP_X_OFFSET, 200+DISP_Y_OFFSET, 280+DISP_X_OFFSET, 160+DISP_Y_OFFSET,
                       fill=None, outline=color.GREEN)
scale_group.append(down_graphic)

# Define moveable bubble
indicator_group = displayio.Group()

chan_1_alarm_anchor = (102, 100)
chan_1_alarm = Triangle(chan_1_alarm_anchor[0]+DISP_X_OFFSET, chan_1_alarm_anchor[1]+DISP_Y_OFFSET,
                        chan_1_alarm_anchor[0]+5+DISP_X_OFFSET, chan_1_alarm_anchor[1]-5+DISP_Y_OFFSET,
                        chan_1_alarm_anchor[0]+5+DISP_X_OFFSET, chan_1_alarm_anchor[1]+5+DISP_Y_OFFSET,
                        fill=color.RED, outline=color.WHITE)
indicator_group.append(chan_1_alarm)

chan_2_alarm_anchor = (139, 140)
chan_2_alarm = Triangle(chan_2_alarm_anchor[0]+DISP_X_OFFSET, chan_2_alarm_anchor[1]+DISP_Y_OFFSET,
                        chan_2_alarm_anchor[0]-5+DISP_X_OFFSET, chan_2_alarm_anchor[1]-5+DISP_Y_OFFSET,
                        chan_2_alarm_anchor[0]-5+DISP_X_OFFSET, chan_2_alarm_anchor[1]+5+DISP_Y_OFFSET,
                        fill=color.RED, outline=color.WHITE)
indicator_group.append(chan_2_alarm)

chan_1_bubble = Circle(112+DISP_X_OFFSET, 200+DISP_Y_OFFSET, 8,
                       fill=color.YELLOW, outline=color.YELLOW, stroke=3)
indicator_group.append(chan_1_bubble)

chan_2_bubble = Circle(131+DISP_X_OFFSET, 200+DISP_Y_OFFSET, 8,
                       fill=color.GREEN, outline=color.GREEN, stroke=3)
indicator_group.append(chan_2_bubble)

scale_group.append(indicator_group)
display.show(scale_group)

def zero_channel():
    # Initiate internal calibration for current channel
    # Returns raw zero offset value
    # Use when scale is started, a new channel is selected or
    # to adjust for measurement drift
    # Remove weight and tare from load cell before executing
    print('channel %1d calibrate.INTERNAL: %5s'
          % (nau7802.channel, nau7802.calibrate('INTERNAL')))
    print('channel %1d calibrate.OFFSET:   %5s'
          % (nau7802.channel, nau7802.calibrate('OFFSET')))
    zero_offset = read(100)  # Average of 100 samples to establish zero offset
    print('...channel zeroed')
    return zero_offset

def read(samples=100):
    # Read and average consecutive raw sample values; return average raw value
    sum = 0
    for i in range(0, samples):
        if nau7802.available:
            sum = sum + nau7802.read()
    return int(sum / samples)

def play_tone(tone=None):
    if tone == 'high':
        pyportal.play_file('/tones/tone_high.wav', wait_to_finish=True)
    elif tone == 'low':
        pyportal.play_file('/tones/tone_low.wav', wait_to_finish=True)

# Instantiate and calibrate load cell inputs
print('*** Instantiate and calibrate load cells')
print(' enable NAU7802 digital and analog power: %5s' % (nau7802.enable(True)))

nau7802.gain = default.PGA_GAIN  # Use default gain
nau7802.channel = 1        # Set to second channel
chan_1_zero = zero_channel()  # Re-calibrate and get raw zero offset value
nau7802.channel = 2  # Set to first channel
chan_2_zero = zero_channel()  # Re-calibrate and get raw zero offset value

play_tone('high')
play_tone('low')

tare_1_mass_gr = round(default.TARE_1_MASS_GR, 1)
tare_2_mass_gr = round(default.TARE_2_MASS_GR, 1)
tare_1_enable = tare_2_enable = False

if tare_1_mass_gr != 0:
    tare_1_enable = True  # use default tare value on startup
if tare_2_mass_gr != 0:
    tare_2_enable = True  # use default tare value on startup

take_screenshot = True
# -- Main loop: Read sample, move bubble, and display values
while True:
    if tare_1_enable:
        tare_1_value.color = color.YELLOW
        tare_1_label.color = color.YELLOW
    else:
        tare_1_value.color = color.GRAY
        tare_1_label.color = color.GRAY
        tare_1_mass_gr = 0.0
    tare_1_value.text=str(tare_1_mass_gr)

    if tare_2_enable:
        tare_2_value.color = color.YELLOW
        tare_2_label.color = color.YELLOW
    else:
        tare_2_value.color = color.GRAY
        tare_2_label.color = color.GRAY
        tare_2_mass_gr = 0.0
    tare_2_value.text=str(tare_2_mass_gr)

    nau7802.channel = 1
    value = read(default.SAMPLE_AVG)
    chan_1_mass_gr = round((value - chan_1_zero) * default.CALIB_RATIO_1, 1) - tare_1_mass_gr
    chan_1_mass_oz = round(chan_1_mass_gr * 0.03527, 2)
    if str(chan_1_mass_gr) == '-0.0':  # Filter -0.0 value
        chan_1_mass_gr = 0.0
    chan_1_value.text = '%5.1f' % (chan_1_mass_gr)

    chan_1_bubble.y = int(map_range(chan_1_mass_gr, default.MIN_GR, default.MAX_GR, 239, 0)) - 8 + DISP_Y_OFFSET
    if chan_1_mass_gr > default.MAX_GR or chan_1_mass_gr < default.MIN_GR:
        chan_1_bubble.fill = color.RED
    else:
        chan_1_bubble.fill = None

    nau7802.channel = 2
    value = read(default.SAMPLE_AVG)
    chan_2_mass_gr = round((value - chan_2_zero) * default.CALIB_RATIO_2, 1) - tare_2_mass_gr
    chan_2_mass_oz = round(chan_2_mass_gr * 0.03527, 2)
    if str(chan_2_mass_gr) == '-0.0':  # Filter -0.0 value
        chan_2_mass_gr = 0.0
    chan_2_value.text      = '%5.1f' % (chan_2_mass_gr)

    chan_2_bubble.y  = int(map_range(chan_2_mass_gr, default.MIN_GR, default.MAX_GR, 239, 0)) - 8 + DISP_Y_OFFSET
    if chan_2_mass_gr > default.MAX_GR or chan_2_mass_gr < default.MIN_GR:
        chan_2_bubble.fill = color.RED
    else:
        chan_2_bubble.fill = None

    print('(%+5.1f, %+5.1f)' % (chan_1_mass_gr, chan_2_mass_gr))

    if pyportal.sd_check():
        if take_screenshot:
            print('Taking Screenshot...')
            save_pixels('/sd/screenshot.bmp')
            print('Screenshot taken')
            take_screenshot = False

    touch = pyportal.touchscreen.touch_point
    if touch:
        for button in buttons:
            if button.contains(touch):
                button.selected = True
                if button.name in ('zero_1', 'zero_2'):
                    # Zero and recalibrate channel
                    channel = int(button.name[5])
                    play_tone('high')
                    nau7802.channel = channel

                    if channel == 1:
                        chan_1_bubble.fill = color.RED
                        chan_1_zero = zero_channel()
                    else:
                        chan_2_bubble.fill = color.RED
                        chan_2_zero = zero_channel()

                    while pyportal.touchscreen.touch_point:
                        time.sleep(0.5)
                    if channel == 1:
                        chan_1_bubble.fill = None
                    else:
                        chan_2_bubble.fill = None
                    play_tone('low')

                if button.name in ('tare_1', 'tare_2'):
                    # get tare value for channel
                    channel = int(button.name[5])
                    play_tone('high')
                    nau7802.channel = channel
                    value = read(default.SAMPLE_AVG)

                    if channel == 1:
                        tare_1_enable = not tare_1_enable  # toggle tare 1 state
                        if tare_1_enable:
                            tare_1_mass_gr = round((value - chan_1_zero) * default.CALIB_RATIO_1, 1)
                            if str(tare_1_mass_gr) == '-0.0':  # Filter -0.0 value
                                tare_1_mass_gr = 0.0
                    else:
                        tare_2_enable = not tare_2_enable  # toggle tare 2 state
                        if tare_2_enable:
                            tare_2_mass_gr = round((value - chan_2_zero) * default.CALIB_RATIO_1, 1)
                            if str(tare_2_mass_gr) == '-0.0':  # Filter -0.0 value
                                tare_2_mass_gr = 0.0

                    while pyportal.touchscreen.touch_point:
                        time.sleep(0.5)
                    play_tone('low')

    zero_1_button.selected = False
    zero_2_button.selected = False
    tare_1_button.selected = False
    tare_2_button.selected = False
