from typing import List, Tuple
import json
from controller.core_logic.atom import Atom
from controller.core_logic.dto import Dto
from controller.core_logic.tool import Tool
from sockets import server

MULTIPLICITY = 1


class AtomsLogic:

    def __init__(self):
        self.dto_x = Dto(Dto.SERVO_X)
        self.dto_y = Dto(Dto.SERVO_Y)
        self.dto_z = Dto(Dto.SERVO_Z)
        self.is_it_surface: bool = True
        self.is_it_atom: bool = False  # TODO реализовать перемещение атома
        self.server = server.Server()
        self.__atoms_list: List[Atom] = []
        self.__tool = Tool()

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

    def update_tool_coordinate(self, x_dict: dict, y_dict: dict, z_dict: dict):
        self.__set_command_to_microcontroller(x_dict, y_dict, z_dict)
        self.__tool.x = x_dict['value']
        self.__tool.y = y_dict['value']
        self.__tool.z = z_dict['value']

    def __set_command_to_microcontroller(self, x_dict, y_dict, z_dict):
        if x_dict['value'] != self.__tool.x:
            # print(x_dict)
            self.server.send_data_to_all_clients(json.dumps(x_dict.copy()))
        if y_dict['value'] != self.__tool.y:
            # print(y_dict)
            self.server.send_data_to_all_clients(json.dumps(y_dict.copy()))
        if z_dict['value'] != self.__tool.z:
            # print(z_dict)
            self.server.send_data_to_all_clients(json.dumps(z_dict.copy()))

    def mark_atom_capture(self, *args) -> Tuple[int, ...]:
        for atom in self.__atoms_list:
            is_x_in = atom.coordinates[0] in range(args[0] - 1, args[0] + 2)
            is_y_in = atom.coordinates[1] in range(args[1] - 1, args[1] + 2)
            is_z_in = atom.coordinates[2] in range(args[2] - 3, args[2] + 1)
            if is_x_in and is_y_in and is_z_in:
                atom.is_captured = True
                return atom.coordinates
        return (0, 0, 0)