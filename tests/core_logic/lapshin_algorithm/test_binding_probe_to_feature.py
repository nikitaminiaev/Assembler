import sys, os

path = os.path.abspath("../../../stub_microcontroller")
print(path)
if path not in sys.path:
    sys.path.insert(0, path)

import numpy as np
from unittest import TestCase
from unittest.mock import MagicMock, call
from controller.core_logic.lapshin_algorithm.binding_probe_to_feature import BindingProbeToFeature
from stub_microcontroller.surface_generator import SurfaceGenerator


class TestBindingProbeToFeature(TestCase):

    def setUp(self) -> None:
        get_val_func = MagicMock()
        set_x_func = MagicMock()
        set_y_func = MagicMock()
        touching_surface_event = MagicMock()
        global_surface = MagicMock()

        self.BindingProbeToFeature = BindingProbeToFeature(
            get_val_func,
            set_x_func,
            set_y_func,
            touching_surface_event,
            global_surface
        )

    def test_calc_optimal_height(self) -> None:
        arr = SurfaceGenerator(20, 20, [(5, 5), (10, 5), (15, 5), (5, 10), (10, 10), (15, 10)]).generate_noise_surface()

        self.BindingProbeToFeature.calc_optimal_height(arr)

        self.assertEqual(21, self.BindingProbeToFeature.z_optimal_height)

    def test_is_vector_entry(self) -> None:
        points = np.array([[1, 1], [7, 8], [7, 9], [7, 19], [200, 190]], dtype='int8')

        self.assertTrue(self.BindingProbeToFeature.is_vector_entry(points, np.array([7, 8], dtype='int8')))
        self.assertTrue(self.BindingProbeToFeature.is_vector_entry(points, np.array([1, 1], dtype='int8')))
        self.assertTrue(self.BindingProbeToFeature.is_vector_entry(points, np.array([7, 19], dtype='int8')))
        self.assertTrue(self.BindingProbeToFeature.is_vector_entry(points, np.array([200, 190], dtype='int8')))

        self.assertFalse(self.BindingProbeToFeature.is_vector_entry(points, np.array([2, 1], dtype='int8')))
        self.assertFalse(self.BindingProbeToFeature.is_vector_entry(points, np.array([20, 10], dtype='int8')))
        self.assertFalse(self.BindingProbeToFeature.is_vector_entry(points, np.array([200, 191], dtype='int8')))

    def test_bypass_bypass_feature(self) -> None:
        self.BindingProbeToFeature.local_surface = SurfaceGenerator(20, 20, [(10, 10)]).generate()
        self.BindingProbeToFeature.z_optimal_height = 21

        figure_probe = np.array([[7, 8],
                                 [8, 7],
                                 [9, 7],
                                 [10, 7],
                                 [11, 7],
                                 [12, 7],
                                 [13, 8],
                                 [13, 9],
                                 [13, 10],
                                 [13, 11],
                                 [13, 12],
                                 [12, 13],
                                 [11, 13],
                                 [10, 13],
                                 [9, 13],
                                 [8, 13],
                                 [7, 12],
                                 [7, 11],
                                 [7, 10],
                                 [7, 9]], dtype='int8')

        figure = self.BindingProbeToFeature.bypass_feature((7, 9))
        self.assertEqual(figure_probe.all(), figure.all())

    def test_reset_to_zero_feature_area(self) -> None:
        self.BindingProbeToFeature.local_surface = SurfaceGenerator(20, 20, [(10, 10)]).generate()
        self.BindingProbeToFeature.z_optimal_height = 21
        figure = self.BindingProbeToFeature.bypass_feature((7, 9))

        self.BindingProbeToFeature.reset_to_zero_feature_area(figure)
        for vector in figure:
            self.assertEqual(self.BindingProbeToFeature.local_surface[vector[1], vector[0]], 0)

        self.assertEqual(self.BindingProbeToFeature.local_surface[10, 10], 0)
        self.assertEqual(self.BindingProbeToFeature.local_surface[10, 11], 0)
        self.assertEqual(self.BindingProbeToFeature.local_surface[11, 10], 0)
        self.assertEqual(self.BindingProbeToFeature.local_surface[11, 11], 0)

    def test_centroid(self) -> None:
        self.BindingProbeToFeature.local_surface = SurfaceGenerator(20, 20, [(8, 9)]).generate()
        self.BindingProbeToFeature.z_optimal_height = 21
        figure = self.BindingProbeToFeature.bypass_feature((5, 8))

        centr = self.BindingProbeToFeature.centroid(figure)

        print(centr)
        print(self.BindingProbeToFeature.local_surface)
