from tkinter import Frame, Button, Scale
from scaleDto import ScaleDto


class ConstructorFrames:

    def __init__(self, tk: object):
        self.frame_bottom = Frame(tk, bg='#ffb700', bd=5)
        self.frame_bottom.place(relx=0.15, rely=0.55, relwidth=0.7, relheight=0.1)

        self.frame_top = Frame(tk, bg='#ffb700', bd=5)
        self.frame_top.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.25)
        self.btn = Button(self.frame_bottom, text='Автоматический режим', command=self.go_auto)

        scale_dto1 = ScaleDto()
        self.scale1 = Scale(self.frame_top, from_=100, to=0, command=scale_dto1.on_scale)

        scale_dto2 = ScaleDto()
        self.scale2 = Scale(self.frame_top, from_=100, to=0, command=scale_dto2.on_scale)

        scale_dto3 = ScaleDto()
        self.scale3 = Scale(self.frame_top, orient='horizontal', from_=0, to=100, command=scale_dto3.on_scale)

    def go_auto(self):
        pass

    def pack(self):
        self.btn.pack()
        self.scale1.pack(side='left', padx=15)
        self.scale2.pack(side='right', padx=15)
        self.scale3.pack(side='top', pady=50)
