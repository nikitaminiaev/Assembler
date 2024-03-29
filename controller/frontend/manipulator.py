import traceback
from time import sleep

import matplotlib as plt

from controller.core_logic.lapshin_algorithm.feature_collection.direction_generator_snake import DirectionGeneratorSnake
from controller.core_logic.scan_algorithms import FIELD_SIZE
from controller.core_logic.exceptions.touching_surface import TouchingSurface
from controller.frontend.graph import Graph, GraphFrame
from tkinter import Frame, Button, Scale, Canvas, StringVar, Entry, Label, constants as c
import tkinter as tk
import threading
from controller.constants import *


RELWIDTH = 0.7
CANVAS_SIZE = 1000
WINDOW_SIZE = '800x600'
FRAME_COLOR = '#3d3d42'

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
        self.graph = Graph()
        self.constructorFrames = ConstructorFrames(self)
        self.constructorFrames.pack()
        self.graph.after_idle(self.update_graph)

    def update_graph(self):
        try:
            self.graph.frame.update_graph_data_algorithm()
            self.graph.after(MS_TO_UPDATE_GRAPH, lambda: self.update_graph())

        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
            self.graph.destroy()
            self.destroy()
            exit(0)

    def custom_mainloop(self):
        try:
            threading.Thread(target=self.graph.frame.draw_graph).start()
            self.graph.frame.atoms_logic.server.set_up()
            self.graph.mainloop()
            self.mainloop()
        except Exception as e:
            print(str(e))
            print(traceback.format_exc())
            self.graph.destroy()
            self.destroy()
            exit(0)

    def custom_destroy(self):
        self.constructorFrames.close()
        sleep(DELAY_BEFORE_DESTROY)
        self.graph.destroy()
        self.destroy()
        exit(0)

class ConstructorFrames:

    def __init__(self, tk: Manipulator):
        self.tk = tk
        self.__canvas = Canvas(tk, height=CANVAS_SIZE, width=CANVAS_SIZE)

        self.create_frames(tk)
        self.crate_scales()
        self.create_entrys_and_labels()
        self.create_buttons()

        self.scanner = self.tk.graph.frame.atoms_logic.create_scanner(self.tk.graph.frame.atoms_logic.touching_surface_event)
        self.__bind_scale_to_tip()

    def create_buttons(self):
        self.__build_surface_btn = Button(self.__bottom_area_1, text='on/off build surface',
                                          command=self.__build_surface)  # не строит поверхноть, но копит данные о ней
        self.__remember_surface_btn = Button(self.__bottom_area_1, text='remember surface',
                                             command=self.__remember_surface)
        self.__remove_noise_btn = Button(self.__bottom_area_1, text='remove noise',
                                         command=self.__remove_noise)

        self.__gen_new_noise_btn = Button(self.__bottom_area_2, text='gen new noise',
                                          command=self.__gen_new_noise)
        # self.__is_it_surface_btn = Button(self.__frame_bottom_1, text='is it surface', bg='#595959',
        # command=self.__is_it_surface)   # кнопка для дебага
        self.__scan_mode = Button(self.__bottom_area_2, text='on/off scan mode',
                                  command=self.__scan_mode)
        self.__del_surface_data_btn = Button(self.__bottom_area_2, text='del surface', command=self.__del_surface_data)

        self.__stop_render_btn = Button(self.__bottom_area_3, text='stop/go render',
                                        command=self.__stop_go_render)
        self.__del_lapshin_data_btn = Button(self.__bottom_area_3, text='del lapshin data',
                                        command=self.__del_lapshin_data)

        self.__auto_on_off_btn = Button(self.__bottom_area_4, text='go/stop auto_scan', bg='#595959', command=self.auto)
        self.__start_lapshin_btn = Button(self.__bottom_area_4, text='start lapshin', command=self.start_lapshin_algorithm)
        self.__reset_offset_btn = Button(self.__bottom_area_4, text='reset offset', command=self.reset_offset)

        self.__bind_to_tip_btn = Button(self.__bottom_area_5, text='bind to tip', command=self.__bind_scale_to_tip)
        self.__display_lapshin_btn = Button(self.__bottom_area_5, text='display lapshin', command=self.__display_lapshin)
        self.__stop_lapshin_btn = Button(self.__bottom_area_5, text='pause lapshin', command=self.__pause_lapshin)
        self.__go_scan_count_btn = Button(self.__bottom_area_5, text='go scan count', command=self.__go_scan_count)
        # self.__remove_surface_btn = Button(self.__frame_bottom_2, text='remove_surface', command=self.__remove_surface)
        # self.__show_surface_btn = Button(self.__frame_bottom_2, text='show_surface', command=self.__show_surface)
        # self.__is_atom_btn = Button(self.__frame_bottom_2, text='is_atom', command=self.__is_atom) # кнопка для дебага
        # self.__is_atom_captured_btn = Button(self.__bottom_area_5, text='is_atom_captured', command=self.__is_atom_captured)

        self.__save_data_btn = Button(self.__frame_debug, text='save data', command=self.__save_file)
        self.__load_data_btn = Button(self.__frame_debug, text='load data', command=self.__load_file)

        self.default_bg = self.__stop_render_btn.cget("background")

    def crate_scales(self):
        self.__scale_z = Scale(self.__frame_top, from_=MAX, to=MIN, length=LENGTH, label='z',
                               command=self.__transmitting_value_z)
        self.__scale_x = Scale(self.__frame_top, orient='horizontal', from_=MIN, to=MAX, length=LENGTH, label='x',
                               command=self.__transmitting_value_x)
        self.__scale_y = Scale(self.__frame_top, orient='horizontal', from_=MIN, to=MAX, length=LENGTH, label='y',
                               command=self.__transmitting_value_y)

    def create_entrys_and_labels(self):
        self.__scan_vars_x_min = StringVar()
        self.__scan_vars_x_max = StringVar()
        self.__scan_vars_y_min = StringVar()
        self.__scan_vars_y_max = StringVar()
        self.__scan_count = StringVar()
        self.__label_x_min = Label(self.__bottom_area_1, text="x_min")
        self.__label_y_min = Label(self.__bottom_area_2, text="y_min")
        self.__label_x_max = Label(self.__bottom_area_3, text="x_max")
        self.__label_y_max = Label(self.__bottom_area_4, text="y_max")
        self.__scan_vars_entry_x_min = Entry(self.__bottom_area_1, textvariable=self.__scan_vars_x_min)
        self.__scan_vars_entry_y_min = Entry(self.__bottom_area_2, textvariable=self.__scan_vars_y_min)
        self.__scan_vars_entry_x_max = Entry(self.__bottom_area_3, textvariable=self.__scan_vars_x_max)
        self.__scan_vars_entry_y_max = Entry(self.__bottom_area_4, textvariable=self.__scan_vars_y_max)
        self.__scan_count_entry = Entry(self.__bottom_area_5, textvariable=self.__scan_count)
        self.__scan_vars_entry_x_min.place(width=5, height=5)
        self.__scan_vars_entry_x_max.place(width=5, height=5)
        self.__scan_vars_entry_y_min.place(width=5, height=5)
        self.__scan_vars_entry_y_max.place(width=5, height=5)
        self.__scan_count_entry.place(width=5, height=5)
        self.__label_x_min.place(width=5, height=5)
        self.__label_x_max.place(width=5, height=5)
        self.__label_y_min.place(width=5, height=5)
        self.__label_y_max.place(width=5, height=5)

        self.__file_name = StringVar()
        self.__save_data_entry = Entry(self.__frame_debug, textvariable=self.__file_name)
        self.__save_data_entry.place(width=20, height=5)
        self.__load_data_entry = Entry(self.__frame_debug, textvariable=self.__file_name)
        self.__load_data_entry.place(width=20, height=5)

    def create_frames(self, tk):
        self.__frame_top = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__frame_top.place(relx=0.15, rely=0.05, relwidth=RELWIDTH, relheight=0.50)
        self.__bottom_area_1 = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__bottom_area_1.place(relx=0.15, rely=0.60, relwidth=RELWIDTH, relheight=0.05)
        self.__bottom_area_2 = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__bottom_area_2.place(relx=0.15, rely=0.65, relwidth=RELWIDTH, relheight=0.05)
        self.__bottom_area_3 = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__bottom_area_3.place(relx=0.15, rely=0.70, relwidth=RELWIDTH, relheight=0.05)
        self.__bottom_area_3 = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__bottom_area_3.place(relx=0.15, rely=0.75, relwidth=RELWIDTH, relheight=0.05)
        self.__bottom_area_4 = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__bottom_area_4.place(relx=0.15, rely=0.80, relwidth=RELWIDTH, relheight=0.05)
        self.__bottom_area_5 = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__bottom_area_5.place(relx=0.15, rely=0.85, relwidth=RELWIDTH, relheight=0.05)
        self.__frame_debug = Frame(tk, bg=FRAME_COLOR, bd=2)
        self.__frame_debug.place(relx=0.15, rely=0.90, relwidth=RELWIDTH, relheight=0.05)

    def __transmitting_value_x(self, x: int):
        y = self.tk.graph.frame.atoms_logic.get_dto_val(DTO_Y)
        z = self.tk.graph.frame.atoms_logic.get_dto_val(DTO_Z)
        try:
            self.tk.graph.frame.atoms_logic.set_val_to_dto(DTO_X, (x, y, z))
        except TouchingSurface as e:
            self.__bind_scale_to_tip()
            print(traceback.format_exc())
            print(str(e))


    def __transmitting_value_y(self, y: int):
        x = self.tk.graph.frame.atoms_logic.get_dto_val(DTO_X)
        z = self.tk.graph.frame.atoms_logic.get_dto_val(DTO_Z)
        try:
            self.tk.graph.frame.atoms_logic.set_val_to_dto(DTO_Y, (x, y, z))
        except TouchingSurface as e:
            self.__bind_scale_to_tip()
            print(traceback.format_exc())
            print(str(e))

    def __transmitting_value_z(self, z: int):
        x = self.tk.graph.frame.atoms_logic.get_dto_val(DTO_X)
        y = self.tk.graph.frame.atoms_logic.get_dto_val(DTO_Y)
        try:
            self.tk.graph.frame.atoms_logic.set_val_to_dto(DTO_Z, (x, y, z))
        except TouchingSurface as e:
            self.__bind_scale_to_tip()
            print(traceback.format_exc())
            print(str(e))

    def __bind_scale_to_tip(self):
        self.__scale_x.set(self.tk.graph.frame.atoms_logic.get_dto_val(DTO_X))
        self.__scale_y.set(self.tk.graph.frame.atoms_logic.get_dto_val(DTO_Y))
        self.__scale_z.set(self.tk.graph.frame.atoms_logic.get_dto_val(DTO_Z))

    def __pause_lapshin(self):
        self.tk.graph.frame.atoms_logic.pause_lapshin()

    def __display_lapshin(self):
        self.tk.graph.frame.atoms_logic.display_lapshin()

    def __del_lapshin_data(self):
        self.tk.graph.frame.atoms_logic.del_lapshin_data()

    def __remove_surface(self):
        self.tk.graph.frame.remove_surface()

    def __show_surface(self):
        self.tk.graph.frame.show_surface()

    def __build_surface(self):
        if self.tk.graph.frame.condition_build_surface:
            self.tk.graph.frame.condition_build_surface = False
            self.__remove_surface()
        else:
            self.tk.graph.frame.condition_build_surface = True
            self.__show_surface()

    def __remember_surface(self):
        self.tk.graph.frame.atoms_logic.remember_surface()

    def __remove_noise(self):
        self.tk.graph.frame.atoms_logic.remove_noise()

    def __gen_new_noise(self):
        self.tk.graph.frame.atoms_logic.gen_new_noise()

    def __del_surface_data(self):
        self.tk.graph.frame.atoms_logic.del_surface_data()

    def __is_it_surface(self):
        if self.tk.graph.frame.atoms_logic.is_surface():
            self.tk.graph.frame.atoms_logic.set_is_surface(False)
        else:
            self.tk.graph.frame.atoms_logic.set_is_surface(True)

    def __scan_mode(self):
        if self.tk.graph.frame.atoms_logic.is_scan_mode():
            self.tk.graph.frame.atoms_logic.set_scan_mode(False)
        else:
            self.tk.graph.frame.atoms_logic.set_scan_mode(True)

    def __save_file(self):
        GraphFrame.write_data_to_json_file(self.__file_name.get(), self.tk.graph.frame.get_data())

    def __load_file(self):
        pass

    def __go_scan_count(self):
        if self.__scan_count.get().strip() == '':
            return
        count = (int(self.__scan_count.get().strip()))
        vars = self.__get_params()
        threading.Thread(target=self.__go_n_scan, args=(count, vars)).start()

    def reset_offset(self):
        self.tk.graph.frame.atoms_logic.reset_offset()

    def __go_n_scan(self, count, vars):
        for _ in range(count):
            self.scanner.scan_algorithm.stop = False
            self._go_auto(*vars)
            self.tk.graph.frame.atoms_logic.remember_surface()
            self.tk.graph.frame.atoms_logic.gen_new_noise()
        self.tk.graph.frame.atoms_logic.remove_noise()

    def auto(self):
        if self.scanner.scan_algorithm.stop:
            self.scanner.scan_algorithm.stop = False
        else:
            self.scanner.scan_algorithm.stop = True
        vars = self.__get_params()
        try:
            threading.Thread(target=self._go_auto, args=vars).start()
        except Exception as e:
            print(traceback.format_exc())
            print(str(e))

    def start_lapshin_algorithm(self):
        vars = self.__get_params()
        try:
            threading.Thread(target=self._go_lapshin_algorithm, args=vars).start()
        except Exception as e:
            print(traceback.format_exc())
            print(str(e))

    def __get_params(self) -> tuple:
        params = ()
        if self.__scan_vars_x_min.get().strip() != '': params += (int(self.__scan_vars_x_min.get().strip()),)
        if self.__scan_vars_y_min.get().strip() != '': params += (int(self.__scan_vars_y_min.get().strip()),)
        if self.__scan_vars_x_max.get().strip() != '': params += (int(self.__scan_vars_x_max.get().strip()),)
        if self.__scan_vars_y_max.get().strip() != '': params += (int(self.__scan_vars_y_max.get().strip()),)

        return params

    def _go_auto(self, x_min: int = 0, y_min: int = 0, x_max: int = FIELD_SIZE, y_max: int = FIELD_SIZE) -> None:
        self.scanner.scan_aria(x_min, y_min, x_max, y_max)

    def _go_lapshin_algorithm(self, x_min: int = 0, y_min: int = 0, x_max: int = FIELD_SIZE, y_max: int = FIELD_SIZE) -> None:
        self.scanner.scan_algorithm.stop = False
        surface = self.scanner.scan_aria(x_min, y_min, x_max, y_max)
        self.tk.graph.frame.atoms_logic.lapshin_searcher.search_features_auto(surface, DirectionGeneratorSnake(), 6)

    def pack(self):
        self.__build_surface_btn.bind('<Button-1>',
                                      lambda e, cause='tk.graph.frame.condition_build_surface': self.change_button(e, cause))
        self.__scan_mode.bind('<Button-1>',
                              lambda e, cause='tk.graph.frame.condition_scan_mode': self.change_button(e, cause))
        # self.__is_it_surface_btn.bind('<Button-1>',
        #                               lambda e, cause='tk.graph.frame.condition_is_it_surface': self.change_button(e, cause))

        self.__stop_render_btn.bind('<Button-1>',
                                    lambda e, cause='tk.graph.frame.quit': self.change_button(e, cause))
        self.__auto_on_off_btn.bind('<Button-1>',
                                    lambda e, cause='scanAlgorithm.stop': self.change_button(e, cause))

        self.__canvas.pack()

        self.__scale_z.pack(side=c.LEFT, pady=5)
        self.__scale_y.pack(side=c.BOTTOM, padx=10)
        self.__scale_x.pack(side=c.BOTTOM, padx=10)

        self.__label_x_min.pack(side=c.LEFT)
        self.__label_x_max.pack(side=c.LEFT)
        self.__label_y_min.pack(side=c.LEFT)
        self.__label_y_max.pack(side=c.LEFT)
        self.__scan_vars_entry_x_min.pack(side=c.LEFT)
        self.__scan_vars_entry_y_min.pack(side=c.LEFT)
        self.__scan_vars_entry_x_max.pack(side=c.LEFT)
        self.__scan_vars_entry_y_max.pack(side=c.LEFT)
        self.__scan_count_entry.pack(side=c.LEFT)
        self.__auto_on_off_btn.pack(side=c.LEFT)
        self.__start_lapshin_btn.pack(side=c.LEFT, padx=5)
        self.__reset_offset_btn.pack(side=c.RIGHT, padx=5)
        self.__del_lapshin_data_btn.pack(side=c.RIGHT, padx=5)
        self.__stop_render_btn.pack(side=c.RIGHT, padx=15)
        self.__scan_mode.pack(side=c.RIGHT, padx=5)
        self.__build_surface_btn.pack(side=c.RIGHT, padx=5)
        self.__remember_surface_btn.pack(side=c.RIGHT, padx=10)
        self.__remove_noise_btn.pack(side=c.RIGHT, padx=5)
        self.__gen_new_noise_btn.pack(side=c.RIGHT, padx=5)
        self.__del_surface_data_btn.pack(side=c.LEFT, padx=5)
        # self.__is_it_surface_btn.pack(side=c.LEFT, padx=5)

        # self.__is_atom_captured_btn.pack(side=c.RIGHT)
        self.__bind_to_tip_btn.pack(side=c.RIGHT, padx=5)
        self.__stop_lapshin_btn.pack(side=c.RIGHT)
        self.__display_lapshin_btn.pack(side=c.RIGHT)
        self.__go_scan_count_btn.pack(side=c.LEFT)
        # self.__remove_surface_btn.pack(side=c.LEFT, padx=50)
        # self.__show_surface_btn.pack(side=c.LEFT)
        # self.__is_atom_btn.pack(side=c.LEFT, padx=5)

        self.__save_data_entry.pack(side=c.LEFT)
        self.__save_data_btn.pack(side=c.LEFT, padx=5)
        self.__load_data_entry.pack(side=c.LEFT, padx=5)
        self.__load_data_btn.pack(side=c.LEFT)

    def scale_set(self, x, y, z):
        self.__scale_x.set((x, y, z))
        self.__scale_y.set((x, y, z))
        self.__scale_z.set((x, y, z))

    def change_button(self, event, cause):
        cause = {
            'scanAlgorithm.stop': {'condition': not self.scanner.scan_algorithm.stop, 'button': self.__auto_on_off_btn},
            'tk.graph.frame.quit': {'condition': not self.tk.graph.frame.stop_graph, 'button': self.__stop_render_btn},
            'tk.graph.frame.condition_build_surface': {'condition': self.tk.graph.frame.condition_build_surface, 'button': self.__build_surface_btn},
            'tk.graph.frame.condition_scan_mode': {'condition': self.tk.graph.frame.atoms_logic.is_scan_mode(), 'button': self.__scan_mode},
            # 'tk.graph.frame.condition_is_it_surface': {'condition': self.tk.graph.frame.atoms_logic.is_it_surface(), 'button': self.__is_it_surface_btn},
        }.get(cause)

        self.cycle_change_bg(cause)

    def cycle_change_bg(self, cause):
        if cause['condition']:
            if self.default_bg == '#595959':
                cause['button'].configure(bg='#d9d9d9')
            else:
                cause['button'].configure(bg='#595959')
        else:
            cause['button'].configure(bg=self.default_bg)


    def __stop_go_render(self):
        if self.tk.graph.frame.stop_graph:
            self.tk.graph.frame.stop_graph = False
            threading.Thread(target=self.tk.graph.frame.draw_graph).start()
        else:
            self.tk.graph.frame.stop_graph = True

    def close(self):
        self.tk.graph.frame.atoms_logic.server.send_data_to_all_clients('stop')
        self.tk.graph.frame.atoms_logic.server.set_down()
        self.tk.graph.frame.close_matplot()
        self.tk.graph.frame.stop_graph = True

