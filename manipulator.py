import matplotlib as plt
import sys
from graph import SeaofBTCapp
from tkinter import Frame, Button, Scale, Canvas, constants as c
import tkinter as tk
from scaleDto import ScaleDto


class Manipulator(tk.Tk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        plt.use("TkAgg")

        self['bg'] = '#fafafa'
        self.title('Name')
        self.wm_attributes('-alpha', 0.7)
        self.geometry('600x1200')

        self.constructorFrames = ConstructorFrames(self)
        self.constructorFrames.pack()

        x = self.constructorFrames.scale_dto_x
        y = self.constructorFrames.scale_dto_y

        self.app = SeaofBTCapp(dto_x=x, dto_y=y)
        self.app.after_idle(self.update)

    def update(self):
        try:
            self.app.frame.update_data(self.constructorFrames.scale_dto_x.var, self.constructorFrames.scale_dto_y.var)
            self.app.after(100, lambda: self.update())
        except:
            sys.exit()

    def custom_mainloop(self):
        self.app.mainloop()
        self.mainloop()


class ConstructorFrames:
    MAX = 100
    MIN = 0

    def __init__(self, tk: object):
        self.__canvas = Canvas(tk, height=1200, width=600)

        self.__frame_top = Frame(tk, bg='#ffb700', bd=2)
        self.__frame_top.place(relx=0.15, rely=0.50, relwidth=0.7, relheight=0.20)

        self.__frame_bottom = Frame(tk, bg='#ffb700', bd=2)
        self.__frame_bottom.place(relx=0.15, rely=0.70, relwidth=0.7, relheight=0.25)

        self.__btn = Button(self.__frame_bottom, text='Auto on/off', command=self.go_auto)

        self.scale_dto_x = ScaleDto(self.__frame_bottom)
        self.__scale_x = Scale(self.__frame_top, from_=ConstructorFrames.MAX, to=ConstructorFrames.MIN,
                               command=self.scale_dto_x.on_scale)

        self.scale_dto_y = ScaleDto(self.__frame_bottom)
        self.__scale_y = Scale(self.__frame_top, from_=ConstructorFrames.MAX, to=ConstructorFrames.MIN,
                               command=self.scale_dto_y.on_scale)

        self.scale_dto_z = ScaleDto(self.__frame_bottom)
        self.__scale_z = Scale(self.__frame_top, orient='horizontal', from_=ConstructorFrames.MIN,
                               to=ConstructorFrames.MAX,
                               command=self.scale_dto_z.on_scale)

    def go_auto(self):
        pass

    def pack(self):
        self.__canvas.pack()
        self.__btn.pack()
        self.__scale_x.pack(side=c.LEFT, padx=15)
        self.__scale_y.pack(side=c.RIGHT, padx=15)
        self.__scale_z.pack(fill=c.Y, anchor=c.S, pady=70)
