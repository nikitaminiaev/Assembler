import matplotlib

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import pylab
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import cm
import numpy

LARGE_FONT = ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, dto_x=None, dto_y=None, dto_z=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("client")
        self.dto_x = dto_x
        self.dto_y = dto_y
        self.dto_z = dto_z
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frame = PageThree(container, dto_x=self.dto_x, dto_y=self.dto_y, dto_z=self.dto_z)
        self.frames[PageThree] = self.frame
        self.frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class PageThree(tk.Frame):

    def __init__(self, parent, dto_x=None, dto_y=None, dto_z=None, **kw):
        super().__init__(parent, **kw)
        self.dto_x = dto_x
        self.dto_y = dto_y
        self.dto_z = dto_z
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        fig = plt.figure()
        self.ax = fig.add_subplot(111, aspect='equal')
        x = int(self.dto_x.var['data'])
        y = int(self.dto_y.var['data'])
        z = int(self.dto_z.var['data'])
        self.ax.add_artist(Circle(xy=(x, y), radius=1, color='b'))
        plt.xlim(0, 100 + 2)
        plt.ylim(0, 100 + 2)
        plt.draw()
        self.canvas = FigureCanvasTkAgg(fig, self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.canvas.draw_idle()

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_data(self, x=0, y=0, z=0):
        # if x != self.dto_y.var:
        self.ax.add_artist(Circle(xy=(x, y), radius=1, color='b'))
        self.canvas.draw_idle()
