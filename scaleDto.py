from tkinter import Text, constants as c


class ScaleDto:

    def __init__(self, frame=None, side=c.TOP):
        self.var = 0
        self.text = Text(frame, width=25, height=4, bg="darkgreen", fg='white', wrap=c.WORD)
        self.text.pack(side=side)

    def on_scale(self, val):
        self.var = int(float(val))
        self.text.insert(1.0, str(self.var))
