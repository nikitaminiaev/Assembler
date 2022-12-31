from abc import ABC, abstractmethod
import numpy as np
from controller.core_logic.entity.feature import Feature


class ScannerInterface(ABC):

    @abstractmethod
    def scan_aria_around_feature(self, feature: Feature) -> np.ndarray:
        pass

    @abstractmethod
    def go_to_feature(self, feature: Feature) -> None:
        pass

    @abstractmethod
    def go_in_direction(self, vector: np.ndarray) -> None:
        pass