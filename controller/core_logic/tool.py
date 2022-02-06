from typing import Tuple


class Tool:

    def __init__(self):
        self.x: int = 0
        self.y: int = 0
        self.z: int = 0
        self.is_it_surface: bool = False
        self.is_it_atom: bool = False
        self.is_atom_captured: bool = False
        self.scan_mode: bool = True
        self.is_coming_down: bool = False
