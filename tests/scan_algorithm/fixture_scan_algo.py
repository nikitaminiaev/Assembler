from unittest.mock import call
from controller.constants import MAX

x_min = 1
y_min = 1
x_max = 5
y_max = 5
INITIAL_DATA = (x_min, y_min, x_max, y_max)

X_DATA_WITHOUT_SURFACE = [call((5, 0, 75))]

Y_DATA_WITHOUT_SURFACE = []

Z_DATA_WITHOUT_SURFACE = [call((0, 0, 75))]

X_DATA_WITH_SURFACE = [call((5, 0, 75))]

Y_DATA_WITH_SURFACE = []

Z_DATA_WITH_SURFACE = [call((0, 0, 75))]
