from controller.core_logic.lapshin_algorithm.entity.atom import Atom
from controller.core_logic.lapshin_algorithm.entity.feature import Feature

MAX_ATOM_SIZE = 50


class FeatureFactory:

    @staticmethod
    def create(feature_perimeter: int, *coord) -> Feature:
        if (feature_perimeter < MAX_ATOM_SIZE):
            feature = Atom(coord)
        else:
            feature = Feature(coord)

        feature.perimeter_len = feature_perimeter
        return feature
