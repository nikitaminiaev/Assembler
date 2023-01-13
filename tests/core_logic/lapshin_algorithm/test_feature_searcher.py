import sys, os

root = sys.path[1]
path = os.path.join(root, "stub_microcontroller")
if path not in sys.path:
    sys.path.insert(0, path)
    sys.path.insert(0, os.path.abspath("../../../stub_microcontroller"))

from controller.core_logic.lapshin_algorithm.binding_probe_to_feature import BindingProbeToFeature
from controller.core_logic.lapshin_algorithm.entity.atom import Atom
from controller.core_logic.lapshin_algorithm.service.recognition.lapshin_feature_recognizer import \
    LapshinFeatureRecognizer
from controller.core_logic.service.feature_scanner import FeatureScanner
from stub_microcontroller.surface_generator import SurfaceGenerator
from unittest import TestCase
from unittest.mock import MagicMock
from controller.core_logic.lapshin_algorithm.feature_searcher import FeatureSearcher
import numpy as np


class TestFeatureSearcher(TestCase):
    def setUp(self) -> None:
        get_val_func = MagicMock()
        set_x_func = MagicMock()
        set_y_func = MagicMock()
        touching_surface_event = MagicMock()
        external_surface = MagicMock()
        push_coord_to_mk = MagicMock()
        binding_in_delay = MagicMock()
        allow_binding = MagicMock()
        scanner = FeatureScanner(get_val_func, set_x_func, set_y_func, touching_surface_event, external_surface, push_coord_to_mk, 0)

        self.binding_probe_to_feature = BindingProbeToFeature(
            LapshinFeatureRecognizer(),
            scanner,
            binding_in_delay,
            allow_binding
        )

        self.feature_searcher = FeatureSearcher(
            self.binding_probe_to_feature,
            scanner,
            LapshinFeatureRecognizer(),
            binding_in_delay,
            allow_binding,
        )

    def test_find_close_vector(self):
        next_direction = np.array([5, 5], dtype='int8')
        vectors_to_neighbors = np.array([
                [10, 11],
                [10, 12],
                [-5, -5],
                [0, 10],
                [10, 0],
                [-5, 10],
            ],
            dtype='int8')

        vector = self.feature_searcher._FeatureSearcher__find_close_vector(vectors_to_neighbors, next_direction)
        self.assertEqual([10, 11], list(vector))

    def test_find_first_feature(self):
        surface = SurfaceGenerator(20, 20, [(10, 10)]).generate()
        self.binding_probe_to_feature.scanner.external_surface = surface
        any_val = 1
        self.binding_probe_to_feature.scanner.get_val_func = MagicMock(
            side_effect=[9, 9, 27, any_val, any_val, any_val, any_val, any_val, any_val, any_val, any_val, any_val,
                         any_val])
        feature = Atom((9, 9, 24))
        feature.max_rad = 2
        self.assertEqual(0, feature.perimeter_len)

        figure_gen = self.feature_searcher.feature_recognizer.recognize_all_figure_in_aria(surface.copy())
        first_figure = next(figure_gen)
        self.binding_probe_to_feature.stop = True
        self.feature_searcher.find_first_feature(first_figure, surface)



    # def test_search_features(self):
    #     self.fail()
    #
    #
    # def test_find_next_feature(self):
    #     self.fail()
    #
    # def test_bind_to_nearby_feature(self):
    #     self.fail()
