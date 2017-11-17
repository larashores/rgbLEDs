import tkinter as tk
from tkinter import ttk
from tkinter import GROOVE, LEFT, RIGHT, X, Y, BOTH, YES, HORIZONTAL, BOTTOM
from tkinter.colorchooser import askcolor

from gui.barrier import Barrier
from gui.runnerPatterns import RunnerPatterns
from gui.labeledScale import LabeledScale
from utilities.constants import *


class MainWindow(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        title_frame = tk.Frame(self, bg=B_COLOR, borderwidth=3, relief=GROOVE)
        mid_frm = ttk.Frame(self)
        top_mid = ttk.Frame(mid_frm)

        title = ttk.Label(title_frame, borderwidth=3, text='LED Lights', style='Title.TLabel')
        some = ChangeSome(self, controller, borderwidth=3, relief=GROOVE)
        beat = BeatDetect(top_mid, controller, borderwidth=3, relief=GROOVE)
        pattern = RunnerPatterns(top_mid, controller, borderwidth=3, relief=GROOVE)
        singles = SingleEffects(self, controller, borderwidth=3, relief=GROOVE)
        strobe = Strobe(mid_frm, controller, borderwidth=3, relief=GROOVE)
        individual = ChangeSingle(self, controller, borderwidth=3, relief=GROOVE)

        title_frame.pack(fill=X)
        title.pack()

        individual.pack(side=BOTTOM, fill=X)
        some.pack(side=LEFT, fill=Y)
        mid_frm.pack(side=LEFT, expand=YES, fill=BOTH)

        top_mid.pack(expand=YES, fill=BOTH)
        beat.pack(side=LEFT, expand=YES, fill=BOTH)
        pattern.pack(side=LEFT, expand=YES, fill=BOTH)

        strobe.pack(expand=YES, fill=BOTH)
        singles.pack(side=RIGHT, fill=BOTH)


class ChangeSingle(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, bg=B_COLOR, **kwargs)
        self.controller = controller
        for ind in range(6):
            frm = ttk.Frame(self)
            frm.pack(side=LEFT, expand=YES, fill=X)
            but = tk.Button(frm, text=str(ind+1), font=SINGLE_FONT, width=3, command=lambda i=ind: self.change(i))
            but.pack(padx=5, pady=5)

    def change(self, ind):
        rgb = askcolor()[0]
        if rgb is not None:
            self.controller.change_single(ind, rgb)


class SingleEffects(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, bg=B_COLOR, **kwargs)
        ttk.Label(self, text='Single Effects', style='Subtitle.TLabel').pack()
        for type_, name in (('changeall', 'Change All'),
                            ('changesome', 'Change Some'),
                            ('dualchange', 'Dual Change')):
            but = tk.Button(self, text=name, font=EFFECT_FONT, command=controller.s_effects[type_])
            but.pack(expand=YES, fill=X, pady=5, padx=15)


class ChangeSome(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, bg=B_COLOR, **kwargs)
        ttk.Label(self, text='Change Multiple', style='Subtitle.TLabel').pack()
        self.controller = controller
        self.checkVars = []
        for ind in range(6):
            var = tk.IntVar()
            self.checkVars.append(var)
            tk.Checkbutton(self, text='LED '+str(ind+1), bg=B_COLOR, fg='grey',
                           activebackground='grey', selectcolor=B_COLOR, font=CHK_FONT,
                           variable=var).pack(expand=YES, fill=BOTH)
        tk.Button(self, text='Change Color',
                  font=CHK_FONT[:2]+('normal',), command=self.change).pack(padx=5, pady=(5, 20))

    def change(self):
        rgb = askcolor()[0]
        led_inds = []
        for ind, var in enumerate(self.checkVars):
            if var.get() == 1:
                led_inds.append(ind)
        self.controller.change_multiple(led_inds, rgb)


class Strobe(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, bg=B_COLOR, **kwargs)
        self.controller = controller
        ttk.Label(self, text='Strobe', style='Subtitle.TLabel').pack()
        option_frm = ttk.Frame(self)
        option_frm.pack(side=BOTTOM, expand=YES)
        frm = ttk.Frame(option_frm)
        frm.pack(fill=BOTH)
        ttk.Label(frm, text='Hertz:').pack(side=LEFT)
        scroll = tk.Scale(frm, command=self.change_freq, from_=1, to=60, resolution=1,
                          bg=B_COLOR, fg=F_COLOR, orient=HORIZONTAL)
        scroll.pack(expand=YES, fill=X, side=RIGHT, padx=(0, 40))
        but_frame = ttk.Frame(option_frm)
        but_frame.pack(fill=Y, pady=20)
        tk.Button(but_frame, command=controller.start_strobe,
                  text='Start', width=5, font=EFFECT_FONT).pack(padx=(0, 10), side=LEFT)
        tk.Button(but_frame, command=controller.stop_strobe,
                  text='End', width=5, font=EFFECT_FONT).pack(padx=(10, 0), side=LEFT)

    def change_freq(self, freq):
        self.controller.change_freq(int(freq))


class BeatDetect(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, bg=B_COLOR, **kwargs)
        self.controller = controller
        self.max_freq = 300
        self.s_freq = 40
        self.e_freq = 150
        self.keep_amount = 10
        self.percent = .5
        self.wait_time = .5
        ttk.Label(self, text='Beat Detection', style='Subtitle.TLabel').pack(fill=X)
        # ------Setting up sliders---------
        top_group = ttk.Frame(self)
        top_group.pack(expand=YES, fill=BOTH)
        left_frm = ttk.Frame(top_group)
        right_frm = ttk.Frame(top_group)
        bottom_frm = ttk.Frame(self)
        bottom_frm.pack(expand=YES, fill=BOTH)
        left_frm.pack(side=LEFT, expand=YES, fill=BOTH)
        right_frm.pack(side=RIGHT, expand=YES, fill=BOTH)
        # ----------------------Left Frame stuff---------------------
        self.percentScale = LabeledScale(left_frm, text='Percent Difference', length=150,
                                         from_=0, to=1, resolution=.01,
                                         command=self.change_percent,
                                         orient=HORIZONTAL)
        self.percentScale.set(self.percent)
        self.percentScale.pack(expand=YES, fill=X, pady=(0, 10), padx=(20, 10))
        Barrier(left_frm).pack(expand=YES, fill=X, padx=10)
        self.waitScale = LabeledScale(left_frm, text='Wait Time', length=150,
                                      from_=0, to=1, resolution=.1,
                                      command=self.change_wait,
                                      orient=HORIZONTAL)
        self.waitScale.set(self.wait_time)
        self.waitScale.pack(expand=YES, fill=X, pady=(0, 10), padx=(20, 10))
        # ----------------------Right Frame stuff----------------------
        self.startScale = LabeledScale(right_frm, text='Start Frequency', length=150,
                                       from_=0, to=self.max_freq, resolution=10,
                                       command=self.change_start,
                                       orient=HORIZONTAL)
        self.startScale.set(self.s_freq)
        self.startScale.pack(expand=YES, fill=X, pady=(0, 10), padx=(10, 20))
        Barrier(right_frm).pack(expand=YES, fill=X, padx=10)
        self.endScale = LabeledScale(right_frm, length=150,
                                     text='End Frequency',
                                     from_=self.s_freq, to=self.max_freq, resolution=10,
                                     command=self.change_end,
                                     orient=HORIZONTAL)
        self.endScale.set(self.e_freq)
        self.endScale.pack(expand=YES, fill=X, pady=(0, 10), padx=(10, 20))
        # ---------------------Bottom frame stuff------------------------
        Barrier(bottom_frm).pack(expand=YES, fill=X, padx=10)
        self.bufferScale = LabeledScale(bottom_frm, text='Magnitude Buffer Size',
                                        from_=0, to=20, resolution=1,
                                        command=self.change_buffer,
                                        orient=HORIZONTAL)
        self.bufferScale.set(self.keep_amount)
        self.bufferScale.pack(side=BOTTOM, expand=YES, fill=X, pady=(0, 10), padx=20)
        # ------------------------------
        but_frame = ttk.Frame(self)
        but_frame.pack(pady=(10, 20), expand=YES, fill=Y)
        tk.Button(but_frame, command=self.controller.start_beat_detect,
                  text='Start', width=5, font=EFFECT_FONT).pack(side=LEFT, padx=(0, 10))
        tk.Button(but_frame, command=self.controller.stop_beat_detect,
                  text='End', width=5, font=EFFECT_FONT).pack(side=RIGHT, padx=(10, 0))

    def change_percent(self, num):
        self.controller.change_fft('percent', float(num))

    def change_wait(self, num):
        self.controller.change_fft('wait_time', float(num))

    def change_buffer(self, num):
        self.controller.change_fft('keep_amount', int(num))

    def change_start(self, num):
        self.endScale.config(from_=num)
        self.controller.change_fft('s_freq', int(num))

    def change_end(self, num):
        self.controller.change_fft('e_freq', int(num))