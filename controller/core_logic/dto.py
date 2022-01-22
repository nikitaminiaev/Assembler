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
        self.sensor_name = sensor_name
        self.__value: int = 0
        self.__surface_data = surface_data
        self.__tool = tool

    def to_dict(self):
        return {
            Dto.SENSOR: self.sensor_name,
            'value': str(self.__value)
        }

    def set_val(self, coordinates: Tuple[int, int, int]) -> None:
        self.__validate_val(coordinates)
        self.__value = int(coordinates[Dto.COORDINATE_ORDER[self.sensor_name]])

    def get_val(self) -> int:
        return self.__value

    def __validate_val(self, coordinates: tuple) -> None:  # todo избавиться от tool.is_it_surface
        coordinates = tuple(map(int, coordinates))
        if (self.sensor_name == Dto.SERVO_X or self.sensor_name == Dto.SERVO_Y) \
                and coordinates[2] < int(self.__surface_data.item((coordinates[1], coordinates[0]))):
            raise TouchingSurface()
        if self.sensor_name == Dto.SERVO_Z and self.__tool.is_it_surface and coordinates[2] < self.__value:
            raise TouchingSurface()
        if self.sensor_name == Dto.SERVO_Z \
                and not self.__tool.is_it_surface \
                and coordinates[2] < self.__value \
                and int(self.__surface_data.item((coordinates[1], coordinates[0]))) > coordinates[2]:
            self.__surface_data[coordinates[1], coordinates[0]] = coordinates[2]
