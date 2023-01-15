import sys, os

root = sys.path[1]
path = os.path.join(root, "stub_microcontroller")
if path not in sys.path:
    sys.path.insert(0, path)
    sys.path.insert(0, os.path.abspath("../../../stub_microcontroller"))

from controller.core_logic.lapshin_algorithm.binding_probe_to_feature import BindingProbeToFeature
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

        self.binding_probe_to_feature.stop = True
        self.feature_searcher.find_first_feature(surface)
        self.assertEqual(self.binding_probe_to_feature.current_feature.coordinates, (10, 10, 24))
        self.assertEqual(self.binding_probe_to_feature.current_feature, self.feature_searcher.structure_of_feature.get_current_feature())

    def test_find_next_feature(self):
        vector_to_next_atom = np.array([6, 6, 24], dtype='int8')
        surface = SurfaceGenerator(30, 20, [(6, 6), (6 + vector_to_next_atom[0], 6 + vector_to_next_atom[1])]).generate()
        any_val = 1
        self.binding_probe_to_feature.scanner.get_val_func = MagicMock(
            side_effect=[9, 9, 27, any_val, any_val, any_val, any_val, any_val, any_val, any_val, any_val, any_val,
                         any_val])

        self.binding_probe_to_feature.stop = True
        self.feature_searcher.find_first_feature(surface)

        surface = SurfaceGenerator(30, 20, [(15, 15), (15 + vector_to_next_atom[0], 15 + vector_to_next_atom[1])]).generate()

        next_feature = self.feature_searcher.find_next_feature(surface)
        self.assertIsNotNone(next_feature)

        current_feature = self.feature_searcher.structure_of_feature.get_current_feature()
        self.assertTrue((vector_to_next_atom == current_feature.vector_to_next).all())

    #
    # def test_search_features(self):
    #     self.fail()
    #

    # def test_bind_to_nearby_feature(self):
    #     self.fail()
