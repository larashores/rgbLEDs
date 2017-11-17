import os

from .model import *
from .fileio import save, load

from utilities.constants import *


class Controller:
    def new_pattern(self, num_lights):
        self.pattern = RunnerPattern(num_lights)

    def get_pattern(self):
        return self.pattern

    def get_light(self, stepind, lightind):
        return self.pattern.get_step(stepind).get_light(lightind)

    def exists(self):
        _dir = os.path.join(PATTERN_DIR, self.get_name()+'.pattern')
        if os.path.exists(_dir):
            return True
        else:

            return False

    def save_pattern(self):
        """
        Saves the pattern to data folder in current directory
        """
        _dir = os.path.join(PATTERN_DIR, self.get_name()+'.pattern')
        save(self.pattern, _dir)

    def load_pattern(self, name):
        self.pattern = load(os.path.join(PATTERN_DIR, name+'.pattern'))

    def len_steps(self):
        return len(self.pattern.steps)

    def get_num_lights(self):
        return len(self.pattern.lights)

    def add_step(self, ind):
        self.pattern.add_step(ind)

    def del_step(self, ind):
        self.pattern.del_step(ind)

    def get_step(self, ind):
        return self.pattern.get_step(ind)

    def set_pos(self, lightind, pos):
        self.pattern.set_position(lightind, pos)

    def get_pos(self, lightind):
        pos = self.pattern.get_position(lightind)
        return pos

    def get_random(self, stepind, lightind):
        light = self.get_light(stepind, lightind)
        return light.get_random()

    def set_random(self, stepind, lightind, rand):
        light = self.get_light(stepind, lightind)
        light.set_random(rand)

    def set_color(self, stepind, lightind, colortup):
        light = self.get_light(stepind, lightind)
        light.set_color(colortup)

    def get_color(self, stepind, lightind):
        """
        Gets the color of a light in a step
        """
        light = self.get_light(stepind, lightind)
        return light.get_color()

    def set_name(self, name):
        """
        Sets the name of the pattern
        """
        self.pattern.name = name

    def get_name(self):
        """
        Gets the name of the pattern
        """
        return self.pattern.name
