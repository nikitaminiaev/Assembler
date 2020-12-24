import json
import os
import time
from tkinter.ttk import Entry

import matplotlib as plt
from graph import Graph, GraphFrame
from tkinter import Frame, Button, Scale, Canvas, StringVar, constants as c
import tkinter as tk
from dto import Dto, SENSOR_NAME
import threading
import pandas as pd

CANVAS_SIZE = 1000

WINDOW_SIZE = '600x400'
FRAME_COLOR = '#98a192'
MAX = 99
MIN = 0
LENGTH = 300


class Manipulator(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        plt.use("TkAgg")
        self.quit = False
        self['bg'] = '#fafafa'
        self.title('Manipulator')
        self.wm_attributes('-alpha', 0.7)
        self.geometry(WINDOW_SIZE)

        self.constructorFrames = ConstructorFrames(self)
        self.constructorFrames.pack()

        self.graph = Graph()
        self.graph.after_idle(self.update_graph)

    def update_graph(self):
        try:
            self.graph.frame.update_data(
                int(self.constructorFrames.scale_dto_x.var['data']),
                int(self.constructorFrames.scale_dto_y.var['data']),
                int(self.constructorFrames.scale_dto_z.var['data']),
            )
            self.graph.after(50, lambda: self.update_graph())

        except Exception as e:
            print(str(e))
            exit(0)

    def custom_mainloop(self):
        try:
            threading.Thread(target=self.graph.frame.draw_graph).start()
            # threading.Thread(target=self.graph.frame.update_file, args=(  # запись данных в файл
            #     self.constructorFrames.scale_dto_x.var,
            #     self.constructorFrames.scale_dto_y.var,
            #     self.constructorFrames.scale_dto_z.var,
            # )).start()
            self.graph.mainloop()
            self.mainloop()
        except Exception as e:
            print(str(e))
            exit(0)


class ConstructorFrames:

    def __init__(self, tk: Manipulator):
        self.tk = tk
        self.__canvas = Canvas(tk, height=CANVAS_SIZE, width=CANVAS_SIZE)

        self.__frame_debug = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__frame_debug.place(relx=0.15, rely=0.75, relwidth=0.7, relheight=0.20)

        self.__frame_top = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__frame_top.place(relx=0.15, rely=0.05, relwidth=0.7, relheight=0.50)

        self.__frame_bottom = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__frame_bottom.place(relx=0.15, rely=0.60, relwidth=0.7, relheight=0.1)
        self.__Auto_on_off_btn = Button(self.__frame_bottom, text='Auto on/off', command=self.__go_auto)

        self.scale_dto_x = Dto(SENSOR_NAME['SERVO_X'], self.__frame_debug, side=c.LEFT)
        self.__scale_x = Scale(self.__frame_top, from_=MAX, to=MIN, length=LENGTH, label='x',
                               command=self.scale_dto_x.on_scale)
        self.scale_dto_y = Dto(SENSOR_NAME['SERVO_Y'], self.__frame_debug, side=c.RIGHT)
        self.__scale_y = Scale(self.__frame_top, from_=MAX, to=MIN, length=LENGTH, label='y',
                               command=self.scale_dto_y.on_scale)
        self.scale_dto_z = Dto(SENSOR_NAME['SERVO_Z'], self.__frame_debug, c.LEFT)
        self.__scale_z = Scale(self.__frame_top, orient='horizontal', from_=MIN, to=MAX, length=LENGTH, label='z',
                               command=self.scale_dto_z.on_scale)

        self.__file_name = StringVar()
        self.__stop_render_btn = Button(self.__frame_bottom, text='stop/go render', command=self.__stop_go_render)
        self.__render_surface_btn = Button(self.__frame_bottom, text='render surface', command=self.__render_surface)
        self.__save_data_entry = Entry(self.__frame_debug, text='render surface', textvariable=self.__file_name)
        self.__save_data_btn = Button(self.__frame_debug, text='save', command=self.__save_file)

    def __render_surface(self):
        self.tk.graph.frame.render_surface()

    def __save_file(self):
        GraphFrame.write_data_to_json_file(self.__file_name.get(), self.tk.graph.frame.data_arr.tolist())

    def __go_auto(self):
        pass

    def __stop_go_render(self):
        if self.tk.graph.frame.quit:
            self.tk.graph.frame.quit = False
            threading.Thread(target=self.tk.graph.frame.draw_graph).start()
        else:
            self.tk.graph.frame.quit = True

    def pack(self):
        self.__canvas.pack()
        self.__Auto_on_off_btn.pack(side=c.LEFT)
        self.__render_surface_btn.pack(side=c.LEFT)
        self.__stop_render_btn.pack(side=c.LEFT)
        self.__save_data_entry.pack(side=c.LEFT)
        self.__save_data_btn.pack(side=c.LEFT)
        self.__scale_x.pack(side=c.LEFT, padx=15)
        self.__scale_y.pack(side=c.RIGHT, padx=15)
        self.__scale_z.pack(fill=c.Y, anchor=c.S, pady=20)
