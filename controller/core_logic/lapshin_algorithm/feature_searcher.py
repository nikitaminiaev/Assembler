import threading
from threading import Event
from typing import Tuple

import numpy as np
from controller.core_logic.lapshin_algorithm.binding_probe_to_feature_interface import BindingProbeToFeatureInterface
from controller.core_logic.lapshin_algorithm.entity.feature import Feature
from controller.core_logic.lapshin_algorithm.feature_collection.doubly_linked_list import DoublyLinkedList
from controller.core_logic.lapshin_algorithm.service.recognition.feature_recognizer_interface import \
    FeatureRecognizerInterface
from controller.core_logic.lapshin_algorithm.service.scanner_around_feature import ScannerAroundFeature
from controller.core_logic.lapshin_algorithm.service.vector_operations import VectorOperations
from controller.core_logic.service.scanner_interface import ScannerInterface

"""
при создании затравки производится поиск такого атома, который расположен под
наименьшим углом к прямой, задающей направление движения. Найденный атом полу-
чает ярлык “следующий”. Причём, при перемещении вдоль кристаллографического на-
правления положение следующего атома цепочки используется для уточнения направле-
ния движения, если изменение локальной кривизны цепочки лежит в заданных пределах.
Таким образом, указанный приём позволяет удерживать выбранное направление, легко
минуя те места на поверхности кристалла, где расположены точечные дефекты решётки.
"""

"""
В случае, когда выполняется обход затравки с присоединением (см. Рис. 5 и Рис. 8),
вначале выполняется сортировка: среди атомов выбираются те, что не принадлежат к
уже пройденной цепочке. После чего среди отобранных ищется тот, что расположен под
наибольшим (наименьшим) углом (отсчёт угла в обоих случаях производится вокруг “те-
кущего” атома в направлении против часовой стрелки) к отрезку, соединяющему “теку-
щий” и “предыдущий” атомы при обходе контура цепочки против часовой стрелки (по ча-
совой стрелке). Найденный таким образом атом принимается за “следующий” атом це-
почки.
"""

"""
Надо искать следующий атом цепочки по предположительному направлению движения. Найдя распознать его определить, 
привязаться, определить относительные координаты к предыдущему и перепрыгивать между ними для усреднения.  
"""


class FeatureSearcher:

    COS_QUARTER_PI = 0.7071

    def __init__(self,
                 binding_to_feature: BindingProbeToFeatureInterface,
                 scanner: ScannerInterface,
                 feature_recognizer: FeatureRecognizerInterface,
                 binding_in_delay: Event,
                 allow_binding: Event
                 ):
        self.scanner = scanner
        self.local_surface = None
        self.binding_to_feature = binding_to_feature
        self.feature_recognizer = feature_recognizer
        self.structure_of_feature = DoublyLinkedList()
        self.binding_in_delay = binding_in_delay
        self.allow_binding = allow_binding
        self.scanner_around_feature = ScannerAroundFeature(scanner)

    def search_features(self):
        surface = self.scanner.scan_aria() #todo избавиться от это-го (уйдет выше или другой метод)
        self.find_first_feature(surface.copy())

        while self.structure_of_feature.count < 4:
            self.binding_in_delay.wait()
            self.allow_binding.clear()
            surface = self.scanner_around_feature.scan_aria_around_feature(self.structure_of_feature.get_current_feature(), 5) #todo выделить в рекурсивную функцию
            self.allow_binding.set()
            try:
                next_feature = self.find_next_feature(surface)
            except RuntimeError:
                self.binding_in_delay.wait()
                self.allow_binding.clear()
                surface = self.scanner_around_feature.scan_aria_around_feature(self.structure_of_feature.get_current_feature(), 7)
                self.allow_binding.set()
                next_feature = self.find_next_feature(surface)

            current_feature = self.structure_of_feature.get_current_feature()
            self.binding_to_feature.jumping(current_feature, next_feature, 5)

            self.structure_of_feature.insert_to_end(next_feature)
            self.binding_to_feature.set_current_feature(next_feature)
            self.allow_binding.set()

    def find_first_feature(self, surface: np.ndarray):
        figure_gen = self.feature_recognizer.recognize_all_figure_in_aria(surface.copy())
        first_figure = next(figure_gen)
        feature = self.feature_recognizer.recognize_feature(first_figure, surface)
        self.structure_of_feature.insert_to_end(feature)
        self.scanner.go_to_coordinate(*feature.coordinates)
        self.binding_to_feature.set_current_feature(feature)
        self.allow_binding.set()
        threading.Thread(target=self.binding_to_feature.bind_to_current_feature).start()

    def find_next_feature(self, surface: np.ndarray) -> Feature: #TODO сделать рефакторинг функции, выделить приватный метод
        current, neighbors = self.__get_figures_center(surface)
        current_center = list(current.keys())[0]
        neighbors_center = list(neighbors.keys())
        vectors_to_neighbors = VectorOperations.calc_vectors_to_neighbors(current_center, neighbors_center)
        next_direction = self.structure_of_feature.get_next_direction()
        vector_to_next_feature = self.__find_close_vector(vectors_to_neighbors, next_direction)
        if vector_to_next_feature is None:
            raise RuntimeError('next feature not found')

        next_feature = self.feature_recognizer.recognize_feature(
            neighbors[(current_center[0] + vector_to_next_feature[0], current_center[1] + vector_to_next_feature[1])],
            surface
        )
        vector_to_next_feature = np.append(vector_to_next_feature, next_feature.max_height)
        next_feature.vector_to_prev = VectorOperations.get_reverse_vector(vector_to_next_feature)
        current_feature = self.structure_of_feature.get_current_feature()
        if current_feature is not None:
            current_feature: Feature
            current_feature.vector_to_next = vector_to_next_feature

        return next_feature

    def bind_to_nearby_feature(self) -> None:  # в случае ошибки при сильном смещении
        pass
        # получить координаты из self.get_val_func
        # делать сканы по кругу и в каждом искать фичу

    def __get_figures_center(self, surface) -> Tuple[dict, dict]:
        figure_gen = self.feature_recognizer.recognize_all_figure_in_aria(surface.copy())
        neighbors = {}
        current = None
        for figure in figure_gen:
            center = self.scanner.get_scan_aria_center(surface)
            if self.feature_recognizer.feature_in_aria(tuple(int(item) for item in center), figure):  # todo вычислять все ценрры и потом current_center тот который ближе всех к центра скана
                current = {self.feature_recognizer.get_center(figure): figure}
                continue
            neighbors[self.feature_recognizer.get_center(figure)] = figure
        if current is None:
            raise RuntimeError('current not found')
        if len(neighbors) == 0:
            raise RuntimeError('neighbors not found')
        return current, neighbors

    def __find_close_vector(self, vectors_to_neighbors: np.ndarray, next_direction: np.ndarray) -> np.ndarray or None:
        """
        диапазон допустимых углов углов
            cos(0) - cos(pi/4)
            cos(7pi/4) - cos(2pi)
        """
        optimal_angle = None
        result = None
        for vector in vectors_to_neighbors:
            angle = VectorOperations.calc_vectors_cos_angle(next_direction, vector)
            if angle < self.COS_QUARTER_PI:   #todo константу в параметр, функцию в VectorOperations
                continue
            if optimal_angle is None:
                optimal_angle = angle
                result = vector
                continue
            if angle > optimal_angle:
                optimal_angle = angle
                result = vector
        return result


