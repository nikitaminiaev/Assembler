from typing import Tuple


class Tool:

    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.z: int = 0
        self.is_it_surface: bool = False
        self.is_it_atom: bool = False  # TODO реализовать перемещение атома
        self.is_atom_captured: bool = False
