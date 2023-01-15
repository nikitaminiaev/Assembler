import numpy as np


class DirectionGeneratorSnake:

    @staticmethod
    def generate_next_direction(count: int) -> np.ndarray:
        x = 3
        y = 0
        if count < 5:
            x = 0
            y = 3
        return np.array([x, y], dtype='int8')
