from typing import Tuple

from numpy import ndarray


class Dto:
    SERVO_X = 'servo_x'
    SERVO_Y = 'servo_y'
    SERVO_Z = 'servo_z'
    HALL = 'hall'
    SENSOR = 'sensor'

    ARR = {
        SERVO_X: 0,
        SERVO_Y: 1,
        SERVO_Z: 2,
    }

    def __init__(self, sensor_name: str, surface_data: ndarray):
        self.surface_data = surface_data
        self.__var = {
            Dto.SENSOR: sensor_name,
            'value': '0',
        }

    def get_copy_var(self):
        return self.__var.copy()

    def set_val(self, coordinates: Tuple[int, int, int]) -> None:
        if self.__validate_val(coordinates):
            sensor_ = Dto.ARR[self.__var[Dto.SENSOR]]
            self.__var['value'] = str(coordinates[sensor_])

    def get_val(self) -> int:
        return int(self.__var['value'])

    def __validate_val(self, coordinates: Tuple[int, int, int]) -> bool:
        # if self.__var[Dto.SENSOR] == Dto.SERVO_Z and :

        return True
