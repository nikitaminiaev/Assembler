import random
import numpy as np
from .constants import *
# import constants

FIELD_SIZE = MAX_FIELD_SIZE - 1


class ScanAlgorithms:

    def __init__(self):
        self.stop = True
        self.__data_arr = np.zeros((FIELD_SIZE + 1, FIELD_SIZE + 1))

    def data_generator(self):
        for y in range(FIELD_SIZE):
            if y % 2 == 0:
                print(f'{int(y*100/FIELD_SIZE)}%')
                for x in range(FIELD_SIZE):
                    z = random.randint(5, 8)
                    self.__data_arr[y, x] = z
                    yield x, y, z
            else:
                for x in range(FIELD_SIZE, -1, -1):
                    z = random.randint(5, 8)
                    self.__data_arr[y, x] = z
                    yield x, y, z

        self.stop = True
