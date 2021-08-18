import matplotlib

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

LARGE_FONT = ("Verdana", 12)
MULTIPLICITY = 1
COLOR_DOT = 'g'
MAX_VALUE = 76


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
        self.server = server.Server()
        self.condition_build_surface = True
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.condition_add_point = False
        self.quit = False
        self.__x_previous = 0
        self.__y_previous = 0
        self.__z_previous = 0
        self.x_arr, self.y_arr = np.meshgrid(np.arange(0, MAX_VALUE, 1), np.arange(0, MAX_VALUE, 1))
        self.data_arr = np.zeros((MAX_VALUE, MAX_VALUE))
        self.surface = None
        self.dots_graph = None
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        plt.xlim(0, MAX_VALUE + 2)
        plt.ylim(0, MAX_VALUE + 2)

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
            self.dots_graph = self.ax.scatter(x, y, z, s=5, c=COLOR_DOT, marker='8')
            self.__set_command_to_microcontroller(x_dict, y_dict, z_dict, x, y, z)
            self.__x_previous = x
            self.__y_previous = y
            self.__z_previous = z
            self.data_arr[y, x] = z
            if self.condition_build_surface:
                self.__build_surface()

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
                time.sleep(0.5)
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
            x_data = x_dict.copy()
            x_data = GraphFrame.__prepare_data(x_data)
            self.server.send_data_to_all_clients(json.dumps(x_data))
            del x_data
        if args[1] != self.__y_previous:
            y_data = y_dict.copy()
            y_data = GraphFrame.__prepare_data(y_data)
            self.server.send_data_to_all_clients(json.dumps(y_data))
            del y_data
        if args[2] != self.__z_previous:
            z_data = z_dict.copy()
            z_data = GraphFrame.__prepare_data(z_data)
            print(z_data)
            self.server.send_data_to_all_clients(json.dumps(z_data))
            del z_data

    def __build_surface(self):
        self.remove_surface()
        self.surface = self.ax.plot_surface(self.x_arr, self.y_arr, self.data_arr,
                                            rstride=1, cstride=1, cmap=plt.cm.get_cmap('Blues_r'),
                                            )
        self.canvas.draw_idle()
        self.ax.mouse_init()

    @staticmethod
    def __prepare_data(data: dict):
        val = int(data['value'])
        data['value'] = val+40
        return data
