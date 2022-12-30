from abc import ABC, abstractmethod
from typing import Tuple
import numpy as np
from controller.core_logic.entity.feature import Feature


class FeatureRecognizerInterface(ABC):

    @abstractmethod
    def recognize_feature(self, start_point: Tuple[int, int], surface: np.ndarray, optimal_height: int) -> Feature:
        pass

    @abstractmethod
    def recognize_perimeter(self, start_point: Tuple[int, int], surface: np.ndarray, optimal_height: int) -> np.ndarray:
        pass

    @abstractmethod
    def feature_in_aria(self, coordinates: tuple, figure: np.ndarray) -> bool:
        pass

    @abstractmethod
    def get_center(self, figure: np.ndarray) -> Tuple[int, int]:
        pass
