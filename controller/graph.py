import traceback
import matplotlib
from controller.core_logic.scan_algorithms import ScanAlgorithms
from .core_logic.atom import Atom
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

    def update_graph_data_algorithm(self):
        if self.atoms_logic.is_new_point():
            try:
                self.tool_tip.remove() if self.tool_tip is not None else None
                self.captured_atom.remove() if self.captured_atom is not None else None
            except Exception as e:
                self.captured_atom = None
                print(traceback.format_exc())
                print(str(e))
            if self.atoms_logic.atom_release_event:
                self.ax.scatter(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_ATOM, marker='8')
                self.atoms_logic.atom_release_event = False
            self.atoms_logic.update_tool_coordinate()
            self.tool_tip = self.ax.scatter(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_TIP, marker='8')
            if self.atoms_logic.is_it_atom() and self.atoms_logic.append_unique_atom():
                self.ax.scatter(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_ATOM, marker='8')
            if self.atoms_logic.atom_captured_event:
                self.__update_all_dots_on_graph()
                self.atoms_logic.atom_captured_event = False
            if self.atoms_logic.is_atom_captured():
                self.captured_atom = self.ax.scatter(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_ATOM, marker='8')
            if self.condition_build_surface:
                self.__build_surface()
            self.__reset_sensor()

    def __reset_sensor(self):
        if self.atoms_logic.tool_is_coming_down():
            return
        self.atoms_logic.set_is_it_surface(False)
        self.atoms_logic.set_is_it_atom(False)

    def __set_tool_tip_dot(self):
        self.tool_tip = self.ax.scatter(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_TIP, marker='8')

    def __update_all_dots_on_graph(self):
        self.ax.collections = []
        self.__set_tool_tip_dot()
        for atom in self.atoms_logic.atoms_list:
            atom: Atom
            if not atom.is_captured:
                self.ax.scatter(*atom.coordinates, s=5, c=COLOR_ATOM, marker='8')
            else:
                self.captured_atom = self.ax.scatter(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_ATOM, marker='8')

    def show_surface(self):
        self.__build_surface()

    def remove_surface(self):
        try:
            self.surface.remove() if self.surface is not None else None
        except Exception as e:
            print(traceback.format_exc())
            print(str(e))

    def draw_graph(self):
        while not self.quit:
            try:
                time.sleep(SLEEP_BETWEEN_DRAW_GRAPH)
                self.canvas.draw_idle()
            except Exception as e:
                self.quit = True
                print(traceback.format_exc())
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
        self.surface = self.ax.plot_surface(self.x_arr, self.y_arr, self.atoms_logic.surface_data,
                                            rstride=1, cstride=1, cmap=plt.cm.get_cmap('Blues_r'),
                                            )
        self.canvas.draw_idle()
        self.ax.mouse_init()

    def get_data(self) -> object:
        return self.atoms_logic.surface_data.tolist()
