import matplotlib as plt
import time
from esp8266.scanAlgorithm import ScanAlgorithm
from graph import Graph, GraphFrame
from tkinter import Frame, Button, Scale, Canvas, StringVar, Entry, constants as c
import tkinter as tk
from dto import Dto
import threading

RELWIDTH = 0.7

CANVAS_SIZE = 1000

WINDOW_SIZE = '800x600'
FRAME_COLOR = '#3d3d42'
MAX = 49
MIN = 0
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

        self.constructorFrames = ConstructorFrames(self)
        self.constructorFrames.pack()

        self.graph = Graph()
        self.graph.after_idle(self.update_graph)

    def update_graph(self):
        try:
            self.graph.frame.update_data(
                int(self.constructorFrames.scale_dto_x.var['data']),
                int(self.constructorFrames.scale_dto_y.var['data']),
                int(self.constructorFrames.scale_dto_z.var['data']),
            )
            self.graph.after(50, lambda: self.update_graph())

        except Exception as e:
            print(str(e))
            exit(0)

    def custom_mainloop(self):
        try:
            threading.Thread(target=self.graph.frame.draw_graph).start()
            self.graph.mainloop()
            self.mainloop()
        except Exception as e:
            print(str(e))
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

        self.scale_dto_x = Dto(Dto.SERVO_X, self.__frame_debug, side=c.LEFT)
        self.__scale_x = Scale(self.__frame_top, from_=MAX, to=MIN, length=LENGTH, label='x',
                               command=self.scale_dto_x.on_scale)
        self.scale_dto_y = Dto(Dto.SERVO_Y, self.__frame_debug, side=c.RIGHT)
        self.__scale_y = Scale(self.__frame_top, from_=MAX, to=MIN, length=LENGTH, label='y',
                               command=self.scale_dto_y.on_scale)
        self.scale_dto_z = Dto(Dto.SERVO_Z, self.__frame_debug, c.LEFT)
        self.__scale_z = Scale(self.__frame_top, orient='horizontal', from_=MIN, to=MAX, length=LENGTH, label='z',
                               command=self.scale_dto_z.on_scale)

        self.__auto_on_off_btn = Button(self.__frame_bottom_1, text='go/stop auto_scan ', command=self.auto)
        self.__build_surface_btn = Button(self.__frame_bottom_1, text='on/off build surface', command=self.__build_surface)
        self.__stop_render_btn = Button(self.__frame_bottom_1, text='stop/go render', command=self.__stop_go_render)
        self.__snap_to_point_btn = Button(self.__frame_bottom_2, text='snap_to_point', command=self.__snap_to_point)
        self.__remove_surface_btn = Button(self.__frame_bottom_2, text='remove_surface', command=self.__remove_surface)
        self.__show_surface_btn = Button(self.__frame_bottom_2, text='show_surface', command=self.__show_surface)
        self.__file_name = StringVar()
        self.__save_data_entry = Entry(self.__frame_debug, textvariable=self.__file_name)
        self.__save_data_entry.place(width=20, height=5)
        self.__save_data_btn = Button(self.__frame_debug, text='save data', command=self.__save_file)
        self.__load_data_entry = Entry(self.__frame_debug, textvariable=self.__file_name)
        self.__load_data_entry.place(width=20, height=5)
        self.__load_data_btn = Button(self.__frame_debug, text='load data', command=self.__load_file)


        self.scanAlgorithm = ScanAlgorithm()


    def __snap_to_point(self):
        self.__scale_x.set(self.scale_dto_x.var['data'])
        self.__scale_y.set(self.scale_dto_y.var['data'])
        self.__scale_z.set(self.scale_dto_z.var['data'])

    def __remove_surface(self):
        self.tk.graph.frame.remove_surface()

    def __show_surface(self):
        self.tk.graph.frame.show_surface()

    def __build_surface(self):
        if self.tk.graph.frame.condition_build_surface:
            self.tk.graph.frame.condition_build_surface = False
        else:
            self.tk.graph.frame.condition_build_surface = True

    def __save_file(self):
        GraphFrame.write_data_to_json_file(self.__file_name.get(), self.tk.graph.frame.data_arr.tolist())

    def __load_file(self):
        pass

    def auto(self):
        if self.scanAlgorithm.stop:
            self.scanAlgorithm.stop = False
            threading.Thread(target=self.__go_auto).start()
        else:
            self.scanAlgorithm.stop = True

    def __go_auto(self):
        self.gen = self.scanAlgorithm.data_generator()
        while not self.scanAlgorithm.stop:
            time.sleep(0.11)
            try:
                x, y, z = next(self.gen)
                self.scale_dto_x.var['data'] = x
                self.scale_dto_y.var['data'] = y
                self.scale_dto_z.var['data'] = z
            except Exception as e:
                print(str(e))

    def __stop_go_render(self):
        if self.tk.graph.frame.quit:
            self.tk.graph.frame.quit = False
            threading.Thread(target=self.tk.graph.frame.draw_graph).start()
        else:
            self.tk.graph.frame.quit = True

    def pack(self):
        self.__canvas.pack()

        self.__scale_x.pack(side=c.LEFT, padx=10)
        self.__scale_y.pack(side=c.LEFT, padx=10)
        self.__scale_z.pack(side=c.BOTTOM, pady=5)

        self.__auto_on_off_btn.pack(side=c.LEFT)
        self.__build_surface_btn.pack(side=c.LEFT, padx=5)
        self.__stop_render_btn.pack(side=c.LEFT)

        self.__snap_to_point_btn.pack(side=c.LEFT)
        self.__remove_surface_btn.pack(side=c.LEFT, padx=50)
        self.__show_surface_btn.pack(side=c.LEFT)

        self.__save_data_entry.pack(side=c.LEFT)
        self.__save_data_btn.pack(side=c.LEFT, padx=5)
        self.__load_data_entry.pack(side=c.LEFT, padx=5)
        self.__load_data_btn.pack(side=c.LEFT)


    def scale_set(self, x, y, z):
        self.__scale_x.set(x)
        self.__scale_y.set(y)
        self.__scale_z.set(z)
