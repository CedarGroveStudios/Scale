# Scale -- _Version 3.0_

### A configurable dual loadcell scale utilizing the CedarGrove NAU7802 FeatherWing. Code is written in CircuitPython and tested with CircuitPython version 7.3.2.

Mass measurements from two loadcell sensors are processed by the CedarGrove NAU7802 precision ADC FeatherWing and displayed graphically on an Adafruit PyPortal, PyPortal Pynt, PyPortal Titano, or RP2040 Feather + TFT FeatherWing. Each channel's display mass values within the range of the loadcell are displayed in Grams, including negative values. Tare and alarm levels are user-specified and selectively enabled as needed.

Default operational parameters are specified in the `scale_defaults.py` file in the microcontroller's root directory. Scale’s graphics and touchscreen zones are display size independent. Built-in board size is automatically detected; other displays are user-specified in the `scale_defaults.py` file. Font sizes do not scale proportionally but adjust somewhat to display size. Tare and alarm settings are stored in the microcontroller's non-volatile memory (NVM) to be recalled upon power-up. To facilitate testing, the code will simulate a missing custom loadcell FeatherWing board.

![Pyportal Scale](https://github.com/CedarGroveStudios/Scale/blob/main/media/pyportal_v20_social.png)

Touching a tare or alarm icon for one second or less (then released after the first beep) toggles the tare or alarm on/off. Touch and hold the icon until the second beep to set the tare/alarm value with the current Scale measurement. Setting the value will be confirmed with two beeps and an on-screen message; errors are three beeps with an on-screen warning message. The updated tare/alarm values and settings are then stored in NVM. Stored settings will be used the next time the Scale is powered on.

Changed tare/alarm settings will be remembered if power is removed. To clear the current settings and revert to the default tare/alarm settings (as recorded in the scale_defaults.py file), touch and hold the area at the top center of the display.

For testing and compatibility checks, the scale will function without the CedarGrove NAU7802 FeatherWing. Measured values are simulated if the Wing is not connected.

On-screen touch areas (button outlines) can be displayed by changing the `debug = True` to `debug = False` in the `scale_code.py` file.

![Pyportal Scale Screenshot](https://github.com/CedarGroveStudios/Scale/blob/main/media/johns_scale.png)

Acknowledgements: Thank you to @siddacious and @foamyguy for educational and very helpful coding examples. Big thanks to @foamyguy for the NVM helper library.

_CedarGroveStudios/Scale v3.0_
