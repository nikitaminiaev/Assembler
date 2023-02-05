import threading
from threading import Event
from typing import Tuple

import numpy as np
from controller.core_logic.lapshin_algorithm.binding_probe_to_feature_interface import BindingProbeToFeatureInterface
from controller.core_logic.lapshin_algorithm.entity.feature import Feature
from controller.core_logic.lapshin_algorithm.exception.neighbors_not_found_exception import NeighborsNotFoundException
from controller.core_logic.lapshin_algorithm.exception.next_feature_not_found_exception import \
    NextFeatureNotFoundException
from controller.core_logic.lapshin_algorithm.feature_collection.direction_generator_interface import \
    DirectionGeneratorInterface
from controller.core_logic.lapshin_algorithm.feature_collection.doubly_linked_list import DoublyLinkedList
from controller.core_logic.lapshin_algorithm.feature_searcher_interface import FeatureSearcherInterface
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


class FeatureSearcher(FeatureSearcherInterface):
    COS_QUARTER_PI = 0.7071

    def __init__(self,
                 binding_to_feature: BindingProbeToFeatureInterface,
                 scanner: ScannerInterface,
                 feature_recognizer: FeatureRecognizerInterface,
                 binding_in_delay: Event,
                 allow_binding: Event
                 ):
        self.scanner = scanner
        self.binding_to_feature = binding_to_feature
        self.feature_recognizer = feature_recognizer
        self.structure_of_feature = DoublyLinkedList()
        self.binding_in_delay = binding_in_delay
        self.allow_binding = allow_binding
        self.scanner_around_feature = ScannerAroundFeature(scanner)

    def search_features_auto(self, surface: np.ndarray, direction_generator: DirectionGeneratorInterface, max_feature_count: int) -> None:
        # todo вычислять и логировать время выполнения функций
        self.find_first_feature(surface)
        while self.structure_of_feature.count < max_feature_count:
            current_feature = self.structure_of_feature.get_current_feature()
            next_feature = self.recur_find_next_feature(current_feature, direction_generator.generate_next_direction(self.structure_of_feature.count), 5) #todo обработать NextFeatureNotFoundException, current_feature получать внутри, параметр - next_direction
            self.average_vector_between_features(current_feature, next_feature)
            self.join_next_feature(next_feature, current_feature.vector_to_next)
            # todo логирвоание print(next_feature.to_string())

    def join_next_feature(self, next_feature: Feature, vector_to_next_feature: np.ndarray) -> None:
        self.scanner.go_to_direction(vector_to_next_feature)
        self.structure_of_feature.insert_to_end(next_feature)
        self.binding_to_feature.set_current_feature(next_feature)
        self.allow_binding.set()

    def average_vector_between_features(self, current_feature: Feature, next_feature: Feature) -> None:
        self.binding_in_delay.wait()
        self.allow_binding.clear()
        self.binding_to_feature.jumping(current_feature, next_feature, 5)  # todo обработать LossCurrentFeatureException

    def recur_find_next_feature(self, current_feature: Feature, next_direction: np.ndarray, count_feature_rad: int) -> Feature:
        if count_feature_rad > 7:
            raise NextFeatureNotFoundException
        self.binding_in_delay.wait()
        self.allow_binding.clear()
        surface = self.scanner_around_feature.scan_aria_around_current_position(current_feature.max_rad * count_feature_rad)
        self.allow_binding.set()
        try:
            next_feature = self.find_next_feature(surface, next_direction)
        except RuntimeError:
            self.allow_binding.set()
            self.binding_in_delay.wait()
            self.allow_binding.clear()
            next_feature = self.recur_find_next_feature(current_feature, next_direction, count_feature_rad + 2)
        return next_feature

    def display(self) -> list or None:
        return self.structure_of_feature.get_all_features()

    def pause_algorithm(self) -> None:
        self.allow_binding.clear()

    def reset_structure(self) -> None:
        self.structure_of_feature = DoublyLinkedList()

    def find_first_feature(self, surface: np.ndarray) -> Feature:
        feature = self.__get_first_feature(surface)
        current_position = self.scanner.get_current_position()
        vector = VectorOperations.get_vector_between_to_point(feature.coordinates, current_position)
        self.scanner.go_to_direction(vector)
        self.go_to_feature_more_accurate(feature, 5)

        self.structure_of_feature.insert_to_end(feature)
        self.binding_to_feature.set_current_feature(feature)
        self.allow_binding.set()
        threading.Thread(target=self.__start_binding_thread, args=(self.binding_to_feature,)).start()
        return feature

    def go_to_feature_more_accurate(self, feature: Feature, rad_count: int):
        surface_for_accurate = self.scanner_around_feature.scan_aria_around_current_position(feature.max_rad * rad_count)
        # todo логирование print('=========_surface===========')
        try:
            actual, _ = self.__get_figures_center(surface_for_accurate.copy())
        except ValueError as e:
            print(surface_for_accurate)
            raise e
        actual_center = list(actual.keys())[0]
        aria_center = self.scanner_around_feature.get_scan_aria_center(surface_for_accurate)
        vector_to_center = VectorOperations.get_vector_between_to_point(actual_center, aria_center)
        z_current = self.scanner.get_current_position()[2]
        vector_to_center = np.append(vector_to_center, feature.max_height - z_current)
        self.scanner.go_to_direction(vector_to_center)
        # todo логирование print('=========vector_to_center===========')

    def __get_first_feature(self, surface):
        figure_gen = self.feature_recognizer.recognize_all_figure_in_aria(surface.copy())
        first_figure = next(figure_gen)
        feature = self.feature_recognizer.recognize_feature(first_figure, surface)
        return feature

    def find_next_feature(self, surface: np.ndarray, next_direction: np.ndarray) -> Feature:  # TODO сделать рефакторинг функции, выделить приватный метод
        try:
            current, neighbors = self.__get_figures_center(surface.copy())
        except ValueError as e:
            print(surface)
            raise e
        print(neighbors)
        if len(neighbors) == 0:
            raise NeighborsNotFoundException
        current_center = list(current.keys())[0]
        neighbors_center = list(neighbors.keys())
        vectors_to_neighbors = VectorOperations.calc_vectors_to_neighbors(current_center, neighbors_center)
        print(next_direction)
        vector_to_next_feature = self.__find_close_vector(vectors_to_neighbors, next_direction)
        if vector_to_next_feature is None:
            raise NextFeatureNotFoundException
        try:
            next_feature = self.feature_recognizer.recognize_feature(
                neighbors[(current_center[0] + vector_to_next_feature[0], current_center[1] + vector_to_next_feature[1])],
                surface
            )
        except ValueError:
            raise NextFeatureNotFoundException
        current_feature = self.structure_of_feature.get_current_feature()
        vector_to_next_feature = np.append(vector_to_next_feature, next_feature.max_height - current_feature.max_height)
        next_feature.vector_to_prev = VectorOperations.get_reverse_vector(vector_to_next_feature)
        if current_feature is not None:
            current_feature: Feature
            current_feature.vector_to_next = vector_to_next_feature
        return next_feature

    def bind_to_nearby_feature(self) -> None:  # todo в случае LossCurrentFeatureException
        pass
        # получить координаты из self.get_val_func
        # делать сканы по кругу и в каждом искать фичу

    """
    :return current: dict{figure_center:tuple : figure:np.ndarray}
    :return neighbors: dict{figure_center:tuple : figure:np.ndarray}
    :raise ValueError
    """
    def __get_figures_center(self, surface) -> Tuple[dict, dict]:
        figure_gen = self.feature_recognizer.recognize_all_figure_in_aria(surface.copy())
        neighbors = {}
        aria_center = self.scanner_around_feature.get_scan_aria_center(surface)
        vectors_len = {}
        for figure in figure_gen:
            figure_center = self.feature_recognizer.get_center(figure)
            vector_to_center = VectorOperations.get_vector_between_to_point(figure_center, aria_center)
            vectors_len[VectorOperations.get_vector_len(vector_to_center)] = figure_center
            neighbors[figure_center] = figure
        if len(vectors_len) == 0:
            # todo логирвоание surface
            raise RuntimeError('figure not found')
        min_vector = min(vectors_len.keys())
        current = {vectors_len[min_vector]: neighbors[vectors_len[min_vector]]}
        del neighbors[list(current.keys())[0]]
        if current is None:
            raise RuntimeError('current not found')
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
            print(angle)
            if angle < self.COS_QUARTER_PI:  # todo константу в параметр, функцию в VectorOperations
                continue
            if optimal_angle is None:
                optimal_angle = angle
                result = vector
                continue
            if angle > optimal_angle:
                optimal_angle = angle
                result = vector
        return result

    def __start_binding_thread(self, binding_to_feature: BindingProbeToFeatureInterface):
        binding_to_feature.bind_to_current_feature()
