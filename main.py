#!/usr/bin/env python
import traceback
from controller.manipulator import Manipulator

try:
    root = Manipulator()
    root.custom_mainloop()
except Exception as e:
    print(str(e))
    print(traceback.format_exc())
    exit(0)
