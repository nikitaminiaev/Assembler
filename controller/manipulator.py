import json
import os
import traceback

import matplotlib as plt
import time
from controller.core_logic.scan_algorithms import ScanAlgorithms, FIELD_SIZE
from .core_logic.exceptions.touching_surface import TouchingSurface
from .graph import Graph, GraphFrame
from tkinter import Frame, Button, Scale, Canvas, StringVar, Entry, constants as c
import tkinter as tk
import threading
from .constants import *


RELWIDTH = 0.7
CANVAS_SIZE = 1000
WINDOW_SIZE = '800x600'
FRAME_COLOR = '#3d3d42'

LENGTH = 300


class Manipulator(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        plt.use("TkAgg")
        self.quit = False
        self['bg'] = '#ccc'
        self.title('Manipulator')
        self.wm_attributes('-alpha', 0.7)
        self.geometry(WINDOW_SIZE)
        self.graph = Graph()
        self.constructorFrames = ConstructorFrames(self)
        self.constructorFrames.pack()
        self.graph.after_idle(self.update_graph)

    def update_graph(self):
        try:
            self.graph.frame.update_graph_data_algorithm()
            self.graph.after(MS_TO_UPDATE_GRAPH, lambda: self.update_graph())

        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
            exit(0)

    def custom_mainloop(self):
        try:
            threading.Thread(target=self.graph.frame.draw_graph).start()
            self.graph.frame.atoms_logic.server.set_up()
            self.graph.mainloop()
            self.mainloop()
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
            exit(0)


class ConstructorFrames:

    def __init__(self, tk: Manipulator):
        self.tk = tk
        self.__canvas = Canvas(tk, height=CANVAS_SIZE, width=CANVAS_SIZE)

        self.__frame_top = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__frame_top.place(relx=0.15, rely=0.05, relwidth=RELWIDTH, relheight=0.50)
        self.__frame_bottom_1 = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__frame_bottom_1.place(relx=0.15, rely=0.60, relwidth=RELWIDTH, relheight=0.05)
        self.__frame_bottom_2 = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__frame_bottom_2.place(relx=0.15, rely=0.65, relwidth=RELWIDTH, relheight=0.05)
        self.__frame_debug = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__frame_debug.place(relx=0.15, rely=0.75, relwidth=RELWIDTH, relheight=0.05)

        self.__scale_x = Scale(self.__frame_top, from_=MAX, to=MIN, length=LENGTH, label='x',
                               command=self.__transmitting_value_x)
        self.__scale_y = Scale(self.__frame_top, from_=MAX, to=MIN, length=LENGTH, label='y',
                               command=self.__transmitting_value_y)
        self.__scale_z = Scale(self.__frame_top, orient='horizontal', from_=MIN, to=MAX, length=LENGTH, label='z',
                               command=self.__transmitting_value_z)
        self.__scan_vars = StringVar()
        self.__scan_vars_entry = Entry(self.__frame_bottom_1, textvariable=self.__scan_vars)
        self.__scan_vars_entry.place(width=10, height=5)

        self.__auto_on_off_btn = Button(self.__frame_bottom_1, text='go/stop auto_scan', bg='#595959', command=self.auto)
        self.__build_surface_btn = Button(self.__frame_bottom_1, text='on/off build surface',
                                          command=self.__build_surface)  # не строит поверхноть, но копит данные о ней
        self.__is_it_surface_btn = Button(self.__frame_bottom_1, text='is it surface', bg='#595959',
                                          command=self.__is_it_surface)
        self.__stop_render_btn = Button(self.__frame_bottom_1, text='stop/go render', command=self.__stop_go_render) # stop/go __drow_graph: canvas.draw_idle()
        self.__snap_to_point_btn = Button(self.__frame_bottom_2, text='snap_to_point', command=self.__snap_to_point)
        self.__remove_surface_btn = Button(self.__frame_bottom_2, text='remove_surface', command=self.__remove_surface)
        self.__show_surface_btn = Button(self.__frame_bottom_2, text='show_surface', command=self.__show_surface)
        self.__is_atom_btn = Button(self.__frame_bottom_2, text='is_atom', command=self.__is_atom)
        self.__is_atom_captured_btn = Button(self.__frame_bottom_2, text='is_atom_captured', command=self.__is_atom_captured)
        self.__file_name = StringVar()
        self.__save_data_entry = Entry(self.__frame_debug, textvariable=self.__file_name)
        self.__save_data_entry.place(width=20, height=5)
        self.__save_data_btn = Button(self.__frame_debug, text='save data', command=self.__save_file)
        self.__load_data_entry = Entry(self.__frame_debug, textvariable=self.__file_name)
        self.__load_data_entry.place(width=20, height=5)
        self.__load_data_btn = Button(self.__frame_debug, text='load data', command=self.__load_file)
        self.default_bg = self.__stop_render_btn.cget("background")
        self.scanAlgorithm = ScanAlgorithms()
        self.__snap_to_point()

    def __transmitting_value_x(self, x: int):
        y = self.tk.graph.frame.atoms_logic.dto_y.get_val()
        z = self.tk.graph.frame.atoms_logic.dto_z.get_val()
        try:
            self.tk.graph.frame.atoms_logic.dto_x.set_val((x, y, z))
        except TouchingSurface as e:
            self.__snap_to_point()
            print(traceback.format_exc())
            print(str(e))


    def __transmitting_value_y(self, y: int):
        x = self.tk.graph.frame.atoms_logic.dto_x.get_val()
        z = self.tk.graph.frame.atoms_logic.dto_z.get_val()
        try:
            self.tk.graph.frame.atoms_logic.dto_y.set_val((x, y, z))
        except TouchingSurface as e:
            self.__snap_to_point()
            print(traceback.format_exc())
            print(str(e))

    def __transmitting_value_z(self, z: int):
        x = self.tk.graph.frame.atoms_logic.dto_x.get_val()
        y = self.tk.graph.frame.atoms_logic.dto_y.get_val()
        try:
            self.tk.graph.frame.atoms_logic.dto_z.set_val((x, y, z))
        except TouchingSurface as e:
            self.__snap_to_point()
            print(traceback.format_exc())
            print(str(e))

    def __snap_to_point(self):
        self.__scale_x.set(self.tk.graph.frame.atoms_logic.dto_x.get_val())
        self.__scale_y.set(self.tk.graph.frame.atoms_logic.dto_y.get_val())
        self.__scale_z.set(self.tk.graph.frame.atoms_logic.dto_z.get_val())

    def __remove_surface(self):
        self.tk.graph.frame.remove_surface()

    def __show_surface(self):
        self.tk.graph.frame.show_surface()

    def __is_atom(self):
        if self.tk.graph.frame.atoms_logic.is_it_atom():
            self.tk.graph.frame.atoms_logic.set_is_it_atom(False)
        else:
            self.tk.graph.frame.atoms_logic.set_is_it_atom(True)

    def __is_atom_captured(self):
        if self.tk.graph.frame.atoms_logic.is_atom_captured():
            self.tk.graph.frame.atoms_logic.set_is_atom_captured(False)
        else:
            self.tk.graph.frame.atoms_logic.set_is_atom_captured(True)

    def __build_surface(self):
        if self.tk.graph.frame.condition_build_surface:
            self.tk.graph.frame.condition_build_surface = False
        else:
            self.tk.graph.frame.condition_build_surface = True

    def __is_it_surface(self):
        if self.tk.graph.frame.atoms_logic.is_it_surface():
            self.tk.graph.frame.atoms_logic.set_is_it_surface(False)
        else:
            self.tk.graph.frame.atoms_logic.set_is_it_surface(True)

    def __save_file(self):
        GraphFrame.write_data_to_json_file(self.__file_name.get(), self.tk.graph.frame.get_data())

    def __load_file(self):
        pass

    def auto(self):
        vars = tuple(map(int, self.__scan_vars.get().split(' ')))
        if self.scanAlgorithm.stop:
            self.scanAlgorithm.stop = False
            threading.Thread(target=self.__go_auto, args=vars).start()
        else:
            self.scanAlgorithm.stop = True

    def __go_auto(self, x_min: int = 0, y_min: int = 0, x_max: int = FIELD_SIZE, y_max: int = FIELD_SIZE): # todo перевести на *kargs
        gen = self.scanAlgorithm.data_generator(x_min, y_min, x_max, y_max)
        while not self.scanAlgorithm.stop:
            time.sleep(SLEEP_BETWEEN_SCAN_ITERATION)
            try:
                x, y, z = next(gen)
                self.tk.graph.frame.atoms_logic.dto_x.set_val((x, y, z))
                self.tk.graph.frame.atoms_logic.dto_y.set_val((x, y, z))
                self.tk.graph.frame.atoms_logic.dto_z.set_val((x, y, z))
            except Exception as e:
                print(traceback.format_exc())
                print(str(e))

    def __stop_go_render(self):
        if self.tk.graph.frame.quit:
            self.tk.graph.frame.quit = False
            threading.Thread(target=self.tk.graph.frame.draw_graph).start()
        else:
            self.tk.graph.frame.quit = True

    def pack(self):
        self.__build_surface_btn.bind('<Button-1>',
                                      lambda e, cause='tk.graph.frame.condition_build_surface': self.change_button(e, cause))
        self.__is_it_surface_btn.bind('<Button-1>',
                                      lambda e, cause='tk.graph.frame.condition_is_it_surface': self.change_button(e, cause))

        self.__stop_render_btn.bind('<Button-1>',
                                      lambda e, cause='tk.graph.frame.quit': self.change_button(e, cause))
        self.__auto_on_off_btn.bind('<Button-1>',
                                      lambda e, cause='scanAlgorithm.stop': self.change_button(e, cause))

        self.__canvas.pack()

        self.__scale_x.pack(side=c.LEFT, padx=10)
        self.__scale_y.pack(side=c.LEFT, padx=10)
        self.__scale_z.pack(side=c.BOTTOM, pady=5)

        self.__scan_vars_entry.pack(side=c.LEFT)
        self.__auto_on_off_btn.pack(side=c.LEFT)
        self.__build_surface_btn.pack(side=c.LEFT, padx=5)
        self.__is_it_surface_btn.pack(side=c.LEFT, padx=5)
        self.__stop_render_btn.pack(side=c.LEFT)

        self.__snap_to_point_btn.pack(side=c.LEFT)
        self.__remove_surface_btn.pack(side=c.LEFT, padx=50)
        self.__show_surface_btn.pack(side=c.LEFT)
        self.__is_atom_btn.pack(side=c.LEFT, padx=5)
        self.__is_atom_captured_btn.pack(side=c.LEFT, padx=5)

        self.__save_data_entry.pack(side=c.LEFT)
        self.__save_data_btn.pack(side=c.LEFT, padx=5)
        self.__load_data_entry.pack(side=c.LEFT, padx=5)
        self.__load_data_btn.pack(side=c.LEFT)

    def scale_set(self, x, y, z):
        self.__scale_x.set((x, y, z))
        self.__scale_y.set((x, y, z))
        self.__scale_z.set((x, y, z))

    def change_button(self, event, cause):
        cause = {
            'scanAlgorithm.stop': {'condition': not self.scanAlgorithm.stop, 'button': self.__auto_on_off_btn},
            'tk.graph.frame.quit': {'condition': not self.tk.graph.frame.quit, 'button': self.__stop_render_btn},
            'tk.graph.frame.condition_build_surface': {'condition': self.tk.graph.frame.condition_build_surface, 'button': self.__build_surface_btn},
            'tk.graph.frame.condition_is_it_surface': {'condition': self.tk.graph.frame.atoms_logic.is_it_surface(), 'button': self.__is_it_surface_btn},
        }.get(cause)

        self.cycle_change_bg(cause)


    def cycle_change_bg(self, cause):
        if cause['condition']:
            if self.default_bg == '#595959':
                cause['button'].configure(bg='#d9d9d9')
            else:
                cause['button'].configure(bg='#595959')
        else:
            cause['button'].configure(bg=self.default_bg)


