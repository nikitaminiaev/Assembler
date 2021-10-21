from typing import List, Tuple
import json
import numpy as np
from controller.constants import *
from controller.core_logic.atom import Atom
from controller.core_logic.dto import Dto
from controller.core_logic.tool import Tool
from sockets import server

MULTIPLICITY = 1


class AtomsLogic:

    def __init__(self):
        self.surface_data = np.zeros((MAX_FIELD_SIZE, MAX_FIELD_SIZE))
        self.__tool = Tool()
        self.dto_x = Dto(Dto.SERVO_X, self.surface_data, self.__tool)
        self.dto_y = Dto(Dto.SERVO_Y, self.surface_data, self.__tool)
        self.dto_z = Dto(Dto.SERVO_Z, self.surface_data, self.__tool)
        self.dto_z.set_val((0, 0, MAX))
        # self.server = server.Server()
        self.__atoms_list: List[Atom] = []

    def is_it_surface(self) -> bool:
        return self.__tool.is_it_surface

    def set_is_it_surface(self, pred: bool):
        self.__tool.is_it_surface = pred

    def is_it_atom(self) -> bool:
        return self.__tool.is_it_atom

    def set_is_it_atom(self, pred: bool):
        self.__tool.is_it_atom = pred

    def append_unique_atom(self, x: int, y: int, z: int) -> bool:
        atom = Atom((x, y, z))
        if not atom in self.__atoms_list:
            self.__atoms_list.append(atom)
            return True

        return False

    def is_atom_captured(self) -> bool:
        return self.__tool.is_atom_captured

    def is_new_point(self, x: int, y: int, z: int) -> bool:
        return (x != self.__tool.x or y != self.__tool.y or z != self.__tool.z) and \
               ((x % MULTIPLICITY == 0) or (y % MULTIPLICITY == 0) or (z % MULTIPLICITY == 0))

    def update_tool_coordinate(self):
        # self.__set_command_to_microcontroller()
        self.__tool.x = self.dto_x.get_val()
        self.__tool.y = self.dto_y.get_val()
        self.__tool.z = self.dto_z.get_val()

    def __set_command_to_microcontroller(self):
        if self.dto_x.get_val() != self.__tool.x:
            # print(x_dict)
            self.server.send_data_to_all_clients(json.dumps(self.dto_x.get_copy_var()))
        if self.dto_y.get_val() != self.__tool.y:
            # print(y_dict)
            self.server.send_data_to_all_clients(json.dumps(self.dto_y.get_copy_var()))
        if self.dto_z.get_val() != self.__tool.z:
            # print(z_dict)
            self.server.send_data_to_all_clients(json.dumps(self.dto_z.get_copy_var()))

    def mark_atom_capture(self, *args) -> Tuple[int, ...]:
        for atom in self.__atoms_list:
            is_x_in = atom.coordinates[0] in range(args[0] - 1, args[0] + 2)
            is_y_in = atom.coordinates[1] in range(args[1] - 1, args[1] + 2)
            is_z_in = atom.coordinates[2] in range(args[2] - 3, args[2] + 1)
            if is_x_in and is_y_in and is_z_in:
                atom.is_captured = True
                return atom.coordinates
        return (0, 0, 0)