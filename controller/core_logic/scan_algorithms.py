import time
from typing import Tuple

from controller.constants import *
from controller.core_logic.exceptions.touching_surface import TouchingSurface

FIELD_SIZE = MAX_FIELD_SIZE - 1


class ScanAlgorithms:

    def __init__(self):
        self.stop = True

    def data_generator_x_y(
            self,
            x_min: int = 0,
            y_min: int = 0,
            x_max: int = FIELD_SIZE,
            y_max: int = FIELD_SIZE
    ):
        assert x_max <= FIELD_SIZE and y_max <= FIELD_SIZE
        for y in range(y_min, y_max):
            yield {DTO_Y: y}
            if y % 2 == 0:
                print(f'{int(y*100/y_max)}%')
                for x in range(x_min, x_max):
                    yield {DTO_X: x}
            else:
                for x in range(x_max, x_min - 1, -1):
                    yield {DTO_X: x}
        print('100%')

    def set_algorithm_x_or_y(self, coordinates: Tuple[int, int, int], set_x_or_y_func, set_z_func):
        assert coordinates[2] < MAX_FIELD_SIZE
        time.sleep(SLEEP_BETWEEN_SCAN_ITERATION)
        try:
            set_x_or_y_func((coordinates[0], coordinates[1], coordinates[2]))
        except TouchingSurface as e:
            print(str(e))
            new_coordinates = (coordinates[0], coordinates[1], coordinates[2] + 2)
            set_z_func(new_coordinates)
            self.set_algorithm_x_or_y(new_coordinates, set_x_or_y_func, set_z_func)

    def set_algorithm_z(self, coordinates: Tuple[int, int, int], set_z_func):
        for z in range(coordinates[2], 0, -1):
            if self.stop:
                break
            time.sleep(SLEEP_BETWEEN_SCAN_ITERATION)
            try:
                set_z_func((coordinates[0], coordinates[1], z))
            except TouchingSurface as e:
                print(str(e))
                z_ = z + 10
                if z_ > FIELD_SIZE:
                    z_ = FIELD_SIZE
                time.sleep(SLEEP_BETWEEN_SCAN_ITERATION)
                set_z_func((coordinates[0], coordinates[1], z_))
                break
