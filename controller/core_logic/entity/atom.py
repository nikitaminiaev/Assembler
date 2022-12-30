from typing import Tuple
from controller.core_logic.entity.feature import Feature


class Atom(Feature):

    def __init__(self, coordinates: tuple, type: str = 'carbon'):
        super().__init__(coordinates)
        self.type: str = type
        self.is_captured: bool = False
        self.max_rad = 4

    def __eq__(self, other):  # todo добавить сюда сравнение на type
        if not isinstance(other, Atom):
            return False
        return self.coordinates == other.coordinates

    def set_coordinates(self, *args):
        self.coordinates = args

