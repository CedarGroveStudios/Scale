# Load Cell Calibrator
# Cedar Grove NAU7802 FeatherWing
# 2021-04-21 v02 Cedar Grove Studios

import board
import time

# from   adafruit_clue                  import clue
import displayio
from cedargrove_nau7802 import NAU7802

SAMPLE_AVG = 1000  # Number of sample values to average
DEFAULT_GAIN = 128  # Default gain for internal PGA

# Instantiate 24-bit load sensor ADC
nau7802 = NAU7802(board.I2C(), address=0x2A, active_channels=2)


def zero_channel():
    # Initiate internal calibration for current channel; return raw zero offset value
    # Use when scale is started, a new channel is selected, or to adjust for measurement drift
    # Remove weight and tare from load cell before executing
    print(
        'channel %1d calibrate.INTERNAL: %5s'
        % (nau7802.channel, nau7802.calibrate('INTERNAL'))
    )
    print(
        'channel %1d calibrate.OFFSET:   %5s'
        % (nau7802.channel, nau7802.calibrate('OFFSET'))
    )
    zero_offset = read(100)  # Read average of 100 samples to establish zero offset
    print('...channel zeroed')
    return zero_offset


def read(samples=100):
    # Read and average consecutive raw sample values; return average raw value
    sum = 0
    for i in range(0, samples):
        if nau7802.available:
            sum = sum + nau7802.read()
    return int(sum / samples)


# Instantiate and calibrate load cell inputs
print('*** Instantiate and calibrate load cells')
print('    enable NAU7802 digital and analog power: %5s' % (nau7802.enable(True)))

nau7802.gain = DEFAULT_GAIN  # Use default gain
nau7802.channel = 1
zero = zero_channel()  # Calibrate and get raw zero offset value
nau7802.channel = 2
zero = zero_channel()  # Calibrate and get raw zero offset value

print('GAIN:', DEFAULT_GAIN)
print('Place the calibration weight on the load cell')
print('To re-zero the load cells, remove all weights and press reset')

### Main loop: Read load cells and display raw values
#     Monitor Zeroing button
while True:
    print('=====')
    nau7802.channel = 1
    value = read(SAMPLE_AVG)
    print(
        'CHAN_%1.0f RAW VALUE: %7.0f  Percent of full-scale at gain x%3.0f : %3.2f: '
        % (nau7802.channel, value, DEFAULT_GAIN, (value / ((2 ** 23) - 1)) * 100)
    )

    nau7802.channel = 2
    value = read(SAMPLE_AVG)
    print(
        'CHAN_%1.0f RAW VALUE: %7.0f  Percent of full-scale at gain x%3.0f : %3.2f: '
        % (nau7802.channel, value, DEFAULT_GAIN, (value / ((2 ** 23) - 1)) * 100)
    )

    time.sleep(0.1)
