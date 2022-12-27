from threading import Event
from typing import Tuple
import numpy as np

from controller.core_logic.entity.feature import Feature
from controller.core_logic.lapshin_algorithm.recognition.feature_recognizer_interface import FeatureRecognizerInterface
from controller.core_logic.scan_algorithms import ScanAlgorithms, DTO_Y, DTO_Z

COEF_NOISE = 2


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

    """
    При разности координат более
    45 % от длины усреднённой постоянной решётки процедура привязки фиксирует состоя-
    ние PAF (Probe Attachment Failure) и пытается захватить ближайший атом.
    """

    def __init__(self, FeatureRecognizer: FeatureRecognizerInterface, get_val_func, set_x_func, set_y_func, touching_surface_event: Event, global_surface):
        self.global_surface = global_surface
        self.local_surface = None
        self.x_local_center = 6
        self.y_local_center = 6 # todo вычислять из радиуса фичи и из x_max...
        self.x_correction = 0
        self.y_correction = 0 # todo сбрасывается при переходе к новой фиче
        self.touching_surface_event = touching_surface_event
        self.set_y_func = set_y_func
        self.set_x_func = set_x_func
        self.get_val_func = get_val_func
        self.delay_between_iterations = 0.1
        self.stop = True
        self.optimal_height = None
        self.scan_algorithm = ScanAlgorithms(0)
        self.feature_recognizer = FeatureRecognizer

    def bind_to_feature(self, feature: Feature) -> None:
        self.__scan_aria_around_feature(feature)
        self.calc_optimal_height(self.local_surface.copy())
        for y, row in enumerate(self.local_surface):
            for x, val in enumerate(row):
                if self.is_start_point(val):
                    figure = self.feature_recognizer.recognize((x, y), self.local_surface, self.optimal_height)
                    if self.feature_recognizer.feature_in_aria((self.x_local_center, self.y_local_center), figure):
                        center_coord = self.feature_recognizer.centroid(figure)
                        x_correct = center_coord[0] - self.x_local_center
                        y_correct = center_coord[1] - self.y_local_center
                        self.x_correction += x_correct
                        self.y_correction += y_correct
                        feature.set_coordinates(
                            feature.coordinates[0] + x_correct,
                            feature.coordinates[1] + y_correct,
                            self.optimal_height,
                        )

    def calc_optimal_height(self, surface: np.ndarray) -> None:
        def recur_clip(arr: np.ndarray, next_to_clip: int):
            arr = np.clip(arr, 0, next_to_clip)
            if np.amax(arr) != int(arr.mean()):
                next_to_clip = recur_clip(arr, next_to_clip - 1)
            return next_to_clip

        self.optimal_height = recur_clip(surface, np.amax(surface)) + COEF_NOISE

    def __scan_aria_around_feature(self, feature: Feature) -> None:
        #todo вычислить максимальный радиус фичи и прибавлять к нему const
        x_min = feature.coordinates[0] - 6 # todo вычислять из радиуса фичи
        y_min = feature.coordinates[1] - 6
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

    def is_start_point(self, val: int) -> bool:
        return val > self.optimal_height
