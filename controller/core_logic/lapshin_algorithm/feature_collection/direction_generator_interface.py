from abc import ABC, abstractmethod
import numpy as np


class DirectionGeneratorInterface(ABC):

    @staticmethod
    @abstractmethod
    def generate_next_direction(count: int) -> np.ndarray:
        pass
