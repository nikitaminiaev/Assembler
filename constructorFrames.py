from tkinter import Frame, Button, Scale
from scaleDto import ScaleDto

class ConstructorFrames:

    def __init__(self, tk: object):
        self.frame_bottom = Frame(tk, bg='#ffb700', bd=5)
        self.frame_bottom.place(relx=0.15, rely=0.55, relwidth=0.7, relheight=0.1)

        self.frame_top = Frame(tk, bg='#ffb700', bd=5)
        self.frame_top.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.25)
        self.btn = Button(self.frame_bottom, text='Автоматический режим', command=self.go_auto)
        self.btn.pack()

        v1 = ScaleDto()
        self.scale1 = Scale(self.frame_top, from_=100, to=0, command=v1.on_scale)
        self.scale1.pack(side='left', padx=15)

        v2 = ScaleDto()
        self.scale2 = Scale(self.frame_top, from_=100, to=0, command=v2.on_scale)
        self.scale2.pack(side='right', padx=15)

        v3 = ScaleDto()
        self.scale3 = Scale(self.frame_top, orient='horizontal', from_=0, to=100, command=v3.on_scale)
        self.scale3.pack(side='top', pady=50)

    def go_auto(self):
        pass