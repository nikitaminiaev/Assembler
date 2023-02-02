import numpy as np
from typing import List, Tuple


class SurfaceGenerator:

    def __init__(self, max_field_size: int, general_height: int, atoms: List[Tuple[int, int]]):
        self.max_field_size = max_field_size
        self.general_height = general_height
        self.atoms = atoms

    def generate(self) -> np.ndarray:
        surface = self.__get_empty_surface()

        return self.__add_atoms(surface, self.atoms)

    def __append_atom(self, surface: np.ndarray, x: int, y: int) -> np.ndarray:
        z = surface[y, x]
        surface[(y - 3):(y + 4), (x - 3):(x + 4)] = z + 1
        surface[(y - 3), (x - 3)] = z
        surface[(y + 3), (x + 3)] = z
        surface[(y - 3), (x + 3)] = z
        surface[(y + 3), (x - 3)] = z
        surface[(y - 2):(y + 3), (x - 2):(x + 3)] = z + 2
        surface[(y - 2), (x - 2)] = z + 1
        surface[(y + 2), (x + 2)] = z + 1
        surface[(y - 2), (x + 2)] = z + 1
        surface[(y + 2), (x - 2)] = z + 1
        surface[(y - 1):(y + 2), (x - 1):(x + 2)] = z + 3
        surface[y, x] = z + 4

        return surface

    def __add_atoms(self, surface: np.ndarray, coordinates: List[Tuple[int, int]]):
        for x, y in coordinates:
            try:
                self.__append_atom(surface, x, y)
            except IndexError as e:
                print(str(e))

        return surface

    def __get_empty_surface(self):
        return np.full((self.max_field_size, self.max_field_size), self.general_height)
