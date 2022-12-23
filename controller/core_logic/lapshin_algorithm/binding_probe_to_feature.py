from threading import Event
from typing import Tuple, List
import numpy as np

from controller.core_logic.entity.feature import Feature
from controller.core_logic.scan_algorithms import ScanAlgorithms, DTO_Y, DTO_Z


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

    def __init__(self, get_val_func, set_x_func, set_y_func, touching_surface_event: Event, global_surface):
        self.global_surface = global_surface
        self.local_surface = None
        self.x_correction = 0
        self.y_correction = 0
        self.touching_surface_event = touching_surface_event
        self.set_y_func = set_y_func
        self.set_x_func = set_x_func
        self.get_val_func = get_val_func
        self.delay_between_iterations = 0.1
        self.stop = True
        self.z_optimal_height = None
        self.scan_algorithm = ScanAlgorithms(0)

    def bind_to_feature(self, feature: Feature) -> None:
        self.__scan_aria_around_feature(feature)
        self.calc_optimal_height(self.local_surface.copy())
        # ----  начало цикла
        # гуляние по local_surface в цикле и делать feature_recognition() если есть start_point
        start_point = self.find_start_point()
        figure = self.feature_recognition(start_point)
        # ---- конец цикла
        center_coord = self.centroid(figure)
        if self.feature_in_aria(feature.coordinates, figure):
            self.x_correction = feature.coordinates[0] - center_coord[0]
            self.y_correction = feature.coordinates[1] - center_coord[1]

    def feature_recognition(self, start_point: Tuple[int, int]) -> np.ndarray: # todo вынести в класс
        figure = self.bypass_feature(start_point)
        self.reset_to_zero_feature_area(figure)
        return figure

    def calc_optimal_height(self, surface: np.ndarray) -> None:
        def recur_clip(arr: np.ndarray, next_to_clip: int):
            arr = np.clip(arr, 0, next_to_clip)
            if np.amax(arr) != int(arr.mean()):
                next_to_clip = recur_clip(arr, next_to_clip - 1)
            return next_to_clip

        self.z_optimal_height = recur_clip(surface, np.amax(surface)) + 2

    def find_start_point(self) -> Tuple[int, int]: # todo заменить на bool функцию котрая будет работать во внешнем цикле
        # todo должны находится любые стартовые точки на всех поверхности. Фильтровать пройденные фичи будут заранее, обнуляя внутренние области
        def recur_search_point(surface: np.ndarray, z: int, x: int, y: int) -> Tuple[int, int]:
            try:
                if surface[y, x] < z:
                    x, y = recur_search_point(surface, z, x + 1, y + 1)
            finally:
                return x, y

        return recur_search_point(self.local_surface, self.z_optimal_height, 0, 0)

    def bypass_feature(self, start_point: Tuple[int, int]) -> np.ndarray:
        x_start = start_point[0]
        y_start = start_point[1]
        points = np.array([[0, 0]], dtype='int8')
        x, y = x_start, y_start
        x_prev, y_prev = x_start, y_start

        while not self.is_vector_entry(points, np.array([x_start, y_start], dtype='int8')):
            gen = self.__gen_bypass_point((x, y))
            max_iteration = 9
            for _ in range(max_iteration):
                try:
                    x, y = next(gen)
                except StopIteration:
                    break
                if self.local_surface[y, x] >= self.z_optimal_height > self.local_surface[y_prev, x_prev] \
                        and self.local_surface[y, x] > self.local_surface[y_prev, x_prev]:
                    points = np.append(points, [[x, y]], axis=0)
                    x_prev, y_prev = x, y
                    break
                x_prev, y_prev = x, y
        return np.delete(points, 0, 0)

    def centroid(self, vertexes: np.ndarray) -> Tuple[int, int]:
        _x_list = vertexes[:, 0]
        _y_list = vertexes[:, 1]
        _len = len(vertexes)
        _x = sum(_x_list) / _len
        _y = sum(_y_list) / _len
        return _x, _y

    def __gen_bypass_point(self, point: Tuple[int, int]):
        """
            обход 8-ми точек против часовой от стартовой
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
        yield x-1, y

    def reset_to_zero_feature_area(self, figure: np.ndarray):
        figtr = np.transpose(figure)
        for st in range(np.min(figtr[0]), np.max(figtr[0]) + 1):
            fig1 = figtr[1][figtr[0] == st]
            self.local_surface[st, np.min(fig1):np.max(fig1) + 1] = 0

    def feature_in_aria(self, feature_coordinates: tuple, figure: np.ndarray) -> bool:
        figtr = np.transpose(figure)
        for st in range(np.min(figtr[0]), np.max(figtr[0]) + 1):
            fig1 = figtr[1][figtr[0] == st]
            for i in range(np.min(fig1),np.max(fig1) + 1):
                if (feature_coordinates[0], feature_coordinates[1]) == (st, i):
                    return True
        return False

    def is_vector_entry(self, arr: np.ndarray, entry: np.ndarray) -> bool:
        return np.isclose(arr - entry, np.zeros(entry.shape)).all(axis=1).any()

    def __scan_aria_around_feature(self, feature: Feature) -> None:
        #todo вычислить максимальный радиус фичи и прибавлять к нему const
        x_min = feature.coordinates[0] - 7
        y_min = feature.coordinates[1] - 7
        x_max = feature.coordinates[0] + 7
        y_max = feature.coordinates[1] + 7

        self.set_x_func(
            x_max,
            self.get_val_func(DTO_Y),
            self.get_val_func(DTO_Z),
        )
        # self.tk.graph.frame.atoms_logic.push_z_coord_to_mk(True)

        self.scan_algorithm.scan_line_by_line(
            self.get_val_func,
            self.set_x_func,
            self.set_y_func,
            self.touching_surface_event,
            x_min=x_min,
            y_min=y_min,
            x_max=x_max,
            y_max=y_max,
        )

        self.fill_local_surface(x_min, y_min, x_max, y_max)

    def fill_local_surface(self, x_min: int, y_min: int, x_max: int, y_max: int): # todo передавать сюда координаты min max coord
        self.local_surface = self.global_surface[y_min:y_max, x_min:x_max].copy()


if __name__ == '__main__':
    points = np.array([[7, 8], [7,9]], dtype='int8')
    e = np.array([7,8], dtype='int8')
    print(points)
    print(np.isclose(points - e, np.zeros(e.shape)).all(axis=1).any())
    # points = np.empty((1,1), dtype='int8')
    # points = np.zeros((1,2))
    # print(points)
    # points = np.append(points, [[1, 2]], axis=0)
    # points = np.append(points, [[4, 5]], axis=0)
    # points = np.append(points, [[5, 5]], axis=0)
    # points = np.append(points, [[8, 5]], axis=0)
    #
    # print(np.delete(points, 0, 0))
    #
    # print(1 in points[:, 0])
    # print(type(points[:, 1]))