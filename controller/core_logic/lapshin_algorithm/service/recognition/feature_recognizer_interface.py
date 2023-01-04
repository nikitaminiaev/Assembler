from abc import ABC, abstractmethod
from typing import Tuple, Iterator
import numpy as np
from controller.core_logic.lapshin_algorithm.entity.feature import Feature


class FeatureRecognizerInterface(ABC):

    @abstractmethod
    def recognize_feature(self, figure: np.ndarray, surface: np.ndarray) -> Feature:
        pass

    @abstractmethod
    def recognize_all_figure_in_aria(self, surface: np.ndarray) -> Iterator[np.ndarray]:
        pass

    @abstractmethod
    def feature_in_aria(self, coordinates: tuple, figure: np.ndarray) -> bool:
        pass

    @abstractmethod
    def get_center(self, figure: np.ndarray) -> Tuple[int, int]:
        pass

    @abstractmethod
    def calc_optimal_height(self, surface_copy: np.ndarray) -> int:
        pass

    @abstractmethod
    def get_max_height(self, surface_copy: np.ndarray) -> int:
        pass

    @abstractmethod
    def calc_max_feature_rad(self, center: tuple, figure: np.ndarray) -> float:
        pass
