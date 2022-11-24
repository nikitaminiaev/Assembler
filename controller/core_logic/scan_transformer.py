import numpy as np


class ScanTransformer:

    def __init__(self):
        self.surfaces = []

    def average_by_z(self, surface1, surface2, surface3) -> np.ndarray:
        return np.around((surface1 + surface2 + surface3)/3)
