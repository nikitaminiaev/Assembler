import traceback
from typing import List, Tuple
import json
import numpy as np
from controller.constants import *
from controller.core_logic.atom import Atom
from controller.core_logic.dto import Dto
from controller.core_logic.tool import Tool
from sockets import server
import time

MULTIPLICITY = 1


class AtomsLogic:

    def __init__(self):
        self.surface_data = np.zeros((MAX_FIELD_SIZE, MAX_FIELD_SIZE))
        self.__tool = Tool()
        self.dto_x = Dto(Dto.SERVO_X, self.surface_data, self.__tool)
        self.dto_y = Dto(Dto.SERVO_Y, self.surface_data, self.__tool)
        self.dto_z = Dto(Dto.SERVO_Z, self.surface_data, self.__tool)
        self.dto_z.set_val((0, 0, MAX))
        self.atom_captured_event: bool = False
        self.atom_release_event: bool = False
        self.append_unique_atom_event: bool = False
        self.tool_is_coming_down: bool = False
        self.server = server.Server(self.handle_server_data)
        self.atoms_list: List[Atom] = []

    # def update_algorithm(self):
    #     # while True:
    #     #     time.sleep(0.01)
    #     if self.is_new_point():
    #         self.update_tool_coordinate()
    #         self.update_surface()
    #         if self.is_it_atom():
    #             self.append_unique_atom_event = self.append_unique_atom()
    #         # if self.atom_captured_event:
    #         #
    #         #     self.atom_captured_event = False

    def handle_server_data(self, data: str):
        try:
            data_dict = json.loads(data)
        except Exception as e:
            print(str(e))
            json_str = f"{data.split('}')[0]}}}" # todo возможность невалидного json
            print(json_str)
            data_dict = json.loads(json_str)
        if data_dict['sensor'] == 'surface':
            self.set_is_it_surface(bool(data_dict['val']))
            self.update_surface()
        if data_dict['sensor'] == 'atom':
            self.set_is_it_atom(bool(data_dict['val']))

    def update_surface(self):
        if self.is_it_surface():
            self.surface_data[self.dto_y.get_val(), self.dto_x.get_val()] = self.dto_z.get_val()

    def is_it_surface(self) -> bool:
        return self.__tool.is_it_surface

    def set_is_it_surface(self, pred: bool):
        self.__tool.is_it_surface = pred

    def is_it_atom(self) -> bool:
        return self.__tool.is_it_atom

    def set_is_it_atom(self, pred: bool):
        self.__tool.is_it_atom = pred

    def append_unique_atom(self) -> bool:
        atom = Atom(self.get_atom_detect_coordinate())
        if not self.__tool.is_atom_captured and not atom in self.atoms_list:
            self.atoms_list.append(atom)
            return True

        return False

    def is_atom_captured(self) -> bool:
        return self.__tool.is_atom_captured

    def set_is_atom_captured(self, pred: bool):
        if pred and not self.__tool.is_atom_captured:
            self.mark_atom_capture()
            self.atom_captured_event = True
        if self.__tool.is_atom_captured and not pred:
            self.mark_atom_release()
            self.atom_release_event = True
        self.__tool.is_atom_captured = pred

    def is_new_point(self) -> bool:
        return (self.dto_x.get_val() != self.__tool.x or self.dto_y.get_val() != self.__tool.y or self.dto_z.get_val() != self.__tool.z) and \
               ((self.dto_x.get_val() % MULTIPLICITY == 0) or (self.dto_y.get_val() % MULTIPLICITY == 0) or (self.dto_z.get_val() % MULTIPLICITY == 0))

    def update_tool_coordinate(self):
        changing_coordinate = self.__set_command_to_microcontroller()
        if changing_coordinate == 'z' and self.__tool.z > self.dto_z.get_val():
            self.tool_is_coming_down = True
        else:
            self.tool_is_coming_down = False
        self.__tool.x = self.dto_x.get_val()
        self.__tool.y = self.dto_y.get_val()
        self.__tool.z = self.dto_z.get_val()

    def get_tool_coordinate(self):
        return self.__tool.x, self.__tool.y, self.__tool.z

    def get_atom_detect_coordinate(self):
        return self.__tool.x, self.__tool.y, self.__tool.z

    def __set_command_to_microcontroller(self) -> str:
        if self.dto_x.get_val() != self.__tool.x:
            # print(x_dict)
            self.server.send_data_to_all_clients(json.dumps(self.dto_x.to_dict()))
            return 'x'
        if self.dto_y.get_val() != self.__tool.y:
            # print(self.dto_y.to_dict())
            self.server.send_data_to_all_clients(json.dumps(self.dto_y.to_dict()))
            return 'y'
        if self.dto_z.get_val() != self.__tool.z:
            data = self.__invert_data(self.dto_z.to_dict())
            # print(data)
            self.server.send_data_to_all_clients(json.dumps(data))
            return 'z'

    @staticmethod
    def __invert_data(data: dict):
        data['value'] = str(MAX - int(data['value']))
        return data

    def mark_atom_capture(self) -> None:
        for atom in self.atoms_list:
            is_x_in = atom.coordinates[0] in range(self.__tool.x - 1, self.__tool.x + 2)
            is_y_in = atom.coordinates[1] in range(self.__tool.y - 1, self.__tool.y + 2)
            is_z_in = atom.coordinates[2] in range(self.__tool.z - 3, self.__tool.z + 1)
            if is_x_in and is_y_in and is_z_in:
                atom.is_captured = True
                break

    def mark_atom_release(self):
        for atom in self.atoms_list:
            if atom.is_captured:
                atom.set_coordinates(self.__tool.x, self.__tool.y, self.__tool.z)
                atom.is_captured = False
                return
