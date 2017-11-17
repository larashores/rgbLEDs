import random
import time
from effects.effects import ColorConvert


class Patterns:
    """
    Stores Runner Patterns and connects to LEDInterface to display updates
    """
    def __init__(self, main):
        self.patterns = []
        self.run = True
        self.main = main
        self.wait = 0
        self.loop = 0
        self.loopForever = 0
        self.ignoreColors = 0

    def start(self, pattern):
        """
        Runs through a pattern and displays it
        """
        if self.loopForever:
            while self.loopForever and self.run:
                self.do_run(pattern)
            return
        for x in range(self.loop):
            if self.run:
                self.do_run(pattern)
            else:
                return

    def do_run(self, pattern):
        """
        Runs through a pattern and displays it
        """
        pattern_hue = random.randint(0, 255)
        pattern_color = ColorConvert.hsv_to_rgb(pattern_hue, 255, 255)
        for step in pattern.stops:
            if not self.run:
                return
            step_hue = random.randint(0, 255)
            step_color = ColorConvert.hsv_to_rgb(step_hue, 255, 255)
            for ind, light in enumerate(step.lights):
                if light.random == 'single':
                    hue = random.randint(0, 255)
                    color = ColorConvert.hsv_to_rgb(hue, 255, 255)
                elif light.random == 'static':
                    color = step_color
                elif light.random == 'pattern':
                    color = pattern_color
                else:
                    color = light.get_color()
                if self.ignoreColors:
                    if not color == [0, 0, 0]:
                        color = self.defaultColor

                self.main.single_change(ind, color)
            self.main.update()
            time.sleep(self.wait)
        self.main.all_off()
        self.main.update()
