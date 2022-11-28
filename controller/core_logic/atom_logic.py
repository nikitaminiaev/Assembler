from threading import Event
from typing import Tuple
import json
import numpy as np
from controller.constants import *
from controller.core_logic.atoms_collection import AtomCollection
from controller.core_logic.dto import Dto
from controller.core_logic.origin import Origin
from controller.core_logic.scan_transformer import ScanTransformer
from controller.core_logic.tool import Tool
from sockets.server import Server

DEPARTURE_BY_Z = 10
INVALID_DTO = "Invalid dto"


class AtomsLogic:

    def __init__(
            self,
            x_field_size: int = MAX_FIELD_SIZE,
            y_field_size: int = MAX_FIELD_SIZE,
            server=Server,
    ):
        self.surface_data = np.zeros((x_field_size, y_field_size))
        self.atom_captured_event: bool = False
        self.is_surface_changed_event: bool = True    # это событие оптимизирует нагрузку на процессор
        self.atom_release_event: bool = False
        self.append_unique_atom_event: bool = False   # todo переместить все от чего зависит graph в отдельный класс
        self.__tool = Tool()
        self.dto_x = Dto(Dto.SERVO_X, self.surface_data, self.__tool)
        self.dto_y = Dto(Dto.SERVO_Y, self.surface_data, self.__tool)
        self.dto_z = Dto(Dto.SERVO_Z, self.surface_data, self.__tool)
        self.dto_z.set_val((0, 0, MAX))
        self.server = server(self.handle_server_data)
        self.atom_collection = AtomCollection(self.__tool)
        self.touching_surface_event = Event()
        self.__origin = Origin()
        self.scan_transformer = ScanTransformer()

    def remove_noise(self):
        if self.scan_transformer.is_surfaces_not_empty():
            self.surface_data = self.scan_transformer.average_by_z()
        self.is_surface_changed_event = True

    def remember_surface(self):
        self.scan_transformer.append_surface(self.surface_data.copy())

    def gen_new_noise(self):  #метод для тестовой мк заглушки
        self.server.send_data_to_all_clients('{"sensor": "gen_new_noise", "value": 1}')

    def tool_is_coming_down(self):
        return self.__tool.is_coming_down

    def is_scan_mode(self):
        return self.__tool.scan_mode

    def set_scan_mode(self, pred: bool) -> None:
        self.__tool.scan_mode = pred

    def set_val_to_dto(self, dto_str: str, coordinates: Tuple[int, int, int], is_auto: bool = False) -> None:
        coordinates_int = tuple(map(int, coordinates))
        dto_name = 'dto_' + dto_str
        dto = getattr(self, dto_name, INVALID_DTO)
        if dto == INVALID_DTO:
            raise ValueError(dto)
        dto.validate_val(coordinates_int)
        dto.set_val(coordinates_int)
        # self.update_tool_coordinate(False)  //todo вернуть это, когда в графике перейдет на событие new_point
        self.push_coord_to_mk(dto_str, is_auto)
        if self.__tool.scan_mode and dto_str == DTO_Z:
            self.__update_existing_surface(coordinates_int)

    def __update_existing_surface(self, coordinates: Tuple[int, ...]) -> None:
        if not self.__tool.is_surface \
                and self.__tool.is_coming_down \
                and int(self.surface_data.item((coordinates[1], coordinates[0]))) > coordinates[2]:
            self.surface_data[coordinates[1], coordinates[0]] = coordinates[2] - CORRECTION_Z
            self.is_surface_changed_event = True

    def handle_server_data(self, data: str):
        data_dict = self.remove_noise_and_parse_server_data(data, 0)
        if data_dict == False:
            return
        try:
            is_surface_ = self.__tool.scan_mode and data_dict['sensor'] == 'surface'
            if is_surface_:
                # self.__tool.is_coming_down = True
                z_val_ = data_dict['z_val']
                self.dto_z.set_val((self.dto_x.get_val(), self.dto_y.get_val(), z_val_ + DEPARTURE_BY_Z))
                self.__tool.z = z_val_ + DEPARTURE_BY_Z
                self.set_is_surface(True)
                self.__build_new_surface(z_val_)
                self.touching_surface_event.set()
            # if data_dict['sensor'] == 'atom':  # todo это будет событие atom_captured
            #     self.set_is_atom_captured(bool(data_dict['val']))
        except Exception:
            return

    def remove_noise_and_parse_server_data(self, data: str, i: int = 0):
        try:
            data_dict = json.loads(data)
        except Exception:
            try:
                json_str = f"{data.split('}')[1]}}}"
            except:
                return False
            i += 1
            if i > 1:
                return False
            data_dict = self.remove_noise_and_parse_server_data(json_str, i)  # todo возможно лучше передавать сюда data.split('}')[i]
        return data_dict

    def __build_new_surface(self, z: int):
        if self.is_surface():
            self.surface_data[self.dto_y.get_val(), self.dto_x.get_val()] = z - CORRECTION_Z
            self.is_surface_changed_event = True

    def is_surface(self) -> bool:
        return self.__tool.is_surface

    def set_is_surface(self, pred: bool):
        self.__tool.is_surface = pred

    def is_atom(self) -> bool:
        return self.__tool.is_atom

    def set_is_atom(self, pred: bool):
        self.__tool.is_atom = pred

    def is_atom_captured(self) -> bool:
        return self.__tool.is_atom_captured

    def set_is_atom_captured(self, pred: bool):
        if pred and not self.__tool.is_atom_captured:
            self.atom_collection.mark_atom_capture()
            self.atom_captured_event = True
        if self.__tool.is_atom_captured and not pred:
            self.atom_collection.mark_atom_release()
            self.atom_release_event = True
        self.__tool.is_atom_captured = pred

    def is_new_point(self) -> bool:
        return (self.dto_x.get_val() != self.__tool.x or self.dto_y.get_val() != self.__tool.y or self.dto_z.get_val() != self.__tool.z) and \
               ((self.dto_x.get_val() % MULTIPLICITY == 0) or (self.dto_y.get_val() % MULTIPLICITY == 0) or (self.dto_z.get_val() % MULTIPLICITY == 0))

    def update_tool_coordinate(self) -> None:
        self.__tool.x = self.dto_x.get_val()
        self.__tool.y = self.dto_y.get_val()
        self.__tool.z = self.dto_z.get_val()

    def get_tool_coordinate(self) -> tuple:
        return self.__tool.get_coordinate()

    def set_new_origin_coordinate(self) -> None:
        self.__origin.set_coordinate(self.dto_x.get_val(), self.dto_y.get_val(), self.dto_z.get_val())

    def get_origin_coordinate(self) -> tuple:
        return self.__origin.get_coordinate()

    def set_origin_to_dto(self) -> None:
        z_max = np.amax(self.surface_data)
        self.set_val_to_dto(DTO_Z, (self.dto_x.get_val(), self.dto_y.get_val(), z_max + 10))
        self.update_tool_coordinate()
        self.push_x_coord_to_mk()
        self.set_val_to_dto(DTO_X, self.get_origin_coordinate())
        self.update_tool_coordinate()
        self.push_x_coord_to_mk()
        self.set_val_to_dto(DTO_Y, self.get_origin_coordinate())
        self.update_tool_coordinate()
        self.push_x_coord_to_mk()
        self.set_val_to_dto(DTO_Z, self.get_origin_coordinate())
        self.update_tool_coordinate()
        self.push_x_coord_to_mk()

    def __set_command_to_microcontroller(self) -> None:  # может приходить False
        if self.dto_x.get_val() != self.__tool.x:
            self.push_x_coord_to_mk()
            return
        if self.dto_y.get_val() != self.__tool.y:
            self.push_y_coord_to_mk()
            return
        # if self.dto_z.get_val() != self.__tool.z:
        #     self.server.send_data_to_all_clients(json.dumps(self.dto_z.to_dict()))
        #     return

    def push_coord_to_mk(self, coord: str, auto_mod: bool = False) -> None:
        if coord == DTO_X: self.push_x_coord_to_mk(auto_mod)
        if coord == DTO_Y: self.push_y_coord_to_mk(auto_mod)
        if coord == DTO_Z: self.push_z_coord_to_mk(auto_mod)

    def push_z_coord_to_mk(self, auto_mod: bool = False) -> None:
        dict = self.dto_z.to_dict()
        dict['auto'] = int(auto_mod)
        self.server.send_data_to_all_clients(json.dumps(dict))

    def push_x_coord_to_mk(self, auto_mod: bool = False) -> None:
        dict = self.dto_x.to_dict()
        dict['auto'] = int(auto_mod)
        self.server.send_data_to_all_clients(json.dumps(dict))

    def push_y_coord_to_mk(self, auto_mod: bool = False) -> None:
        dict = self.dto_y.to_dict()
        dict['auto'] = int(auto_mod)
        self.server.send_data_to_all_clients(json.dumps(dict))

    def get_dto_val(self, dto_str: str) -> int:
        dto_name = 'dto_' + dto_str
        dto = getattr(self, dto_name, INVALID_DTO)
        if dto == INVALID_DTO:
            raise ValueError(dto)
        return dto.get_val()

    def set_val_dto_curried(self, dto_str: str):
        def wrap(coordinates: Tuple[int, int, int]):
            self.set_val_to_dto(dto_str, coordinates, True)

        return wrap
