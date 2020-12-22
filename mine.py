#!/usr/bin/env python
from manipulator import Manipulator

try:
    root = Manipulator()
    root.custom_mainloop()
except:
    exit(0)
