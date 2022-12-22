from abc import ABC, abstractmethod


class Feature(ABC):

    def __init__(self, coordinates: tuple):
        self.coordinates: tuple = coordinates

    @abstractmethod
    def set_coordinates(self, *args) -> None:
        pass

