"""
"""

import tkinter as tk
from tkinter import ttk


class ListChoiceGUI(ttk.Frame):
    """
    Purpose:    Scrolling Listbox where entries can be added and deleted
    Attributes:
        parent:     Parent widget
        choicelist: The list where choice strings are stored
        indexvar:   IntVar where the selected index is stored
    """
    def __init__(self, parent, controller, update_cmd, delete_cmd, **kwargs):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.update_cmd = update_cmd
        self.delete_cmd = delete_cmd
        self.lbox, self.sbar, self.hsbar = self._make_widgets(kwargs)
        self.last_selection = None
        if delete_cmd is not None:
            self.lbox.bind('<Delete>', lambda event: self.delete())
        self.lbox.bind('<Button-1>', lambda event: self._click())
        self.lbox.bind('<Up>', lambda event: self._up())
        self.lbox.bind('<Down>', lambda event: self._down())

    def _make_widgets(self, kwargs):
        frm = ttk.Frame(self)
        sbar = ttk.Scrollbar(frm)
        lbox = tk.Listbox(frm, selectmode=tk.SINGLE,  **kwargs)
        sbar.config(command=lbox.yview)
        lbox.config(yscrollcommand=sbar.set)
        lbox.config(selectmode=tk.SINGLE)

        hsbar = ttk.Scrollbar(self, orient=tk.HORIZONTAL)
        hsbar.config(command=lbox.xview)
        lbox.config(xscrollcommand=hsbar.set)

        sbar.pack(side=tk.RIGHT, fill=tk.Y)
        hsbar.pack(side=tk.BOTTOM, fill=tk.X)
        lbox.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)
        frm.pack(expand=tk.YES, fill=tk.BOTH)

        return lbox, sbar, hsbar

    def delete(self):
        if self.controller.get_selection() is not None:
            self.delete_cmd(self.controller.get_selection())

    def _click(self):
        self.after(20, self.__click)

    def __click(self):
        val = self.lbox.curselection()
        if len(val) != 1:
            pass
        else:
            self.controller.set_selection(val[0])

    def _up(self):
        self.controller.up()

    def _down(self):
        self.controller.down()

    def update_selection(self):
        ind = self.controller.get_selection()
        self.lbox.selection_clear(0, tk.END)
        self.lbox.selection_set(ind)
        self.after(20, lambda: self.lbox.activate(ind))
        self.update_cmd(ind)


class ListChoice:
    def __init__(self, parent=None, *,
                 update_cmd=lambda x: None,
                 delete_cmd=lambda x: None,
                 **kwargs):
        self.model = ListChoiceModel()
        self.gui = ListChoiceGUI(parent, self, update_cmd, delete_cmd, **kwargs)

    def __iter__(self):
        for choice in self.model:
            yield choice

    def __getitem__(self, index):
        return self.model.choices[index]

    def __len__(self):
        return len(self.model.choices)

    def pack(self, **kwargs):
        self.gui.pack(**kwargs)

    def index(self, ind):
        return self.model.choices.index(ind)

    def add_choice(self, string):
        self.model.add_choice(string)
        self.model.set_current_index(-1)
        self.update()

    def insert_choice(self, ind, string):
        if ind < 0 and len(self) != 0:
            ind %= (len(self) + 1)
        self.model.insert_choice(ind, string)
        self.model.set_current_index(ind)
        self.update()

    def set_position(self, ind):
        if ind < 0 and len(self) != 0:
            ind %= (len(self) + 1)
        self.gui.lbox.yview_moveto(ind)

    def get_top(self):
        return (self.gui.lbox.yview()[0]) * len(self)

    def set_top(self, top):
        if len(self) == 0:
            return
        value = top / len(self)
        self.gui.lbox.yview_moveto(value)

    def get_y_position(self):
        return self.gui.lbox.yview()[1]

    def delete(self, ind):
        self.model.delete(int(ind))
        self.update()
        if self.get_selection() is not None:
            self.gui.update_selection()

    def clear(self):
        self.model.choices.clear()
        self.update()
        self.model.cur_selection = None

    def update(self):
        self.gui.lbox.delete(0, tk.END)
        for choice in self.model:
            self.gui.lbox.insert(tk.END, choice)

    def choices(self):
        return list(self.model)

    def get_selection(self):
        return self.model.get_curent_index()

    def set_selection(self, ind):
        if ind < 0 and ind >= -len(self):
            ind %= len(self)

        l_ind = self.get_selection()
        if l_ind != int(ind):
            self.model.set_current_index(ind)
        self.gui.update_selection()

    def up(self):
        l_ind = self.get_selection()
        self.model.up()
        if l_ind != self.get_selection():
            self.gui.update_selection()

    def down(self):
        l_ind = self.get_selection()
        self.model.down()
        if l_ind != self.get_selection():
            self.gui.update_selection()

    def get_position(self):
        return self.gui.lbox.yview()[0]

    def bind(self, key, handler):
        self.gui.lbox.bind(key, handler)

class ListChoiceModel:
    def __init__(self):
        self.choices = []
        self.cur_selection = None

    def __iter__(self):
        for choice in self.choices:
            yield choice

    def add_choice(self, string):
        self.choices.append(string)
        if self.cur_selection is None:
            self.cur_selection = 0

    def insert_choice(self, ind, string):
        self.choices.insert(ind, string)
        if self.cur_selection is None:
            self.cur_selection = 0

    def set_current_index(self, ind):
        if ind is not None and ind < 0:
            ind = len(self.choices) - ind
        self.cur_selection = ind

    def get_curent_index(self):
        return self.cur_selection

    def up(self):
        ind = self.get_curent_index()
        if ind > 0:
            self.cur_selection = ind - 1

    def down(self):
        ind = self.get_curent_index()
        if ind < len(self.choices)-1:
            self.cur_selection = ind + 1

    def delete(self, ind):
        self.choices.pop(ind)
        if ind == self.cur_selection:
            if self.cur_selection == 0:
                if len(self.choices) == 0:
                    self.cur_selection = None
            else:
                if len(self.choices)-1 > self.cur_selection:
                    self.cur_selection += 0
                else:
                    self.cur_selection -= 1
        elif ind < self.cur_selection:
            self.cur_selection -= 1
        else:
            pass


if __name__ == '__main__':
    root = tk.Tk()

    def delete(ind):
        list1.delete(ind)
    list1 = ListChoice(update_cmd=lambda ind: print('Selecting', ind), delete_cmd=delete)
    list1.pack(expand=tk.YES, fill=tk.BOTH)

    for choice in ['1', 'poop', '2', '4asfd','45','hey','adga','meeee','asdfas','425','adsf']:
        list1.add_choice(choice)
    list1.set_selection(10)

    tk.mainloop()

