import tkinter as tk
from tkinter import ttk
from tkinter.colorchooser import askcolor
import os

from gui.labeledScale import LabeledScale
from utilities.listchoice import ListChoice
from gui.barrier import Barrier
from runnerEditor import runners
from utilities.constants import *
from runnerEditor.model.fileio import load


class RunnerPatterns(tk.Frame):
    def __init__(self, parent, controller, **kwargs):
        tk.Frame.__init__(self, parent, bg=B_COLOR, **kwargs)
        self.controller = controller
        ttk.Label(self, text='LED Runner Patterns', style='Subtitle.TLabel').pack(pady=(0, 10))
        self.curPattern = 0
        self.speed = 0
        self.loop = 0               # Amount of times to loop
        self.ignoreVar = tk.IntVar()
        self.loopVar = tk.IntVar()     # Loop forever
        # ============================--------List box and pattern edit creation--------==========================
        self.lbox = ListChoice(self, update_cmd=self.set_cur_pattern, delete_cmd=self.del_pattern,
                               height=6, background='black', foreground='white')
        self.lbox.bind('<Double-Button-1>', self.double_cick)

        pat = ttk.Frame(self,)
        tk.Button(pat, command=self.add_pattern,
                  text='Add', bg=B_COLOR, fg=F_COLOR,
                  font=SMALL_FONT,
                  width=7).pack(side=tk.LEFT, padx=(15, 15))
        tk.Button(pat, command=self.del_pattern,
                  text='Delete', bg=B_COLOR, fg=F_COLOR,
                  font=SMALL_FONT,
                  width=7).pack(side=tk.LEFT, padx=(15, 15))
        # ===========================--------Run Settings creation-------------===============================
        settings = ttk.Frame(self)
        chks = ttk.Frame(settings)
        chks.pack()
        tk.Checkbutton(chks, text='Ignore Colors', command=self.change_ignore, variable=self.ignoreVar,
                       bg=B_COLOR, fg='grey', activebackground='grey', selectcolor=B_COLOR).pack(side=tk.LEFT)
        tk.Checkbutton(chks, text='Loop Forever', command=self.loop_forever, variable=self.loopVar,
                       bg=B_COLOR, fg='grey', activebackground='grey', selectcolor=B_COLOR).pack(side=tk.LEFT)

        scales = ttk.Frame(self)
        LabeledScale(scales, command=self.change_loop, text='Loop Amount',
                     from_=1, to=10, resolution=1,
                     orient=tk.HORIZONTAL).pack(expand=tk.YES, fill=tk.X, side=tk.LEFT, padx=(10, 5))

        scl = LabeledScale(scales, command=self.change_speed, text='Time (ms)',
                           from_=0, to=300, resolution=10,
                           orient=tk.HORIZONTAL)
        scl.set(100)
        scl.pack(side=tk.LEFT, padx=(5, 10), expand=tk.YES, fill=tk.X)
        # ============================-------Activator Buttons-------------===========================
        act = tk.Frame(self, bg=B_COLOR)
        tk.Button(act, text='Start', command=self.start_runner,
                  font=EFFECT_FONT, width=5).pack(side=tk.LEFT, padx=(20, 10))
        self.col = tk.Button(act, command=self.change_color,
                             text='Color', bg='blue', fg='grey',
                             font=EFFECT_FONT,
                             width=5)
        self.col.pack(side=tk.LEFT, padx=10)
        tk.Button(act, command=self.stop_runner,
                  text='End',
                  font=EFFECT_FONT,
                  width=5).pack(side=tk.LEFT, padx=(10, 20))
        self.lbox.pack(expand=tk.YES, fill=tk.BOTH, padx=(20, 10))
        pat.pack(pady=(10, 0))
        Barrier(self).pack(expand=tk.YES, fill=tk.X, padx=20, pady=(8, 2))
        settings.pack()
        scales.pack(expand=tk.YES, fill=tk.X)
        act.pack(pady=20)

        self.load_patterns()
        self.controller.set_default_color([0, 0, 255])

    def start_runner(self):
        pattern = load(os.path.join(PATTERN_DIR, self.lbox.choices()[self.curPattern]+'.pattern'))
        self.controller.start_runner_pattern(pattern)

    def stop_runner(self):
        self.controller.stop_runner_pattern()

    def add_pattern(self):
        runners.new_pattern(self.load_patterns)

    def change_loop(self, num):
        self.controller.change_loop(int(num))

    def loop_forever(self):
        self.controller.set_infinite(self.loopVar.get())

    def change_speed(self, num):
        self.controller.change_speed(int(num))

    def change_ignore(self):
        self.controller.change_ignore(self.ignoreVar.get())

    def change_color(self):
        color = askcolor()
        if color == (None, None):
            return
        html = color[1]
        rgb = color[0]
        self.col.config(bg=html)
        self.controller.setDefaultColor(list(rgb))

    def load_patterns(self):
        """
        Loads patterns into the lbox
        """
        self.lbox.clear()
        for file_name in os.listdir(PATTERN_DIR):
            name = os.path.splitext(file_name)[0]
            self.lbox.add_choice(name)
        if len(self.lbox.choices()) != 0:
            self.lbox.set_selection(self.curPattern)

    def open_pattern(self):
        name = self.lbox.choices()[self.curPattern]
        runners.load_pattern(name, self.load_patterns)

    def del_pattern(self, ind=None):
        name = self.lbox.choices()[self.curPattern]
        if self.curPattern == len(self.lbox.choices()) - 1:
            self.curPattern -= 1
        os.remove(os.path.join(PATTERN_DIR, name + '.pattern'))
        self.load_patterns()
        self.lbox.set_selection(self.curPattern)

    def set_cur_pattern(self, ind):
        self.curPattern = ind

    def double_cick(self, event):
        """
        Handler for double clicks. Opens pattern
        """
        self.open_pattern()
