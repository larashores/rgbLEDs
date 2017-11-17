from saveable.composite import Composite
from saveable.SaveableChar import SaveableChar
from saveable.saveableInt import saveable_int
from saveable.saveableFloat import SaveableFloat
from saveable.saveableArray import saveable_array
from saveable.saveableString import SaveableString


class LightLocation(Composite):
    x = SaveableFloat
    y = SaveableFloat


class Light(Composite):
    random = SaveableChar
    r = saveable_int('u8')
    g = saveable_int('u8')
    b = saveable_int('u8')

    MAPPING = {'none': 'n', 'single': 'i', 'static': 's', 'pattern': 'p'}
    MAPPING.update(dict(reversed(item) for item in MAPPING.items()))

    def __init__(self):
        Composite.__init__(self)
        self.random = 'n'

    def get_random(self):
        return self.MAPPING[self.random]

    def set_random(self, rand):
        self.random = self.MAPPING[rand]

    def get_color(self):
        return [self.r, self.g, self.b]

    def set_color(self, colortup):
        self.r, self.g, self.b = colortup


class RunnerStep(Composite):
    lights = saveable_array(Light)

    def __init__(self, num=None):
        Composite.__init__(self)
        if num is not None:
            for _ in range(num):
                self.add_light()

    def __iter__(self):
        for light in self.lights:
            yield light

    def __str__(self):
        string = '('
        for ind, light in enumerate(self.lights):
            if light.get_color() != [0, 0, 0] or light.random != 'n':
                string += str(ind+1)+','
        string += ')'
        return string

    def add_light(self):
        light = Light()
        self.lights.append(light)

    def get_light(self, ind):
        return self.lights[ind]


class RunnerPattern(Composite):
    name = SaveableString
    lights = saveable_array(LightLocation)
    steps = saveable_array(RunnerStep)

    def __init__(self, num_lights=None):
        Composite.__init__(self)
        self.name = 'Untitled Pattern'
        if num_lights is not None:
            for _ in range(num_lights):
                self.lights.append(LightLocation())

    def __iter__(self):
        for step in self.steps:
            yield step

    def get_position(self, lightind):
        light = self.lights[lightind]
        return light.x, light.y

    def set_position(self, lightind, pos):
        light = self.lights[lightind]
        light.x, light.y = pos

    def add_step(self, ind):
        step = RunnerStep(len(self.lights))
        self.steps.insert(ind, step)

    def del_step(self, ind):
        self.steps.pop(ind)

    def get_step(self, ind):
        return self.steps[ind]
