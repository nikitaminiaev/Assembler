import numpy as np


class Feature:

    def __init__(self, coordinates: tuple):
        self.coordinates: tuple = coordinates
        self.max_rad: int = 0
        self.max_height: int = 0
        self.perimeter_len: int = 0
        self.vector_to_next = None
        self.vector_to_prev = None

    def set_coordinates(self, *args):
        self.coordinates = args

    def to_string(self) -> str:
        vector_to_next_str = None
        vector_to_prev_str = None
        if self.vector_to_next is not None:
            vector_to_next_str = np.array2string(self.vector_to_next)
        if self.vector_to_prev is not None:
            vector_to_prev_str = np.array2string(self.vector_to_prev)
        return f"{self.max_rad}, {self.max_height}, {self.perimeter_len}, {vector_to_next_str}, {vector_to_prev_str}"
