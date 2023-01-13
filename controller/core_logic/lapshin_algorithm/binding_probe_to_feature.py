import traceback
from threading import Event
from time import sleep
from typing import Tuple
import numpy as np
from controller.core_logic.lapshin_algorithm.entity.feature import Feature
from controller.core_logic.lapshin_algorithm.binding_probe_to_feature_interface import BindingProbeToFeatureInterface
from controller.core_logic.lapshin_algorithm.service.recognition.feature_recognizer_interface import FeatureRecognizerInterface
from controller.core_logic.lapshin_algorithm.service.scanner_around_feature import ScannerAroundFeature
from controller.core_logic.lapshin_algorithm.service.vector_operations import VectorOperations
from controller.core_logic.service.feature_scanner import ScannerInterface



class BindingProbeToFeature(BindingProbeToFeatureInterface):

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

    def __init__(self, feature_recognizer: FeatureRecognizerInterface, scanner: ScannerInterface, binding_in_delay: Event, allow_binding: Event):
        self.scanner = scanner
        self.feature_recognizer = feature_recognizer
        self.current_feature = None
        self.delay = 0.05
        self.stop = False
        self.binding_in_delay = binding_in_delay
        self.allow_binding = allow_binding
        self.scanner_around_feature = ScannerAroundFeature(scanner)

    def bind_to_current_feature(self) -> None:
        while not self.stop:
            self.allow_binding.wait()
            try:
                correction = self.return_to_feature(self.current_feature)
                self.__correct_delay(*correction)
            except Exception as e:
                self.stop = True
                print(e)
                print(traceback.format_exc())
            self.binding_in_delay.set()
            sleep(self.delay)
            self.binding_in_delay.clear()

    def set_current_feature(self, feature: Feature) -> None:
        self.current_feature = feature

    def return_to_feature(self, feature: Feature) -> Tuple[int, int]:
        surface = self.scanner_around_feature.scan_aria_around_current_position(int(round(feature.max_rad)) * 3)
        feature_height = self.feature_recognizer.get_max_height(surface.copy())
        figure_gen = self.feature_recognizer.recognize_all_figure_in_aria(surface)
        for figure in figure_gen:
            if self.feature_recognizer.feature_in_aria(self.scanner.get_scan_aria_center(surface), figure):
                actual_center = self.feature_recognizer.get_center(figure)
                hypothetical_center = self.scanner.get_scan_aria_center(surface)
                correction = self.__calc_correction(actual_center, hypothetical_center)
                self.__update_feature_coord(feature, figure, correction, feature_height, actual_center)
                self.scanner.go_to_direction(np.asarray((*correction, feature_height)))
                return correction
        raise RuntimeError('feature not found')

    def jumping(self, current_feature: Feature, next_feature: Feature) -> None:
        self.binding_in_delay.wait()
        self.allow_binding.clear()
        self.scanner.go_to_direction(current_feature.vector_to_next)
        x_correction, y_correction = self.return_to_feature(next_feature)
        current_feature.vector_to_next[0] += x_correction
        current_feature.vector_to_next[1] += y_correction
        next_feature.vector_to_prev = VectorOperations.get_reverse_vector(current_feature.vector_to_next)
        #todo вычислять точный вектора до фич и усреднять вектор

    def set_stop(self, is_stop: bool) -> None:
        self.stop = is_stop

    def __update_feature_coord(self, feature: Feature, figure, correction, feature_height, actual_center):
        feature.set_coordinates(
            feature.coordinates[0] + correction[0],
            feature.coordinates[1] + correction[1],
            feature_height,
            )
        feature.max_height = feature_height
        if feature.max_rad == 0: feature.max_rad = self.feature_recognizer.calc_max_feature_rad(actual_center, figure)
        if feature.perimeter_len == 0: feature.perimeter_len = len(figure)

    def __calc_correction(self, actual_center: tuple, hypothetical_center: tuple):
        x_correct = actual_center[0] - hypothetical_center[0]
        y_correct = actual_center[1] - hypothetical_center[1]
        return x_correct, y_correct

    def __correct_delay(self, x: int, y: int):
        pass
