from abc import ABC, abstractmethod
import numpy as np
from controller.core_logic.lapshin_algorithm.entity.feature import Feature
from controller.core_logic.scan_algorithms import FIELD_SIZE


class ScannerInterface(ABC):

    @abstractmethod
    def scan_aria_around_feature(self, feature: Feature) -> np.ndarray:
        pass

    @abstractmethod
    def scan_aria(self, x_min: int = 0, y_min: int = 0, x_max: int = FIELD_SIZE, y_max: int = FIELD_SIZE) -> np.ndarray:
        pass

    @abstractmethod
    def go_to_feature(self, feature: Feature) -> None:
        pass

    @abstractmethod
    def go_in_direction(self, vector: np.ndarray) -> None:
        pass

    @abstractmethod
    def switch_scan(self, stop: bool) -> None:
        pass

    @abstractmethod
    def get_scan_aria_center(self, feature) -> tuple:
        pass