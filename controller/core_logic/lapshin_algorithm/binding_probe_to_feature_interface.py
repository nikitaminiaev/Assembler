from abc import ABC, abstractmethod
from typing import Tuple
from controller.core_logic.entity.feature import Feature


class BindingProbeToFeatureInterface(ABC):

    @abstractmethod
    def bind_to_feature(self, feature: Feature) -> None:
        pass

    @abstractmethod
    def return_to_feature(self, feature: Feature) -> Tuple[int, int]:
        pass