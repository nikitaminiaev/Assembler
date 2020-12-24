import json
import os

import matplotlib

# from manipulator import Manipulator

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from colour import Color
import time
import numpy as np

LARGE_FONT = ("Verdana", 12)
MULTIPLICITY = 1

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
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.condition_add_point = False
        self.quit = False
        self.__x_previous = 0
        self.__y_previous = 0
        self.__z_previous = 0
        self.dots_graph = None
        # self.__x_arr = np.array([])
        # self.y_arr = np.array([])
        # self.z_arr = np.array([])
        self.__x_arr = np.arange(0, 100, 1)
        self.__y_arr = np.arange(0, 100, 1)
        self.data_arr = np.zeros((100, 100))
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        red = Color("blue")
        self.colors = list(red.range_to(Color("white"), 170))

        plt.xlim(0, 100 + 2)
        plt.ylim(0, 100 + 2)

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_data(self, x=0, y=0, z=0):
        self.condition_add_point = (x != self.__x_previous or y != self.__y_previous or z != self.__z_previous) and \
                                   ((x % MULTIPLICITY == 0) or (y % MULTIPLICITY == 0) or (z % MULTIPLICITY == 0))
        if self.condition_add_point:
            self.dots_graph = self.ax.scatter(x, y, z, s=2, c=str(self.colors[z]), marker='8')
            self.ax.plot([x, self.__x_previous], [y, self.__y_previous], [z, self.__z_previous], c=str(self.colors[z]))
            self.__x_previous = x
            self.__y_previous = y
            self.__z_previous = z
            self.data_arr[y, x] = z

    def render_surface(self):
        self.dots_graph.remove()
        x_arr, y_arr = np.meshgrid(self.__x_arr, self.__y_arr)
        self.ax.plot_surface(x_arr, y_arr, self.data_arr, rstride=1, cstride=1, cmap=plt.cm.get_cmap('Blues_r'))
        self.canvas.draw_idle()

    def draw_graph(self):
        while not self.quit:
            try:
                time.sleep(0.5)
                self.canvas.draw_idle()
            except Exception as e:
                self.quit = True
                print(str(e))
                exit(0)

    def update_file(self, dto_x, dto_y, dto_z):
        while not self.quit:
            try:
                time.sleep(0.1)
                if self.condition_add_point:
                    GraphFrame.write_data_to_json_file('data.json', dto_x)
                    GraphFrame.write_data_to_json_file('data.json', dto_y)
                    GraphFrame.write_data_to_json_file('data.json', dto_z)
            except Exception as e:
                self.quit = True
                print(str(e))
                exit(0)

    @staticmethod
    def write_data_to_json_file(file_name: str, dto):
        if os.path.exists(file_name):
            with open(file_name, 'rb+') as data_file:
                data_file.seek(-1, os.SEEK_END)
                data_file.truncate()
            with open(file_name, 'a') as data_file:
                data_file.write(f",{json.dumps(dto)}]")
        else:
            with open(file_name, 'a') as data_file:
                data_file.write(f"[{json.dumps(dto)}]")

    @staticmethod
    def read_json_file(file_name: str):
        if os.path.exists(file_name):
            with open(file_name, 'r') as data_file:
                return json.load(data_file)
