from random import random
from tkinter import *
from constructorFrames import ConstructorFrames
import matplotlib as plt
from time import time as timer
from threading import Thread

from graph import SeaofBTCapp

plt.use("TkAgg")

root = Tk()

root['bg'] = '#fafafa'
root.title('Name')
root.wm_attributes('-alpha', 0.7)
root.geometry('600x1200')

constructorFrames = ConstructorFrames(root)
constructorFrames.pack()

x = constructorFrames.scale_dto_x
y = constructorFrames.scale_dto_y

app = SeaofBTCapp(dto_x=x, dto_y=y)


def update():
    # root.after(100, update(x))
    app.frame.update_data(int(random()*100), 10)

    app.after(100, lambda: update())


app.after_idle(update)
# root.after(100, update())
# root.after(1000, update())
# Thread(target=update, args=[], daemon=True).start()
root.mainloop()
app.mainloop()
