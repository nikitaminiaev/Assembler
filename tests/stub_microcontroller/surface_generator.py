import numpy as np

MAX_FIELD_SIZE = 76


# # 1  2  3  4  5  6  7  8  9 10 11 12 13

# [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 1
#  [1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1],  # 2
#  [1, 1, 2, 2, 3, 3, 3, 2, 2, 1, 1, 1, 1],  # 3
#  [1, 1, 2, 3, 4, 4, 4, 3, 2, 1, 1, 1, 1],  # 4
#  [1, 1, 2, 3, 4, 5, 4, 3, 2, 1, 1, 1, 1],  # 5
#  [1, 1, 2, 3, 4, 4, 4, 3, 2, 1, 1, 1, 1],  # 6
#  [1, 1, 2, 2, 3, 3, 3, 2, 2, 1, 1, 1, 1],  # 7
#  [1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1],  # 8
#  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 9
#  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]  # 10

class SurfaceGenerator:

    def __init__(self, max_field_size: int, general_height: int):
        self.max_field_size = max_field_size
        self.general_height = general_height

    def generate(self) -> np.ndarray:
        real_surface = np.full((self.max_field_size, self.max_field_size), self.general_height)
        surface = self.__add_atom(real_surface, 15, 10)
        noise = self.__get_noise(self.max_field_size)

        return surface + noise

    @staticmethod
    def __add_atom(surface: np.ndarray, x: int, y: int) -> np.ndarray:
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

    @staticmethod
    def __get_noise(max_field_size: int) -> np.ndarray:
        return np.random.choice([-1, 0, +1], (max_field_size, max_field_size), replace=True, p=[0.2, 0.6, 0.2])


if __name__ == '__main__':
    print(SurfaceGenerator(20, 20).generate())
