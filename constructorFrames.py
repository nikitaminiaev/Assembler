from tkinter import Frame, Button, Scale, Canvas, constants as c
from scaleDto import ScaleDto

MAX = 100
MIN = 0


class ConstructorFrames:

    def __init__(self, tk: object):
        self.__canvas = Canvas(tk, height=1200, width=600)

        self.__frame_top = Frame(tk, bg='#ffb700', bd=2)
        self.__frame_top.place(relx=0.15, rely=0.50, relwidth=0.7, relheight=0.20)

        self.__frame_bottom = Frame(tk, bg='#ffb700', bd=2)
        self.__frame_bottom.place(relx=0.15, rely=0.70, relwidth=0.7, relheight=0.25)

        self.__btn = Button(self.__frame_bottom, text='Auto on/off', command=self.go_auto)

        self.scale_dto_x = ScaleDto(self.__frame_bottom)
        self.__scale_x = Scale(self.__frame_top, from_=MAX, to=MIN, command=self.scale_dto_x.on_scale)

        self.scale_dto_y = ScaleDto(self.__frame_bottom)
        self.__scale_y = Scale(self.__frame_top, from_=MAX, to=MIN, command=self.scale_dto_y.on_scale)

        self.scale_dto_z = ScaleDto(self.__frame_bottom)
        self.__scale_z = Scale(self.__frame_top, orient='horizontal', from_=MIN, to=MAX, command=self.scale_dto_z.on_scale)

    def go_auto(self):
        pass

    def pack(self):
        self.__canvas.pack()
        self.__btn.pack()
        self.__scale_x.pack(side=c.LEFT, padx=15)
        self.__scale_y.pack(side=c.RIGHT, padx=15)
        self.__scale_z.pack(fill=c.Y, anchor=c.S, pady=70)
