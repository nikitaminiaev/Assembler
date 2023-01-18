#!/usr/bin/env python
import traceback
from time import sleep

from controller.frontend.manipulator import Manipulator

root = Manipulator()


def on_closing():
    root.custom_destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.graph.protocol("WM_DELETE_WINDOW", on_closing)

try:
    root.custom_mainloop()
except Exception as e:
    print(str(e))
    print(traceback.format_exc())
    root.destroy()
    exit(0)
