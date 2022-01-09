import random
import numpy as np
from controller.constants import *

FIELD_SIZE = MAX_FIELD_SIZE - 1


class ScanAlgorithms:

    def __init__(self):
        self.stop = True
        self.__data_arr = np.zeros((FIELD_SIZE + 1, FIELD_SIZE + 1))

    def data_generator(self, x_min: int = 0, y_min: int = 0, x_max: int = FIELD_SIZE, y_max: int = FIELD_SIZE):
        assert x_max <= FIELD_SIZE and y_max <= FIELD_SIZE
        for y in range(y_min, y_max):
            if y % 2 == 0:
                print(f'{int(y*100/y_max)}%')
                for x in range(x_min, x_max):
                    z = random.randint(50, 50)
                    self.__data_arr[y, x] = z
                    yield x, y, z
            else:
                for x in range(x_max, x_min - 1, -1):
                    z = random.randint(50, 50)
                    self.__data_arr[y, x] = z
                    yield x, y, z
        print('100%')
        self.stop = True
