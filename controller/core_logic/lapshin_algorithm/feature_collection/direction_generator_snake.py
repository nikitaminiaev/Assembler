import numpy as np


class DirectionGeneratorSnake:

    @staticmethod
    def generate_next_direction(count: int) -> np.ndarray:
        x = 1
        y = 0
        if count < 4:
            x = 0
            y = 1
        if count == 4:
            x = -1
            y = 1
        if count > 4:
            x = -1
            y = 0
        return np.array([x, y], dtype='int8')

