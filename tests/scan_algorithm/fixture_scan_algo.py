from unittest.mock import call
from controller.constants import MAX

x_min = 1
y_min = 1
x_max = 5
y_max = 5
INITIAL_DATA = (x_min, y_min, x_max, y_max)

X_DATA_WITHOUT_SURFACE = [
    call((5, 0, 75)),
    call((5, 1, 75)),
    call((4, 1, 75)),
    call((3, 1, 75)),
    call((2, 1, 75)),
    call((1, 1, 75)),
    call((1, 2, 75)),
    call((2, 2, 75)),
    call((3, 2, 75)),
    call((4, 2, 75)),
    call((5, 2, 75)),
    call((5, 3, 75)),
    call((4, 3, 75)),
    call((3, 3, 75)),
    call((2, 3, 75)),
    call((1, 3, 75)),
    call((1, 4, 75)),
    call((2, 4, 75)),
    call((3, 4, 75)),
    call((4, 4, 75)),
    call((5, 4, 75)),
    call((5, 5, 75)),
    call((4, 5, 75)),
    call((3, 5, 75)),
    call((2, 5, 75)),
    call((1, 5, 75))
]

Y_DATA_WITHOUT_SURFACE = []

X_DATA_WITH_SURFACE = [call((5, 0, 75))]

Y_DATA_WITH_SURFACE = []

Z_DATA_WITH_SURFACE = [call((0, 0, 75))]
