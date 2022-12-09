from threading import Event
from typing import Tuple, List
import numpy as np


class BindingProbeToFeature:
    """
    1. Изображение, заданное в некотором окне, просматривается до тех пор, пока не будет
    встречена точка, имеющая высоту большую z, т. е. первая точка, принадлежащая контуру
    очередной области. Найденная точка становится текущей; (особенность - имеет высоту больше чем общий шум)
    2. Просматривается восемь соседних к текущей точек, образующих цепной код, 42,45 до тех
    пор, пока не будет обнаружена точка, имеющая высоту большую z. Найденная таким об-
    разом точка становится текущей;
    3. Повторяется пункт 2, пока не будет встречена первая точка границы области, т. е. не
    произойдёт замыкания контура области;
    4. Зная координаты контура области, вычисляются (с точностью до долей пиксела) коор-
    динаты центра тяжести области;
    5. Точкам изображения, принадлежащим распознанной области, присваиваются нулевые
    значения высоты, и если счётчики строки и столбца просматриваемого окна не достигли
    максимального значения, то выполняется переход к пункту 1.
    """

    def __init__(self, get_val_func, set_x_func, set_y_func, touching_surface_event: Event, **kwargs):
        self.local_surface = np.zeros((7, 7))
        self.touching_surface_event = touching_surface_event
        self.set_y_func = set_y_func
        self.set_x_func = set_x_func
        self.get_val_func = get_val_func
        self.delay_between_iterations = 1
        self.stop = True
        self.z_optimal_height = None  # можно вычислить программно после сканирования области local_surface
        self.current_absolute_coordinates_feature = None

    def bind_to_feature(self, start_point: Tuple[int, int]) -> None:
        # сканирование области local_surface

        self.calc_optimal_height(self.local_surface.copy())
        start_point = self.find_start_point()

        coord = self.bypass_feature(start_point)

        centr_coord = self.centroid(coord)

    def calc_optimal_height(self, surface: np.ndarray) -> None:
        def recur_clip(arr: np.ndarray, next_to_clip: int):
            arr = np.clip(arr, 0, next_to_clip)
            if np.amax(arr) != int(arr.mean()):
                next_to_clip = recur_clip(arr, next_to_clip - 1)
            return next_to_clip

        self.z_optimal_height = recur_clip(surface, np.amax(surface)) + 2

    def find_start_point(self) -> Tuple[int, int]:
        # todo должны находится любые стартовые точки на всех поверхности. Фильтровать пройденные фичи будут заранее, обнуляя внутренние области
        def recur_search_point(surface: np.ndarray, z: int, x: int, y: int) -> Tuple[int, int]:
            try:
                if surface[y, x] < z:
                    x, y = recur_search_point(surface, z, x + 1, y + 1)
            finally:
                return x, y

        return recur_search_point(self.local_surface, self.z_optimal_height, 0, 0)

    def bypass_feature(self, start_point: Tuple[int, int]) -> list:
        x_start = start_point[0]
        y_start = start_point[1]
        points = []

        while points[-1] == (x_start, y_start):
            gen = self.__gen_bypass_point(points[-1])
            max_iteration = 8
            for _ in range(max_iteration):
                try:
                    x, y = next(gen)
                except StopIteration:
                    break
                x_prev, y_prev = self.local_surface[-1]
                if self.local_surface[y, x] >= self.z_optimal_height \
                   and self.local_surface[y_prev, x_prev] < self.local_surface[y, x]:
                    points.append((x, y))
                    break

        return points

    def centroid(self, vertexes: List[Tuple[int, int], ...]):
        _x_list = [vertex[0] for vertex in vertexes]
        _y_list = [vertex[1] for vertex in vertexes]
        _len = len(vertexes)
        _x = sum(_x_list) / _len
        _y = sum(_y_list) / _len
        return _x, _y

    def __gen_bypass_point(self, point: Tuple[int, int]):
        """
            обход 8-ми точек по кругу от стартовой
        """
        x = point[0]
        y = point[1]
        y += 1
        yield x, y
        x -= 1
        yield x, y
        for _ in range(2):
            y -= 1
            yield x, y
        for _ in range(2):
            x += 1
            yield x, y
        for _ in range(2):
            y += 1
            yield x, y
