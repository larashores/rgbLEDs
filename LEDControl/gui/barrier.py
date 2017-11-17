import tkinter as tk


class Barrier(tk.Frame):
    """
    Fill should always be X when packing
    """
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, height=2, bd=1, relief=tk.SUNKEN)
