from tkinter import *
# from tkinter.ttk import Frame, Label, Scale, Style
from MyScale import MyScale

root = Tk()

root['bg'] = '#fafafa'
root.title('Name')
root.wm_attributes('-alpha', 0.7)
root.geometry('900x500')

frame_bottom = Frame(root, bg='#ffb700', bd=5)
frame_bottom.place(relx=0.15, rely=0.55, relwidth=0.7, relheight=0.1)

frame_top = Frame(root, bg='#ffb700', bd=5)
frame_top.place(relx=0.15, rely=0.15, relwidth=0.7, relheight=0.25)


def go_auto():
    pass


def on_scale(val):
    text.insert(1.0, str(val))
    return int(float(val))


btn = Button(frame_bottom, text='Автоматический режим', command=go_auto)
btn.pack()

v1 = MyScale()
scale1 = Scale(frame_top, from_=100, to=0, command=v1.on_scale)
scale1.pack(side='left', padx=15)

v2 = MyScale()
scale2 = Scale(frame_top, from_=100, to=0, command=v2.on_scale)
scale2.pack(side='right', padx=15)

v3 = MyScale()
scale3 = Scale(frame_top, orient='horizontal', from_=0, to=100, command=v3.on_scale)
scale3.pack(side='top', pady=50)

root.mainloop()
