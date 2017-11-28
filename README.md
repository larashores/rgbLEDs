# rgbLEDs
Code for controlling multiple RGB LED lights with an arduino and WS2803 chip

A python GUI in LEDControl is used to send commands to an Arduino which simply fowards it along to the WS2803. It would be possible to control directly from the computer but some annoying connector would need to be made. The Arduino code is in ArduinoLEDs. The arduino pins 5 and 6 are used for clock and data respectivly. The arduino and WS2803 should be powered by the same external power supply.

Included features are manually changing the color of one or more lights, having the lights change automatically due to beat detection in music, using a predefined pattern to light the LEDs in a specific order and time period, strobing the lights using their current colors, or selecting predefined effects. The predefined effects randomly change all lights to a specific color, randomly change 2/3 of the lights to a color and leave the rest off, or randomly change half of the lights to one color and half of the lights to another color.

Images of the GUI and pattern editor:

<img src="https://raw.githubusercontent.com/vinceshores/rgbLEDs/master/images/mainwindow.PNG" width="400"> <img src="https://raw.githubusercontent.com/vinceshores/rgbLEDs/master/images/patterneditor.PNG" width="300">

Image of WS2803 chip:

<img src="https://raw.githubusercontent.com/vinceshores/rgbLEDs/master/images/chip.PNG" width="300">

Finally a really bad image of the lights in action:

<img src="https://raw.githubusercontent.com/vinceshores/rgbLEDs/master/images/lights.PNG" width="300">
