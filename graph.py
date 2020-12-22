import matplotlib

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from colour import Color
import time

LARGE_FONT = ("Verdana", 12)


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
        self.quit = False
        self.x = 0
        self.y = 0
        self.z = 0
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
        if x != self.x or y != self.y or z != self.z:
            self.ax.scatter(x, y, z, s=20, c=str(self.colors[z]), marker='8')
            self.x = x
            self.y = y
            self.z = z

    def draw_graph(self):
        while not self.quit:
            try:
                time.sleep(0.5)
                self.canvas.draw_idle()
            except:
                self.quit = True
                exit(0)
