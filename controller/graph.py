import threading
import matplotlib
from mpl_toolkits.mplot3d.art3d import Poly3DCollection, Path3DCollection
from controller.core_logic.scan_algorithms import ScanAlgorithms
from .core_logic.atom_logic import AtomsLogic

matplotlib.use("TkAgg")
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
        self.atoms_logic = AtomsLogic()
        self.__scanAlgorithm = ScanAlgorithms()
        self.condition_build_surface = True
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.is_new_point = False
        self.quit = False
        self.x_arr, self.y_arr = np.meshgrid(np.arange(0, MAX_FIELD_SIZE, 1), np.arange(0, MAX_FIELD_SIZE, 1))
        self.__data_arr_for_graph = np.zeros((MAX_FIELD_SIZE, MAX_FIELD_SIZE))
        self.surface = None
        self.tool_tip = None
        self.captured_atom = None
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        plt.xlim(0, MAX_FIELD_SIZE + 2)
        plt.ylim(0, MAX_FIELD_SIZE + 2)

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_data(self):
        x = int(self.atoms_logic.dto_x.var['value'])
        y = int(self.atoms_logic.dto_y.var['value'])
        z = int(self.atoms_logic.dto_z.var['value'])
        if self.atoms_logic.is_new_point(x, y, z):
            try:
                self.tool_tip.remove() if self.tool_tip is not None else None
                self.captured_atom.remove() if self.captured_atom is not None else None
            except Exception as e:
                print(str(e))
            self.tool_tip = self.ax.scatter(x, y, z, s=5, c=COLOR_TIP, marker='8')
            self.atoms_logic.update_tool_coordinate(
                self.atoms_logic.dto_x.var,
                self.atoms_logic.dto_y.var,
                self.atoms_logic.dto_z.var
            )
            if self.atoms_logic.is_it_surface:
                self.__data_arr_for_graph[y, x] = z  # todo озможно стоит перенести это поле с данными в atoms_logic
                # threading.Thread(target=self.__generate_surface).start() # независимая генерация данных для графика
            if self.atoms_logic.is_it_atom and \
               self.atoms_logic.append_unique_atom(x, y, z) and \
               not self.atoms_logic.is_atom_captured():
                self.ax.scatter(x, y, z, s=5, c=COLOR_ATOM, marker='8')
            if self.atoms_logic.is_atom_captured():
                self.captured_atom = self.ax.scatter(x, y, z - 1, s=5, c=COLOR_ATOM, marker='8')
                atom_coordinates = self.atoms_logic.mark_atom_capture((x, y, z))
                self.__remove_captured_atom(*atom_coordinates)
            if self.condition_build_surface:
                self.__build_surface()


    def __remove_captured_atom(self, *args):
        for dot in self.ax.collections:
            if isinstance(dot, Poly3DCollection):
                continue
            dot: Path3DCollection
            if args == self.__get_dot_coordinates(dot):
                dot.remove()

    @staticmethod
    def __get_dot_coordinates(dot: Path3DCollection) -> tuple:
        _offsets3d = dot.__getattribute__('_offsets3d')
        return (
            int(_offsets3d[0][0]),
            int(_offsets3d[1][0]),
            int(_offsets3d[2][0]),
        )

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
            self.surface.remove() if self.surface is not None else None
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

    def __build_surface(self):
        self.remove_surface()
        self.surface = self.ax.plot_surface(self.x_arr, self.y_arr, self.__data_arr_for_graph,
                                            rstride=1, cstride=1, cmap=plt.cm.get_cmap('Blues_r'),
                                            )
        self.canvas.draw_idle()
        self.ax.mouse_init()

    def get_data(self) -> object:
        return self.__data_arr_for_graph.tolist()




