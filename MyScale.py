from tkinter import Text, WORD


class MyScale:

    def __init__(self):
        self.var = 0
        self.text = Text(width=25, height=5, bg="darkgreen", fg='white', wrap=WORD)
        self.text.pack()

    def on_scale(self, val):
        self.var = int(float(val))
        self.text.insert(1.0, str(self.var))
