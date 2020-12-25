import json
import os
import matplotlib as cm

# cm.use("TkAgg")
cm.use('Qt4Agg')
# todo  сделать чтобы красная точка рендерилась без графика
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from colour import Color
import time
import numpy as np

LARGE_FONT = ("Verdana", 12)
MULTIPLICITY = 1
COLOR_DOT = 'g'


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
        self.condition_build_surface = True
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        self.condition_add_point = False
        self.quit = False
        self.__x_previous = 0
        self.__y_previous = 0
        self.__z_previous = 0
        self.dots_graph_list = []
        self.lines_graph_list = []
        self.x_arr, self.y_arr = np.meshgrid(np.arange(0, 50, 1), np.arange(0, 50, 1))
        self.data_arr = np.zeros((50, 50))
        self.surface = None
        self.dots_graph = None
        fig = plt.figure()
        self.ax = fig.add_subplot(111, projection='3d')

        red = Color("blue")
        self.colors = list(red.range_to(Color("white"), 170))

        plt.xlim(0, 50 + 2)
        plt.ylim(0, 50 + 2)

        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_data(self, x=0, y=0, z=0):
        self.condition_add_point = (x != self.__x_previous or y != self.__y_previous or z != self.__z_previous) and \
                                   ((x % MULTIPLICITY == 0) or (y % MULTIPLICITY == 0) or (z % MULTIPLICITY == 0))
        if self.condition_add_point:
            try:
                self.dots_graph.remove()
            except:
                pass
            self.dots_graph = self.ax.scatter(x, y, z, s=5, c=COLOR_DOT, marker='8')
            self.__x_previous = x
            self.__y_previous = y
            self.__z_previous = z
            self.data_arr[y, x] = z
            if self.condition_build_surface:
                self.build_surface()

    def build_dots_graph(self, x, y, z):
        self.dots_graph_list.append(self.ax.scatter(x, y, z, s=2, c=str(self.colors[z]), marker='8'))
        self.ax.plot([x, self.__x_previous], [y, self.__y_previous], [z, self.__z_previous], c=str(self.colors[z]))

    def build_surface(self):
        self.remove_surface()
        self.surface = self.ax.plot_surface(self.x_arr, self.y_arr, self.data_arr,
                                            rstride=1, cstride=1, cmap=plt.cm.get_cmap('Blues'),
                                            )
        self.canvas.draw_idle()

    def remove_surface(self):
        try:
            self.surface.remove()
        except:
            pass

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
