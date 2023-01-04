from typing import List

from controller.core_logic.lapshin_algorithm.entity.atom import Atom
from controller.core_logic.tool import Tool


class AtomCollection:
    def __init__(self, tool: Tool):
        self.__tool = tool
        self.atoms_list: List[Atom] = []

    def append_unique_atom(self) -> bool:
        if not self.__tool.is_atom:
            return False
        atom = Atom(self.__tool.get_coordinate())
        if not self.__tool.is_atom_captured and not atom in self.atoms_list:
            self.atoms_list.append(atom)
            return True

        return False

    def mark_atom_capture(self) -> None:
        for atom in self.atoms_list:
            is_x_in = atom.coordinates[0] in range(self.__tool.x - 1, self.__tool.x + 2)
            is_y_in = atom.coordinates[1] in range(self.__tool.y - 1, self.__tool.y + 2)
            is_z_in = atom.coordinates[2] in range(self.__tool.z - 3, self.__tool.z + 1)
            if is_x_in and is_y_in and is_z_in:
                atom.is_captured = True
                break

    def mark_atom_release(self) -> None:
        for atom in self.atoms_list:
            if atom.is_captured:
                atom.set_coordinates(self.__tool.x, self.__tool.y, self.__tool.z)
                atom.is_captured = False
                return
