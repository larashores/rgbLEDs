import tkinter as tk
from tkinter import ttk

from utilities.constants import *


class LabeledScale(ttk.Frame):
    def __init__(self, parent, text, **kwargs):
        ttk.Frame.__init__(self, parent)
        ttk.Label(self, text=text).pack(expand=tk.YES, fill=tk.X)
        self.scale = tk.Scale(self, bg=B_COLOR, fg=F_COLOR, **kwargs)
        self.scale.pack(expand=tk.YES, fill=tk.X)

    def set(self, num):
        self.scale.set(num)

    def config(self, **kwargs):
        self.scale.config(**kwargs)
