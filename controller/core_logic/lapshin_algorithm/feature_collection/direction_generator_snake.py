import numpy as np

from controller.core_logic.lapshin_algorithm.feature_collection.direction_generator_interface import \
    DirectionGeneratorInterface


class DirectionGeneratorSnake(DirectionGeneratorInterface):

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

