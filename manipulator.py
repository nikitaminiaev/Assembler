import queue
import matplotlib as plt
from graph import SeaofBTCapp
from tkinter import Frame, Button, Scale, Canvas, constants as c
import tkinter as tk
from scaleDto import ScaleDto
import threading

CANVAS_SIZE = 1000

WINDOW_SIZE = '600x400'
FRAME_COLOR = '#98a192'
MAX = 100
MIN = 0
LENGTH = 300


class Manipulator(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quit = False
        plt.use("TkAgg")

        self['bg'] = '#fafafa'
        self.title('Manipulator')
        self.wm_attributes('-alpha', 0.7)
        self.geometry(WINDOW_SIZE)

        self.constructorFrames = ConstructorFrames(self)
        self.constructorFrames.pack()

        self.app = SeaofBTCapp()
        self.app.after_idle(self.update)

        self.data = ()
        self.q_data = queue.Queue()

    def update(self):
        try:
            while not self.q_data.empty():
                data = self.q_data.get()
                self.app.frame.update_data(
                    data[0],
                    data[1],
                    data[2],
                )
            self.app.after(200, lambda: self.update())
        except:
            exit(0)

    def custom_mainloop(self):
        threading.Thread(target=self.add_data_in_queue, args=(
            int(self.constructorFrames.scale_dto_x.var['data']),
            int(self.constructorFrames.scale_dto_y.var['data']),
            int(self.constructorFrames.scale_dto_z.var['data']),
        )).start()
        self.app.mainloop()
        self.mainloop()

    def add_data_in_queue(self, x, y, z):
        while not self.quit:
            try:
                if (x, y, z) != self.data:
                    self.q_data.put((x, y, z))
                    self.data = (x, y, z)
            except:
                self.quit = True
                exit(0)


class ConstructorFrames:

    def __init__(self, tk: object):
        self.__canvas = Canvas(tk, height=CANVAS_SIZE, width=CANVAS_SIZE)

        self.__frame_debug = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__frame_debug.place(relx=0.15, rely=0.75, relwidth=0.7, relheight=0.20)

        self.__frame_top = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__frame_top.place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.50)

        self.__frame_bottom = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__frame_bottom.place(relx=0.15, rely=0.60, relwidth=0.7, relheight=0.1)
        self.__btn = Button(self.__frame_bottom, text='Auto on/off', command=self.go_auto)

        self.scale_dto_x = ScaleDto(self.__frame_debug, side=c.LEFT)
        self.__scale_x = Scale(self.__frame_top, from_=MAX, to=MIN, length=LENGTH, label='x',
                               command=self.scale_dto_x.on_scale)
        self.scale_dto_y = ScaleDto(self.__frame_debug, side=c.RIGHT)
        self.__scale_y = Scale(self.__frame_top, from_=MAX, to=MIN, length=LENGTH, label='y',
                               command=self.scale_dto_y.on_scale)
        self.scale_dto_z = ScaleDto(self.__frame_debug, c.LEFT)
        self.__scale_z = Scale(self.__frame_top, orient='horizontal', from_=MIN, to=MAX, length=LENGTH, label='z',
                               command=self.scale_dto_z.on_scale)

    def go_auto(self):
        pass

    def pack(self):
        self.__canvas.pack()
        self.__btn.pack()
        self.__scale_x.pack(side=c.LEFT, padx=15)
        self.__scale_y.pack(side=c.RIGHT, padx=15)
        self.__scale_z.pack(fill=c.Y, anchor=c.S, pady=20)
