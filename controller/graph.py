import threading
import matplotlib
from matplotlib.collections import PathCollection
from controller.core_logic.scan_algorithms import ScanAlgorithms
from .core_logic.atom_work import AtomWork

matplotlib.use("TkAgg")
from sockets import server
import json
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import time
import numpy as np
from .constants import *

LARGE_FONT = ("Verdana", 12)
MULTIPLICITY = 1
COLOR_TIP = 'g'
COLOR_ATOM = 'r'


class Graph(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("client")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        self.frame = GraphFrame(container)
        self.frames[GraphFrame] = self.frame
        self.frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class GraphFrame(tk.Frame):

    def __init__(self, parent, **kw):
        super().__init__(parent, **kw)
        self.AtomWork = AtomWork()
        self.__scanAlgorithm = ScanAlgorithms()
        self.server = server.Server()
        self.condition_build_surface = True
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.condition_add_point = False
        self.quit = False
        self.__x_previous = 0
        self.__y_previous = 0
        self.__z_previous = 0
        self.x_arr, self.y_arr = np.meshgrid(np.arange(0, MAX_FIELD_SIZE, 1), np.arange(0, MAX_FIELD_SIZE, 1))
        self.__data_arr_for_graph = np.zeros((MAX_FIELD_SIZE, MAX_FIELD_SIZE))
        self.surface = None
        self.dots_graph = None
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        plt.xlim(0, MAX_FIELD_SIZE + 2)
        plt.ylim(0, MAX_FIELD_SIZE + 2)

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_data(self, x_dict: dict, y_dict: dict, z_dict: dict):
        x = int(x_dict['value'])
        y = int(y_dict['value'])
        z = int(z_dict['value'])
        self.condition_add_point = (x != self.__x_previous or y != self.__y_previous or z != self.__z_previous) and \
                                   ((x % MULTIPLICITY == 0) or (y % MULTIPLICITY == 0) or (z % MULTIPLICITY == 0))
        if self.condition_add_point:
            try:
                self.dots_graph.remove()
            except Exception as e:
                print(str(e))
            self.dots_graph = self.ax.scatter(x, y, z, s=5, c=COLOR_TIP, marker='8')
            self.__set_command_to_microcontroller(x_dict, y_dict, z_dict, x, y, z)
            self.__x_previous = x
            self.__y_previous = y
            self.__z_previous = z
            if self.AtomWork.is_it_surface:
                self.__data_arr_for_graph[y, x] = z # todo озможно стоит перенести это поле с данными в AtomWork
                # threading.Thread(target=self.__generate_surface).start() # независимая генерация данных для графика
            if self.AtomWork.is_it_atom and self.AtomWork.atom_is_unique(x, y, z):
                self.ax.scatter(x, y, z, s=5, c=COLOR_ATOM, marker='8')
            if self.AtomWork.is_atom_captured:
                pass # todo если True нужно рендерить вторую красную точку с наконечником снизу и удалять атом с поверхности
            if self.condition_build_surface:
                self.__build_surface()

    def get_coordinates(self, dot: PathCollection) -> dict:
        _offsets3d = dot.__getattribute__('_offsets3d')
        return {
            'x': int(_offsets3d[0][0]),
            'y': int(_offsets3d[1][0]),
            'z': int(_offsets3d[2][0]),
        }

    def __generate_surface(self):
        gen = self.__scanAlgorithm.data_generator()
        self.__scanAlgorithm.stop = False
        while not self.__scanAlgorithm.stop:
            try:
                x, y, z = next(gen)
                self.__data_arr_for_graph[y, x] = z
            except Exception as e:
                print(str(e))

    def show_surface(self):
        self.__build_surface()

    def remove_surface(self):
        try:
            self.surface.remove()
        except Exception as e:
            print(str(e))

    def draw_graph(self):
        while not self.quit:
            try:
                time.sleep(SLEEP_BETWEEN_DRAW_GRAPH)
                self.canvas.draw_idle()
            except Exception as e:
                self.quit = True
                print(str(e))
                exit(0)

    @staticmethod
    def write_data_to_json_file(file_name: str, data):
        if os.path.exists(file_name):
            with open(file_name, 'rb+') as data_file:
                data_file.seek(-1, os.SEEK_END)
                data_file.truncate()
            with open(file_name, 'a') as data_file:
                data_file.write(f",{json.dumps(data)}]")
        else:
            with open(file_name, 'a') as data_file:
                data_file.write(f"[{json.dumps(data)}]")

    @staticmethod
    def read_json_file(file_name: str):
        if os.path.exists(file_name):
            with open(file_name, 'r') as data_file:
                return json.load(data_file)

    def __set_command_to_microcontroller(self, x_dict, y_dict, z_dict, *args):
        if args[0] != self.__x_previous:
            # print(x_data)
            self.server.send_data_to_all_clients(json.dumps(x_dict.copy()))
        if args[1] != self.__y_previous:
            # print(y_data)
            self.server.send_data_to_all_clients(json.dumps(y_dict.copy()))
        if args[2] != self.__z_previous:
            # print(z_data)
            self.server.send_data_to_all_clients(json.dumps(z_dict.copy()))

    def __build_surface(self):
        self.remove_surface()
        self.surface = self.ax.plot_surface(self.x_arr, self.y_arr, self.__data_arr_for_graph,
                                            rstride=1, cstride=1, cmap=plt.cm.get_cmap('Blues_r'),
                                            )
        self.canvas.draw_idle()
        self.ax.mouse_init()

    def get_data(self) -> object:
        return self.__data_arr_for_graph.tolist()
