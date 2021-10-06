# scale_config.py

class Defaults:
    MAX_GR       = 100  # Maximum (full-scale) display range in grams
    PGA_GAIN     = 128  # Default gain for internal PGA
    SAMPLE_AVG   = 100  # Number of sample values to average
    CHAN_1_NAME = 'CELL_A'  # 6 characters maximum
    CHAN_2_NAME = 'CELL_B'  # 6 characters maximum
    TARE_1_MASS_GR  = 6.4
    TARE_2_MASS_GR  = 0.0
    ALARM_1_MASS_GR = 0.0
    ALARM_2_MASS_GR = 0.0

    # Calculate minimum scale value based on default maximum value
    MIN_GR = ((MAX_GR // 5) * -1)

    # Load cell calibration ratio; ADC_raw_measurement
    # Obtained emperically; individual load cell dependent
    _CHAN_1_RAW_VALUE = 215300  # 100g at gain x128 for load cell serial#4540-01
    _CHAN_1_TEST_MASS_GR = 100

    _CHAN_2_RAW_VALUE = 215300  # 100g at gain x128 for load cell serial#4540-02
    _CHAN_2_TEST_MASS_GR = 100

    CALIB_RATIO_1 = _CHAN_1_TEST_MASS_GR / _CHAN_1_RAW_VALUE
    CALIB_RATIO_2 = _CHAN_2_TEST_MASS_GR / _CHAN_2_RAW_VALUE


class ScalePalette:
    # Define a few colors (https://en.wikipedia.org/wiki/Web_colors)
    BLACK     = 0x000000
    RED       = 0xFF0000
    RED_DK    = 0xA00000
    YELLOW    = 0xFFFF00
    YELLOW_DK = 0x202000
    CYAN      = 0x00FFFF
    BLUE      = 0x0000FF
    BLUE_DK   = 0x000080
    WHITE     = 0xFFFFFF
    ORANGE    = 0xFFA500
    GREEN     = 0x00FF00
    GRAY      = 0x508080
    PURPLE    = 0x800080
    MAROON    = 0x800000
