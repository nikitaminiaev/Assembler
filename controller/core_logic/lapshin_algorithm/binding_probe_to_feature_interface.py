from abc import ABC, abstractmethod
from typing import Tuple
from controller.core_logic.lapshin_algorithm.entity.feature import Feature


class BindingProbeToFeatureInterface(ABC):

    @abstractmethod
    def bind_to_current_feature(self) -> None:
        pass

    @abstractmethod
    def set_current_feature(self, feature: Feature) -> None:
        pass

    @abstractmethod
    def return_to_feature(self, feature: Feature) -> Tuple[int, int]:
        pass

    @abstractmethod
    def set_stop(self, is_stop: bool) -> None:
        pass

    @abstractmethod
    def jumping(self, current_feature: Feature, next_feature: Feature, jump_count: int) -> None:
        pass
