# cedargrove_scale\defaults.py

class Configuration:

    BRIGHTNESS  = 0.1  # Display brightness, 0 to 1.0; 0.75 typical, 0.1 for photos

    MAX_GR       = 100  # Maximum (full-scale) display range in grams
    MIN_GR       =   0  # Miminum of display range in grams

    CHAN_1_NAME = 'CELL_A'  # 6 characters maximum
    CHAN_2_NAME = 'CELL_B'  # 6 characters maximum

    TARE_1_MASS_GR  =   6.4  # Channel 1 startup tare value; zero to disable
    TARE_2_MASS_GR  =   0.0  # Channel 2 startup tare value; zero to disable
    ALARM_1_MASS_GR =   0.0  # Channel 1 startup alarm value; zero to disable
    ALARM_2_MASS_GR =  50.0  # Channel 1 startup alarm value; zero to disable

    MASS_UNITS = 'GRAMS'  # Mass units of either GRAMS or OUNCE; limited to 5 char
