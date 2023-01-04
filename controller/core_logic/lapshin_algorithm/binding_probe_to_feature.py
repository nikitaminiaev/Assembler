import traceback
from time import sleep
from typing import Tuple

from controller.core_logic.lapshin_algorithm.entity.feature import Feature
from controller.core_logic.lapshin_algorithm.binding_probe_to_feature_interface import BindingProbeToFeatureInterface
from controller.core_logic.lapshin_algorithm.service.recognition.feature_recognizer_interface import FeatureRecognizerInterface
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

    def __init__(self, feature_recognizer: FeatureRecognizerInterface, feature_scanner: ScannerInterface):
        self.feature_scanner = feature_scanner
        self.local_surface = None
        self.x_hypothetical_center = 6
        self.y_hypothetical_center = 6 # todo вычисля
        # ть из радиуса фичи и из x_max...
        self.delay_between_iterations = 0.05
        self.stop = False
        self.optimal_height = None
        self.feature_recognizer = feature_recognizer

    def bind_to_feature(self, feature: Feature) -> None:
        while not self.stop:
            try:
                correction = self.return_to_feature(feature)
                self.__correct_delay(*correction)
            except Exception as e:
                self.stop = True
                print(e)
                print(traceback.format_exc())
            sleep(self.delay_between_iterations)

    def return_to_feature(self, feature: Feature) -> Tuple[int, int]:
        surface = self.feature_scanner.scan_aria_around_feature(feature)
        feature_height = self.feature_recognizer.get_max_height(surface.copy())
        figure_gen = self.feature_recognizer.recognize_all_figure_in_aria(surface)
        for figure in figure_gen:
            if self.feature_recognizer.feature_in_aria((self.x_hypothetical_center, self.y_hypothetical_center), figure):
                x_correction, y_correction = self.__calc_correction(figure)
                self.__update_feature(feature, figure, x_correction, y_correction, feature_height)
                self.feature_scanner.go_to_feature(feature)
                return x_correction, y_correction
        raise RuntimeError('feature not found')

    def __update_feature(self, feature: Feature, figure, x_correction, y_correction, feature_height):
        feature.set_coordinates(
            feature.coordinates[0] + x_correction,
            feature.coordinates[1] + y_correction,
            feature_height,
            )
        # todo расчет max_rad
        feature.perimeter_len = len(figure)

    def __calc_correction(self, figure):
        actual_center = self.feature_recognizer.get_center(figure)
        x_correct = int(actual_center[0] - self.x_hypothetical_center)
        y_correct = int(actual_center[1] - self.y_hypothetical_center)
        return x_correct, y_correct

    def __correct_delay(self, x: int, y: int):
        pass
