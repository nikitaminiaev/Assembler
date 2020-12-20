import matplotlib

matplotlib.use("TkAgg")

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

LARGE_FONT = ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, dto_x=None, dto_y=None, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self)
        tk.Tk.title(self, "client")
        self.dto_x = dto_x
        self.dto_y = dto_y
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frame = PageThree(container, dto_x=self.dto_x, dto_y=self.dto_y)
        self.frames[PageThree] = self.frame
        self.frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class PageThree(tk.Frame):

    def __init__(self, parent, dto_x=None, dto_y=None):
        tk.Frame.__init__(self, parent)
        self.dto_x = dto_x
        self.dto_y = dto_y
        label = tk.Label(self, text="Graph Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        fig = plt.figure()
        self.ax = fig.add_subplot(111, aspect='equal')
        x = self.dto_x.var
        y = self.dto_y.var
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

    def update_data(self, x=0, y=0):
        # if x != self.dto_y.var:
        self.ax.add_artist(Circle(xy=(x, y), radius=1, color='b'))
        self.canvas.draw_idle()

