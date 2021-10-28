from typing import Tuple


class Atom:

    def __init__(self, coordinates: tuple, type: str = 'carbon'):
        self.coordinates: Tuple[int, ...] = coordinates
        self.type: str = type
        self.is_captured: bool = False

    def __eq__(self, other):  # todo добавить сюда сравнение на type
        if not hasattr(other, 'coordinates'):
            return False
        return self.coordinates == other.coordinates


if __name__ == '__main__':
    l = [Atom((1, 1, 1)), Atom((1, 2, 1))]
    if Atom((1, 1, 2)) in l:
        a = 1
