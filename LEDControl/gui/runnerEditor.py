import tkinter as tk
from tkinter import ttk

from tkinter.colorchooser import askcolor
from tkinter.messagebox import askyesno

from utilities.constants import *
from gui.barrier import Barrier
from utilities.listchoice import ListChoice


class RunnerEdit(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        ttk.Label(self, text='Pattern Editor', style='Subtitle.TLabel').pack()
        self.controller = controller
        left = ttk.Frame(self)
        right = ttk.Frame(self)
        btm = ttk.Frame(self)
        # ===========================Bottom Stuff=====================
        add = tk.Button(btm, command=self.add_step, text='Add Step', width=9, font=EFFECT_FONT)
        delete = tk.Button(btm, command=self.delete_step, text='Delete Step', width=9, font=EFFECT_FONT)
        save = tk.Button(btm, command=self.save, text='Done', width=9, font=EFFECT_FONT)
        # =========================Left side stuff====================
        self.canvas = EditCanvas(left, controller, bg=B_COLOR)
        self.canvas.defaultColor = [0, 0, 255]
        # =================Right side stuff============================
        steps = ttk.Label(right, text='Steps', style='Effect.TLabel')
        self.addBefore = tk.IntVar()
        addbutton = tk.Checkbutton(right, variable=self.addBefore, text='Add Step Before',
                                   bg=B_COLOR, fg=F_COLOR, selectcolor=B_COLOR)
        self.steps = ListChoice(right, update_cmd=self.canvas.load_step, delete_cmd=self.delete_step, height=8,
                                background='black', foreground='white')
        self.defButton = tk.Button(right, text='Default Color', command=self.default_color,
                                   bg='#%02x%02x%02x' % tuple(self.canvas.defaultColor),
                                   fg='grey')
        self.nameVar = tk.StringVar()
        name = ttk.Label(right, text='Pattern Name')
        name_ent = ttk.Entry(right, textvariable=self.nameVar)
        # ==============================================================

        btm.pack(side=tk.BOTTOM, expand=tk.YES, fill=tk.X, padx=5, pady=(0, 10))
        add.pack(side=tk.LEFT, padx=5)
        delete.pack(side=tk.LEFT, padx=5)
        save.pack(side=tk.LEFT, padx=5)

        left.pack(side=tk.LEFT)
        right.pack(side=tk.LEFT, expand=tk.YES, fill=tk.Y)

        self.canvas.pack()

        name.pack()
        name_ent.pack()
        Barrier(right).pack(expand=tk.YES, fill=tk.X, pady=(10, 0), padx=(7, 7))
        steps.pack()
        addbutton.pack(fill=tk.X)
        self.steps.pack(expand=tk.YES, fill=tk.Y)
        self.defButton.pack(pady=(10, 0))

        self.controller.load_lbox = self.steps.update

    def new_pattern(self, num_lights):
        self.controller.new_pattern(num_lights)   # Start new pattern
        self.canvas.center_step()                  # Initially centers lights on canvas
        self.controller.add_step(0)
        self.steps.add_choice(self.controller.get_step(0))
        self.steps.set_selection(0)
        self.canvas.load_step(0)
        self.nameVar.set(self.controller.get_name())

    def load_pattern(self, name):
        self.controller.load_pattern(name)
        for ind in range(self.controller.len_steps()):
            self.steps.add_choice(self.controller.get_step(ind))
        self.steps.set_selection(0)
        self.canvas.load_step(0)
        self.nameVar.set(self.controller.get_name())

    def add_step(self):
        curstep = self.canvas.curStep
        if self.addBefore.get():
            self.controller.add_step(curstep)
        else:
            curstep += 1
            self.controller.add_step(curstep)
        self.canvas.load_step(curstep)
        self.steps.insert_choice(curstep, self.controller.get_step(curstep))
        self.steps.set_selection(self.canvas.curStep)

    def delete_step(self, ind=None):
        """
        Deletes the current step and then loads the one after or before it
        """
        tot = self.controller.len_steps()
        cur = self.canvas.curStep
        if tot == 1:
            return
        self.controller.del_step(cur)
        self.steps.delete(cur)
        if tot-1 == cur:
            ind = cur-1
            self.steps.set_selection(ind)
            self.canvas.load_step(ind)
        else:
            ind = cur
            self.steps.set_selection(ind)
            self.canvas.load_step(ind)

    def save(self):
        self.controller.set_name(self.nameVar.get())

        exists = self.controller.exists()
        if exists:
            sure = askyesno('Continue', message='Pattern Name already exists')
            if sure:
                self.controller.save_pattern()
            else:
                return
        self.controller.save_pattern()
        self.quit()

    def default_color(self):
        color = askcolor()
        if color == (None, None):
            return
        else:
            color = list(color[0])
        for ind, col in enumerate(color):
            color[ind] = int(col)
        self.canvas.defaultColor = color
        self.defButton.config(bg='#%02x%02x%02x' % tuple(self.canvas.defaultColor))


class EditCanvas(tk.Canvas):
    CIRCLE_RADIUS = 30

    def __init__(self, parent, controller, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.controller = controller
        self.lightitems = []
        self.clickedLight = None
        self.bind('<Button-1>', self.mouse_press)
        self.bind('<Button-2>', self.middle_press)
        self.bind('<Button-3>', self.right_click)
        self.bind('<Double-Button-1>', self.double_mouse_press)
        self.bind('<B1-Motion>', self.mouse_drag)

    def center_step(self):
        """
        Centers location of lights, should be called once on a new pattern
        """
        size = (self.cget('width'), self.cget('height'))
        center = (int(size[0])/2, int(size[1])/2)
        for num in range(self.controller.get_num_lights()):
            self.controller.set_pos(num, center)

    def load_step(self, step_ind):
        """
        Loads the step onto the canvas, deletes current one from view
        """
        self.curStep = step_ind
        for lightitem in self.lightitems:
            for item in lightitem:
                self.delete(item)
        self.lightitems.clear()
        self.draw_circles()

    def draw_circles(self):
        """
        Draws the circles on the canvas using the controller to get the info
        """
        for num in range(self.controller.get_num_lights()):
            random = self.controller.get_random(self.curStep, num)
            center = self.controller.get_pos(num)
            color = self.controller.get_color(self.curStep, num)
            pos = (center[0]-self.CIRCLE_RADIUS,
                   center[1]-self.CIRCLE_RADIUS,
                   center[0]+self.CIRCLE_RADIUS,
                   center[1]+self.CIRCLE_RADIUS)
            circ = self.create_oval(pos, outline='grey', width=5, fill='#%02x%02x%02x' % tuple(color))
            text = self.create_text(center, text=str(num+1), font=('tkdefaultfont', 15, 'bold'), fill='grey')
            if random == 'single':
                self.itemconfig(circ, outline='red', dash=50)
            elif random == 'static':
                self.itemconfig(circ, outline='blue', dash=50)
            elif random == 'pattern':
                self.itemconfig(circ, outline='green', dash=50)
            self.lightitems.append((circ, text))

    def get_circle(self):
        """
        Gets first index of overlapping circle
        """
        overlap = self.find_overlapping(self.xlast, self.ylast,
                                        self.xlast, self.ylast)
        for i in range(len(overlap)-1, -1, -1):
            item = overlap[i]
            for ind, lightitem in enumerate(self.lightitems):
                if item in lightitem:
                    return ind

    # ==========================-Handlers====================================
    def mouse_press(self, event):
        """
        Registers initial mouse cooridates
        """
        self.xlast = event.x
        self.ylast = event.y
        ind = self.get_circle()
        self.clickedLight = ind

    def right_click(self, event):
        self.mouse_press(event)
        ind = self.clickedLight
        if ind is None:
            return
        circ = self.lightitems[ind][0]
        if self.controller.get_color(self.curStep, ind) == self.defaultColor:
            self.controller.set_color(self.curStep, ind, [0, 0, 0])
            self.itemconfig(circ, fill='#000000')
            self.controller.load_lbox()
        else:
            self.itemconfig(circ, fill='#%02x%02x%02x' % tuple(self.defaultColor))
            self.controller.set_color(self.curStep, ind, self.defaultColor)
            self.controller.load_lbox()

    def middle_press(self, event):
        """
        Changes randomness of light. Solid line uses the normal color,
        a red dashed line has an individual random color, and a blue
        dashed line uses the random color of the step
        """
        self.mouse_press(event)
        ind = self.clickedLight
        if ind is None:
            return
        circ = self.lightitems[self.clickedLight][0]
        random = self.controller.get_random(self.curStep, ind)
        if random == 'none':
            self.controller.set_random(self.curStep, ind, 'single')
            self.itemconfig(circ, outline='red', dash=50)
        elif random == 'single':
            self.controller.set_random(self.curStep, ind, 'static')
            self.itemconfig(circ, outline='blue', dash=50)
        elif random == 'static':
            self.controller.set_random(self.curStep, ind, 'pattern')
            self.itemconfig(circ, outline='green', dash=50)
        elif random == 'pattern':
            self.controller.set_random(self.curStep, ind, 'none')
            self.itemconfig(circ, outline='grey', dash=())

    def double_mouse_press(self, event):
        """
        Changes color or light
        """
        color = askcolor()
        if color == (None, None):       # Tests to make sure cancel was not pressed
            return
        else:
            color = list(color[0])
        for ind, col in enumerate(color):
            color[ind] = int(col)
        ind = self.clickedLight
        if ind is None:
            return
        circ = self.lightitems[ind][0]
        self.itemconfig(circ, fill='#%02x%02x%02x' % tuple(color))
        self.controller.set_color(self.curStep, ind, color)
        self.controller.loadLbox()

    def mouse_drag(self, event):
        """
        Move light on mouse drag
        """
        x, y = event.x, event.y
        if self.clickedLight is not None:
            lightitems = self.lightitems[self.clickedLight]
            circ = lightitems[0]
            txt = lightitems[1]     # position of text
            #if x < 10 or y < 10 or x > self.imgsize-10 or y > self.imgsize-10:
            #    return
            self.move(txt, x-self.xlast, y-self.ylast)
            self.move(circ, x-self.xlast, y-self.ylast)
            coords = self.coords(txt)
            self.controller.set_pos(self.clickedLight, coords)
            self.xlast = x
            self.ylast = y
