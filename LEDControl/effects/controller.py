from effects.fftAnalyze import FFTAnalyze
from effects.effects import SingleEffects, ChangeLights
from effects.patterns import Patterns
from effects.strobe import Strobe
from serialout.ledInterface import LEDControl

import threading


class Controller:
    def __init__(self):
        self.interface = None #LEDControl()
        self.singles = SingleEffects(self.interface)
        self.change = ChangeLights(self.interface)
        self.s_effects = {'changeall': self.singles.switch_all,
                          'changesome': self.singles.switch_some,
                          'dualchange': self.singles.dual_change}
        self.analyze = FFTAnalyze(self.s_effects['changeall'])
        self.strobe = Strobe(self.interface)
        self.runner = Patterns(self.interface)

    def change_single(self, index, colortup):
        self.change.change_single(index, colortup)

    def change_mltiple(self, indtup, colortup):
        self.change.change_multiple(indtup, colortup)

    def start_beat_detect(self):
        self.analyze.run = True
        t = threading.Thread(target=self.analyze.start, daemon=True)
        t.start()

    def stop_beat_detect(self):
        self.analyze.run = False

    # ===============-----------------------------Runner Settings--------------------===================================
    def start_runner_pattern(self, pattern):
        self.runner.run = True
        t = threading.Thread(target=lambda: self.runner.start(pattern), daemon=True)
        t.start()

    def stop_runner_pattern(self):
        self.runner.run = False

    def change_speed(self, num):
        self.runner.wait = num/1000

    def change_loop(self, num):
        self.runner.loop = num

    def set_infinite(self, val):
        self.runner.loopForever = val

    def change_ignore(self, val):
        self.runner.ignoreColors = val

    def set_default_color(self, col):
        self.runner.defaultColor = col

    # ===================================================================================================================
    def start_strobe(self):
        self.strobe.run = True
        t = threading.Thread(target=self.strobe.start, daemon=True)
        t.start()

    def stop_strobe(self):
        self.strobe.run = False

    def change_freq(self, freq):
        self.strobe.freq = freq

    def end(self):
        self.stop_beat_detect()
        self.stop_strobe()

    def change_fft(self, attr, num):
        """
        Changes attr of the fft
        Choices are: s_freq
                     e_freq
                     keep_amount
                     percent
                     wait_time
        """
        setattr(self.analyze, attr, num)
