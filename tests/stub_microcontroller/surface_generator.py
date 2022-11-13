import numpy as np

MAX_FIELD_SIZE = 76

# # 1  2  3  4  5  6  7  8  9 10 11 12 13

# [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 1
#  [1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],  # 2
#  [1, 1, 2, 3, 3, 3, 3, 3, 2, 1, 1, 1, 1],  # 3
#  [1, 1, 2, 3, 4, 4, 4, 3, 2, 1, 1, 1, 1],  # 4
#  [1, 1, 2, 3, 4, 5, 4, 3, 2, 1, 1, 1, 1],  # 5
#  [1, 1, 2, 3, 4, 4, 4, 3, 2, 1, 1, 1, 1],  # 6
#  [1, 1, 2, 3, 3, 3, 3, 3, 2, 1, 1, 1, 1],  # 7
#  [1, 1, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1],  # 8
#  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 9
#  [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]  # 10

class SurfaceGenerator:

    def __init__(self, max_field_size: int):
        self.real_surface = np.full((max_field_size, max_field_size), 20)

    def generate(self) -> np.ndarray:
        return self.real_surface


if __name__ == '__main__':
    print(SurfaceGenerator(10).generate())
