from abc import ABC, abstractmethod
import numpy as np

from controller.core_logic.lapshin_algorithm.entity.feature import Feature
from controller.core_logic.lapshin_algorithm.feature_collection.direction_generator_interface import \
    DirectionGeneratorInterface


class FeatureSearcherInterface(ABC):

    @abstractmethod
    def search_features_auto(self, surface: np.ndarray, direction_generator: DirectionGeneratorInterface, max_feature_count: int) -> None:
        pass

    @abstractmethod
    def find_first_feature(self, surface: np.ndarray) -> Feature:
        pass

    @abstractmethod
    def recur_find_next_feature(self, current_feature: Feature, next_direction: np.ndarray, count_feature_rad: int) -> Feature:
        pass

    @abstractmethod
    def average_vector_between_features(self, current_feature: Feature, next_feature: Feature) -> None:
        pass

    @abstractmethod
    def join_next_feature(self, next_feature: Feature, vector_to_next_feature: np.ndarray) -> None:
        pass

    @abstractmethod
    def pause_algorithm(self):    #временно
        pass

