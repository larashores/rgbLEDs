import time
import serial

nRGBs = 6


class LED:
    def __init__(self):
        self.red = 0
        self.green = 0
        self.blue = 0

    def change_color(self, colortup):
        """
        Changes led colors based on colortup
        """
        if not colortup:
            return
        self.red = int(colortup[0])
        self.blue = int(colortup[1])
        self.green = int(colortup[2])

    def off(self):
        """
        Turns the led off
        """
        self.change_color((0, 0, 0))


class LEDControl:
    """
    Provides a link to the SerialInterface, and has methods to manipulate
    LED colors based on an RGB color tuple
    """
    def __init__(self):
        self.ser = SerialInterface()
        self.leds = []
        self.savedColors = []
        for num in range(nRGBs):
            self.leds.append(LED())
        time.sleep(3)               # Wait for serial port to set up
        self.update()

    def single_change(self, index, colortup):
        """
        Changes color of the led index given
        """
        self.change_colors((index,), colortup)

    def change_colors(self, lednums, colortup):
        """
        Changes a list of leds to the colortup and up. Does not update
        """
        for lednum in lednums:
            led = self.leds[lednum]
            led.change_color(colortup)

    def save_color(self):
        self.savedColors.clear()
        for led in self.leds:
            self.savedColors.append([led.red, led.blue, led.green])

    def send_saved(self):
        for ind, led in enumerate(self.leds):
            led.red = self.savedColors[ind][0]
            led.blue = self.savedColors[ind][1]
            led.green = self.savedColors[ind][2]
        self.ser.update(self.leds)

    def all_off(self):
        """
        Turns all the LEDS off, does not update
        """
        for led in self.leds:
            led.off()

    def change_all(self, colortup):
        """
        Changes the color of all leds, doesnt update
        """
        to_change = list(range(len(self.leds)))
        self.change_colors(to_change, colortup)

    def update(self):
        self.ser.update(self.leds)


class SerialInterface:
    def __init__(self):
        self.ser = serial.Serial(port=3, baudrate=9600)
        self.savedColors = None

    def get_values(self, leds):
        """
        Returns bytearray of led colors to send
        based on leds list
        """
        valuebytes = bytearray()
        for led in leds:
            valuebytes.append(led.red)
            valuebytes.append(led.blue)
            valuebytes.append(led.green)
        return valuebytes

    def update(self, leds):
        """
        Updates the leds through the serial port
        Takes a list of LED objects
        """
        values = self.get_values(leds)
        self.send_values(values)

    def send_values(self, values):
        for num in range(len(values)):
            value = bytes(values[num:num+1])        # Pass bytes a list not int
            self.ser.write(value)
