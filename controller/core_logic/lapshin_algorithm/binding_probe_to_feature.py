from time import sleep
from typing import Tuple

import numpy as np

from controller.core_logic.entity.feature import Feature
from controller.core_logic.lapshin_algorithm.binding_probe_to_feature_interface import BindingProbeToFeatureInterface
from controller.core_logic.lapshin_algorithm.recognition.feature_recognizer_interface import FeatureRecognizerInterface
from controller.core_logic.scan_algorithms import ScanAlgorithms
from controller.core_logic.service.feature_scanner import ScannerInterface



class BindingProbeToFeature(BindingProbeToFeatureInterface):
    COEF_NOISE = 2
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

    def __init__(self, feature_recognizer: FeatureRecognizerInterface, feature_scanner: ScannerInterface):
        self.feature_scanner = feature_scanner
        self.local_surface = None
        self.x_hypothetical_center = 6
        self.y_hypothetical_center = 6 # todo вычислять из радиуса фичи и из x_max...
        self.x_correction = 0
        self.y_correction = 0 # todo сбрасывается при переходе к новой фиче
        self.delay_between_iterations = 0.1
        self.stop = True
        self.optimal_height = None
        self.scan_algorithm = ScanAlgorithms(0)
        self.feature_recognizer = feature_recognizer

    def bind_to_feature(self, feature: Feature) -> None:
        while not self.stop:
            correction = self.return_to_feature(feature)
            self.__correct_delay(*correction)
            sleep(self.delay_between_iterations)

    def return_to_feature(self, feature: Feature) -> Tuple[int, int]:
        self.local_surface = self.feature_scanner.scan_aria_around_feature(feature)
        self.calc_optimal_height(self.local_surface.copy())
        for y, row in enumerate(self.local_surface):
            for x, val in enumerate(row):
                if self.__is_start_point(val):
                    figure = self.feature_recognizer.recognize_perimeter((x, y), self.local_surface, self.optimal_height)
                    if self.feature_recognizer.feature_in_aria((self.x_hypothetical_center, self.y_hypothetical_center), figure):
                        x_correction, y_correction = self.__calc_correction(figure)
                        self.x_correction += x_correction
                        self.y_correction += y_correction
                        self.__update_feature(feature, figure, x_correction, y_correction)
                        self.feature_scanner.go_to_feature(feature)
                        return x_correction, y_correction
        raise RuntimeError('feature not found')

    def __update_feature(self, feature: Feature, figure, x_correction, y_correction):
        feature.set_coordinates(
            feature.coordinates[0] + x_correction,
            feature.coordinates[1] + y_correction,
            self.optimal_height,
            )
        # todo расчет max_rad
        feature.perimeter_len = len(figure)

    def __calc_correction(self, figure):
        actual_center = self.feature_recognizer.get_center(figure)
        x_correct = int(actual_center[0] - self.x_hypothetical_center)
        y_correct = int(actual_center[1] - self.y_hypothetical_center)
        return x_correct, y_correct

    def calc_optimal_height(self, surface_copy: np.ndarray) -> None:
        def recur_clip(arr: np.ndarray, next_to_clip: int):
            arr = np.clip(arr, 0, next_to_clip)
            if np.amax(arr) != int(arr.mean()):
                next_to_clip = recur_clip(arr, next_to_clip - 1)
            return next_to_clip

        self.optimal_height = recur_clip(surface_copy, np.amax(surface_copy)) + self.COEF_NOISE

    def __is_start_point(self, val: int) -> bool:
        return val > self.optimal_height

    def __correct_delay(self, x: int, y: int):
        pass
