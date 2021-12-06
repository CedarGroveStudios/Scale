# Scale -- _Version 2.0-Alpha_

### A configurable dual loadcell scale utilizing the CedarGrove NAU7802 FeatherWing for the Adafruit PyPortal. Code is written in CircuitPython.

Mass measurements from two loadcell sensors are processed by the CedarGrove NAU7802 precision ADC FeatherWing and displayed graphically on an Adafruit PyPortal, PyPortal Pynt, or PyPortal Titano. Each channel's display mass values within the range of the loadcell are displayed in Grams, including negative values. Tare and alarm levels are user-specified and selectively enabled as needed.

Default operational parameters are specified in the `scale_defaults.py` file in the PyPortal's root directory. Scale on-screen graphics and fonts are automatically sized and positioned based upon detected PyPortal display characteristics.

![Pyportal Scale](https://github.com/CedarGroveStudios/Scale/blob/main/photos_and_graphics/pyportal_v20_social.png)

Touching a tare or alarm icon for one second or less (then released after the first beep) toggles it on/off. Touch and hold the icon until the second beep to set the tare/alarm value with the current Scale measurement. Setting the value will be confirmed with two beeps and an on-screen message; errors are three beeps with an on-screen warning message. The updated tare/alarm values and settings are then stored on the SD card (if installed). Stored settings will be used the next time the Scale is powered on.

Using an SD card will allow changed tare/alarm settings to be remembered if power is removed. To clear the SD card settings and reset to default tare/alarm settings (as recorded in the scale_defaults.py file), touch and hold the area at the top center of the display.

For testing and compatibility checks, the v2.0-Alpha code will function without the CedarGrove NAU7802 FeatherWing; the measured values are simulated if the Wing is not connected.

On-screen touch areas (buttons) are outlined in the v2.0-Alpha version. Changing the `code.py` line 24 `debug = True` to `debug = False` will remove the button outlines.

![Pyportal Scale Screenshot](https://github.com/CedarGroveStudios/Scale/blob/main/photos_and_graphics/johns_scale.png)

Acknowledgements: Thank you to @siddacious and @foamyguy for educational and very helpful coding examples.

_CedarGroveStudios/Scale v2.0-Alpha_
