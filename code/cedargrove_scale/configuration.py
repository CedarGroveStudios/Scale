# cedargrove_scale\configuration.py
import board

class Configuration:
    SAMPLE_AVG = 100  # Number of samples to average per measurement

    PGA_GAIN   = 128  # Default gain for internal PGA

    # Load cell calibration ratio; ADC_raw_measurement
    # Obtained emperically; individual load cell dependent
    _CHAN_1_RAW_VALUE    = 215300  # 100g at gain x128 for load cell serial#4540-01
    _CHAN_1_TEST_MASS_GR =    100

    _CHAN_2_RAW_VALUE    = 215300  # 100g at gain x128 for load cell serial#4540-02
    _CHAN_2_TEST_MASS_GR =    100

    CALIB_RATIO_1 = _CHAN_1_TEST_MASS_GR / _CHAN_1_RAW_VALUE
    CALIB_RATIO_2 = _CHAN_2_TEST_MASS_GR / _CHAN_2_RAW_VALUE

class Screen:
    # Determine display and object sizes
    WIDTH = board.DISPLAY.width
    HEIGHT = board.DISPLAY.height

class Dial:
    RADIUS = int(Screen.HEIGHT * 1/4)
    CENTER = (Screen.WIDTH // 2, Screen.HEIGHT // 2)

class Pointer:
    STROKE = 2
    DIAMETER = int((Screen.HEIGHT * 1/32) + (2 * STROKE))
    RADIUS = DIAMETER // 2
    OUT_PATH_RADIUS = Dial.RADIUS - DIAMETER
    IN_PATH_RADIUS = Dial.RADIUS - (2 * DIAMETER)

class Palette:
    # Define a few colors (https://en.wikipedia.org/wiki/Web_colors)
    BLACK     = 0x000000
    CYAN      = 0x00FFFF
    BLUE      = 0x0000FF
    BLUE_DK   = 0x000080
    GRAY      = 0x508080
    GREEN     = 0x00FF00
    MAROON    = 0x800000
    ORANGE    = 0xFFA500
    PURPLE    = 0x800080
    RED       = 0xFF0000
    RED_DK    = 0xA00000
    YELLOW    = 0xFFFF00
    YELLOW_DK = 0x202000
    WHITE     = 0xFFFFFF
