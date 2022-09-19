#!/usr/bin/env python
import traceback
from controller.frontend.manipulator import Manipulator

root = Manipulator()
try:
    root.custom_mainloop()
except Exception as e:
    print(str(e))
    print(traceback.format_exc())
    root.destroy()
    exit(0)
