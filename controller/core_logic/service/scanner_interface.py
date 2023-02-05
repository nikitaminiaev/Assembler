from abc import ABC, abstractmethod
import numpy as np


class ScannerInterface(ABC):

    @abstractmethod
    def scan_aria(self, x_min: int, y_min: int, x_max: int, y_max: int) -> np.ndarray:
        pass

    @abstractmethod
    def go_to_direction(self, vector: np.ndarray) -> None:
        pass

    @abstractmethod
    def get_current_position(self) -> tuple:
        pass