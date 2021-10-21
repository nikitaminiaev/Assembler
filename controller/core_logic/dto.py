import traceback
from typing import Tuple
from numpy import ndarray
from controller.core_logic.exceptions.touching_surface import TouchingSurface
from controller.core_logic.tool import Tool


class Dto:
    SERVO_X = 'servo_x'
    SERVO_Y = 'servo_y'
    SERVO_Z = 'servo_z'
    HALL = 'hall'
    SENSOR = 'sensor'

    COORDINATE_ORDER = {
        SERVO_X: 0,
        SERVO_Y: 1,
        SERVO_Z: 2,
    }

    def __init__(self, sensor_name: str, surface_data: ndarray, tool: Tool):
        self.__var = {
            Dto.SENSOR: sensor_name,
            'value': '0',
        }
        self.__surface_data = surface_data
        self.__tool = tool

    def get_copy_var(self):
        return self.__var.copy()

    def set_val(self, coordinates: Tuple[int, int, int]) -> None:
        try:
            self.__validate_val(coordinates)
            self.__var['value'] = str(coordinates[Dto.COORDINATE_ORDER[self.__var[Dto.SENSOR]]])
        except TouchingSurface as e:
            print(traceback.format_exc())
            print(str(e))

    def get_val(self) -> int:
        return int(self.__var['value'])

    def __validate_val(self, coordinates: tuple) -> None:
        coordinates = tuple(map(int, coordinates))
        if coordinates[2] < int(self.__surface_data.item((coordinates[1], coordinates[0]))):
            raise TouchingSurface()
