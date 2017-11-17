import tkinter as tk

from runnerEditor.model.controller import Controller
from gui.runnereditor import RunnerEdit


def main():
    root = tk.Tk()
    controller = Controller()
    edit = RunnerEdit(root, controller)
    edit.new_pattern(6)
    edit.pack()
    tk.mainloop()

if __name__ == '__main__':
    main()
