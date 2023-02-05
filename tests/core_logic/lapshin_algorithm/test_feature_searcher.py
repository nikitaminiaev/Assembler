import sys, os

root = sys.path[1]
path = os.path.join(root, "stub_microcontroller")
if path not in sys.path:
    sys.path.insert(0, path)
    sys.path.insert(0, os.path.abspath("../../../stub_microcontroller"))

from controller.core_logic.lapshin_algorithm.binding_probe_to_feature import BindingProbeToFeature
from controller.core_logic.lapshin_algorithm.service.recognition.lapshin_feature_recognizer import \
    LapshinFeatureRecognizer
from controller.core_logic.service.scanner import Scanner
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
        scanner = Scanner(get_val_func, set_x_func, set_y_func, touching_surface_event, external_surface, push_coord_to_mk, 0)

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
        surface = SurfaceGenerator(30, 20, [(14, 14)]).generate()
        self.feature_searcher.scanner.external_surface = surface
        self.feature_searcher.scanner.scan_algorithm = MagicMock()
        any_val = 1
        self.feature_searcher.scanner.get_val_func = MagicMock(
            side_effect=[14, 14, any_val, any_val, any_val,
                         any_val, any_val, any_val, any_val, 14, 14, any_val, any_val, any_val, any_val, any_val, any_val,
                         any_val, any_val, any_val, any_val, any_val, any_val, any_val, any_val, any_val, any_val, any_val, any_val,
                         ])

        self.binding_probe_to_feature.stop = True
        self.feature_searcher.find_first_feature(surface)
        self.assertEqual(self.binding_probe_to_feature.current_feature.coordinates, (14, 14, 24))
        self.assertEqual(self.binding_probe_to_feature.current_feature, self.feature_searcher.structure_of_feature.get_current_feature())

    def test_find_next_feature(self):
        vector_to_next_atom = np.array([12, 12], dtype='int8')
        self.binding_probe_to_feature.scanner.scan_algorithm = MagicMock()
        surface = SurfaceGenerator(30, 20, [(12, 12), (12 + vector_to_next_atom[0], 12 + vector_to_next_atom[1])]).generate()
        any_val = 1
        self.binding_probe_to_feature.scanner.get_val_func = MagicMock(
            side_effect=[12, 12, 3, 4, 5, 6, 7, 8, 9,
                         12, 12,any_val,any_val, any_val,any_val,any_val,
                         10, any_val,any_val,any_val, any_val,any_val,any_val,
                         10, any_val,any_val,any_val, any_val,any_val,any_val,
                         ])

        self.binding_probe_to_feature.stop = True
        self.feature_searcher.scanner.external_surface = surface
        self.feature_searcher.find_first_feature(surface)

        next_feature = self.feature_searcher.find_next_feature(surface, vector_to_next_atom)
        self.assertIsNotNone(next_feature)

        current_feature = self.feature_searcher.structure_of_feature.get_current_feature()
        self.assertTrue((np.append(vector_to_next_atom, [0]) == current_feature.vector_to_next).all())

    #
    # def test_search_features(self):
    #     self.fail()
    #

    # def test_bind_to_nearby_feature(self):
    #     self.fail()
