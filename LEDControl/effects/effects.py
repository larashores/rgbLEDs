import colorsys
import random


class ColorConvert:
    @staticmethod
    def rgb_to_hsv(r, g, b):
        r /= 255
        g /= 255
        b /= 255
        colortup = colorsys.rgb_to_hsv(r, g, b)
        h = int(colortup[0]*255)
        s = int(colortup[1]*255)
        v = int(colortup[2]*255)
        return h, s, v

    @staticmethod
    def hsv_to_rgb(h, s, v):
        h /= 255
        s /= 255
        v /= 255
        colortup = colorsys.hsv_to_rgb(h, s, v)
        r = int(colortup[0]*255)
        g = int(colortup[1]*255)
        b = int(colortup[2]*255)
        return r, g, b


class SingleEffects:
    """
    Used for effects that only have to be updated once with no args
    """
    RATIO = (2/3)

    def __init__(self, main):
        self.main = main
        self.lastHue = 0

    def switch_all(self):
        """
        Switches all the leds at once
        """
        randhue = random.sample(set(range(self.lastHue-30)).union(range(self.lastHue+30, 255)), 1)[0]
        self.lastHue = randhue
        colortup = ColorConvert.hsv_to_rgb(randhue, 255, 255)
        self.main.change_all(colortup)
        self.main.update()

    def switch_some(self):
        """
        Switches the color os some of the leds, the rest remain off
        """
        n_rgbs = len(self.main.leds)
        max_leds = int(n_rgbs*self.RATIO)
        randhue = random.sample(set(range(self.lastHue-30)).union(range(self.lastHue+30, 255)), 1)[0]
        colortup = ColorConvert.hsv_to_rgb(randhue, 255, 255)
        leds = random.sample(set(range(n_rgbs)), max_leds)
        self.main.all_off()
        self.main.change_colors(leds, colortup)
        self.main.update()

    def dual_change(self):
        """
        Switches half of the colors to a certain color and half to another
        """
        n_rgbs = len(self.main.leds)
        nswitch = n_rgbs//2
        hue_1 = random.randint(0, 255)
        hue_2 = random.sample(set(range(hue_1-30)).union(range(hue_1+30, 255)), 1)[0]
        colortup1 = ColorConvert.hsv_to_rgb(hue_1, 255, 255)
        colortup2 = ColorConvert.hsv_to_rgb(hue_2, 255, 255)
        leds = set(range(n_rgbs))
        led_1 = random.sample(leds, nswitch)
        led_2 = random.sample(leds.difference(led_1), nswitch)
        self.main.change_colors(led_1, colortup1)
        self.main.change_colors(led_2, colortup2)
        self.main.update()


class ChangeLights:
    """
    Used for manipulating lights directly
    """
    def __init__(self, main):
        self.main = main

    def change_single(self, ind, colortup):
        self.main.single_change(ind, colortup)
        self.main.update()

    def change_multiple(self, inds, colortup):
        self.main.change_colors(inds, colortup)
        self.main.update()
