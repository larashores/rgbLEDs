from tkinter import ttk
import tkinter as tk
from gui.mainWindow import MainWindow
from effects.controller import Controller
from utilities.constants import EFFECT_FONT, SUB_FONT, B_COLOR, F_COLOR, TITLE_FONT


def main():
    controller = Controller()
    root = tk.Tk()
    root.title('LED Lights')

    def close():
        controller.end()
        root.destroy()
    root.protocol('WM_DELETE_WINDOW', close)

    s = ttk.Style()
    s.configure('TFrame', background='black')
    s.configure('TLabel', background=B_COLOR, foreground=F_COLOR)
    s.configure('TCheckbutton', background=B_COLOR, foreground=F_COLOR, selectcolor=B_COLOR, activebackground='grey')
    s.configure('Effect.TButton', font=EFFECT_FONT, width=9)
    s.configure('Effect.TLabel', font=EFFECT_FONT)
    s.configure('Title.TLabel', font=TITLE_FONT)
    s.configure('Subtitle.TLabel', font=SUB_FONT)
    s.configure('Component.TFrame', font=SUB_FONT, borderwidth=3, relief=tk.GROOVE)

    gui = MainWindow(root, controller)
    gui.pack(expand=tk.YES, fill=tk.BOTH)
    tk.mainloop()


if __name__ == '__main__':
    main()
