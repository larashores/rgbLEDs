from tkinter import *

from runnerEditor.model.controller import Controller
from gui.runnerEditor import RunnerEdit


def new_pattern(finish_cmd):
    root = Toplevel()
    root.protocol('WM_DELETE_WINDOW',lambda: root.quit())
    controller = Controller()
    edit = RunnerEdit(root,controller)
    edit.new_pattern(6)
    edit.pack()
    root.focus_set()
    root.grab_set()
    root.transient()
    edit.mainloop()
    root.destroy()
    finish_cmd()


def load_pattern(name, finish_cmd):
    root = Toplevel()
    root.protocol('WM_DELETE_WINDOW',lambda: root.quit())
    controller = Controller()
    edit = RunnerEdit(root,controller)
    edit.load_pattern(name)
    edit.pack()
    edit.mainloop()
    root.destroy()
    finish_cmd()