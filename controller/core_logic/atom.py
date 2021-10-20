from typing import Tuple

from matplotlib.collections import PathCollection


class Atom:

    def __init__(self, coordinates: tuple, type: str='carbon'):
        self.coordinates: Tuple[int] = coordinates
        self.type: str = type
        self.is_captured: bool = False

    def __eq__(self, other):
        if not hasattr(other, 'coordinates'):
            return False
        return self.coordinates == other.coordinates


    #
    # @staticmethod
    # def set_coordinates(dot: PathCollection, x: int, y: int, z: int) -> None:
    #     dot.__setattr__('_offsets3d', (x, y, z))


if __name__ == '__main__':
    l = [Atom((1, 1, 1)), Atom((1, 2, 1))]
    if Atom((1, 1, 2)) in l:
        a = 1