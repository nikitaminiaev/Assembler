from tkinter import *
from constructorFrames import ConstructorFrames

root = Tk()

root['bg'] = '#fafafa'
root.title('Name')
root.wm_attributes('-alpha', 0.7)
root.geometry('900x500')

constructorFrames = ConstructorFrames(root)

root.mainloop()
