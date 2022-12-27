from abc import ABC, abstractmethod


class Feature(ABC):

    def __init__(self, coordinates: tuple, max_rad: int, perimeter_len: int):
        self.coordinates: tuple = coordinates
        self.max_rad: int = max_rad
        self.perimeter_len = perimeter_len
        # todo ссылки (вектор 3х мерный) до предыдущего и next фичи


    @abstractmethod
    def set_coordinates(self, *args) -> None:
        pass

