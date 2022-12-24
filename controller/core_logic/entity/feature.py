from abc import ABC, abstractmethod


class Feature(ABC):

    def __init__(self, coordinates: tuple, max_rad: int):
        self.coordinates: tuple = coordinates
        self.max_rad: int = max_rad

    @abstractmethod
    def set_coordinates(self, *args) -> None:
        pass

