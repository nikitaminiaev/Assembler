import time
from threading import Event
from typing import Tuple

from controller.constants import *
from controller.core_logic.exceptions.touching_surface import TouchingSurface

WAIT_TIMEOUT = 0.2
FIELD_SIZE = MAX_FIELD_SIZE - 1


class ScanAlgorithms:

    def __init__(self, sleep_between_scan_iteration: float):
        self.stop = True
        self.sleep_between_scan_iteration = sleep_between_scan_iteration

    def scan_line_by_line(self, get_val_func, set_x_func, set_y_func, touching_surface_event: Event, **kwargs):
        gen_x_y = self.data_generator_x_y(kwargs['x_min'], kwargs['y_min'], kwargs['x_max'], kwargs['y_max'])
        while not self.stop:
            try:
                next_coordinate = next(gen_x_y, False)
                if not next_coordinate:
                    break
                z = get_val_func(DTO_Z)
                x = get_val_func(DTO_X)
                y = get_val_func(DTO_Y)
                if DTO_X in next_coordinate:
                    touching_surface_event.clear()
                    self.__set_algorithm_x_or_y((next_coordinate[DTO_X], y, z), set_x_func, touching_surface_event)
                if DTO_Y in next_coordinate:
                    touching_surface_event.clear()
                    self.__set_algorithm_x_or_y((x, next_coordinate[DTO_Y], z), set_y_func, touching_surface_event)
                touching_surface_event.wait(WAIT_TIMEOUT)
            except Exception as e:
                print(str(e))
                break

    def data_generator_x_y(
            self,
            x_min: int = 0,
            y_min: int = 0,
            x_max: int = FIELD_SIZE,
            y_max: int = FIELD_SIZE
    ):
        assert x_max <= FIELD_SIZE and y_max <= FIELD_SIZE
        for y in range(y_min, y_max + 1):
            yield {DTO_Y: y}
            if y % 2 == 0:
                print(f'{int(y*100/y_max)}%')
                for x in range(x_min, x_max + 1):
                    yield {DTO_X: x}
            else:
                for x in range(x_max, x_min - 1, -1):
                    yield {DTO_X: x}
        print('100%')

    def __set_algorithm_x_or_y(self, coordinates: Tuple[int, int, int], set_x_or_y_func, touching_surface_event: Event):
        assert coordinates[2] < MAX_FIELD_SIZE
        time.sleep(self.sleep_between_scan_iteration)
        try:
            set_x_or_y_func((coordinates[0], coordinates[1], coordinates[2]))
            touching_surface_event.wait(WAIT_TIMEOUT)
        except TouchingSurface as e:
            print(str(e))
            new_coordinates = (coordinates[0], coordinates[1], coordinates[2] + 10)
            self.__set_algorithm_x_or_y(new_coordinates, set_x_or_y_func, touching_surface_event)
