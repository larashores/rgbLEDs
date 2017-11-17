# rgbLEDs
Code for controlling multiple RGB LED lights with an arduino and WS2803 chip

A python GUI in LEDControl is used to send commands to an Arduino which simply fowards it along to the WS2803. It would be possible to control directly from the computer but some annoying connector would need to be made. The Arduino code is in ArduinoLEDs. The arduino pins 5 and 6 are used for clock and data respectivly. The arduino and WS2803 should be powered by the same external power supply.

Images of the GUI and pattern editor:

<img src="https://raw.githubusercontent.com/vinceshores/rgbLEDs/master/images/mainwindow.PNG" width="400"> <img src="https://raw.githubusercontent.com/vinceshores/rgbLEDs/master/images/patterneditor.PNG" width="300">

Image of WS2803 chip:

<img src="https://raw.githubusercontent.com/vinceshores/rgbLEDs/master/images/chip.PNG" width="300">

Finally a really bad image of the lights in action:

<img src="https://raw.githubusercontent.com/vinceshores/rgbLEDs/master/images/lights.PNG" width="300">
