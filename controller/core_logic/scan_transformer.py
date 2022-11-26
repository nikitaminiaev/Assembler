import numpy as np

from tests.stub_microcontroller.surface_generator import *


class ScanTransformer:

    def __init__(self):
        self.__surfaces = []

    def append_surface(self, surface: np.ndarray):
        self.__surfaces.append(surface)

    def average_by_z(self) -> np.ndarray:
        return np.around(sum(self.__surfaces) / len(self.__surfaces))

    def is_surfaces_not_empty(self) -> bool:
        return len(self.__surfaces) > 0
