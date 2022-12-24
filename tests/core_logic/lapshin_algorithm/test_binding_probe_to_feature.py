import sys, os

from controller.core_logic.entity.atom import Atom

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

    zero_points = [
        (10, 10),
        (10, 11),
        (11, 10),
        (11, 11),
    ]

    def test_reset_to_zero_feature_area(self) -> None:
        self.BindingProbeToFeature.local_surface = SurfaceGenerator(20, 20, [(10, 10)]).generate()
        self.BindingProbeToFeature.z_optimal_height = 21
        figure = self.BindingProbeToFeature.bypass_feature((7, 9))

        self.BindingProbeToFeature.reset_to_zero_feature_area(figure)
        for vector in figure:
            self.assertEqual(self.BindingProbeToFeature.local_surface[vector[1], vector[0]], 0)

        for x, y in self.zero_points:
            self.assertEqual(self.BindingProbeToFeature.local_surface[x, y], 0)

    def test_reset_to_zero_feature_another_area(self) -> None:
        self.BindingProbeToFeature.local_surface = SurfaceGenerator(12, 20, [(7, 6)]).generate()
        self.BindingProbeToFeature.z_optimal_height = 22
        figure = self.BindingProbeToFeature.bypass_feature((7, 4))

        self.BindingProbeToFeature.reset_to_zero_feature_area(figure)
        for vector in figure:
            self.assertEqual(self.BindingProbeToFeature.local_surface[vector[1], vector[0]], 0)
            self.assertTrue(self.BindingProbeToFeature.feature_in_aria((vector[0], vector[1]), figure))

    def test_reset_to_zero_feature_another_area2(self) -> None:
        self.BindingProbeToFeature.local_surface = np.array([[20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], [20, 20, 20, 20, 21, 21, 21, 21, 21, 20, 20, 20, 20], [20, 20, 20, 21, 21, 22, 22, 22, 21, 21, 20, 20, 20], [20, 20, 20, 21, 22, 23, 23, 23, 22, 21, 20, 20, 20], [20, 20, 20, 21, 22, 23, 24, 23, 22, 21, 20, 20, 20], [20, 20, 20, 21, 22, 23, 23, 23, 22, 21, 20, 20, 20], [20, 20, 20, 21, 21, 22, 22, 22, 21, 21, 20, 20, 20], [20, 20, 20, 20, 21, 21, 21, 21, 21, 20, 20, 20, 20], [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]])
        figure = np.array([[6, 5], [7, 5], [8, 6], [8, 7], [8, 8], [7, 9], [6, 9], [5, 9], [4, 8], [4, 7], [4, 6], [5, 5]])

        self.BindingProbeToFeature.reset_to_zero_feature_area(figure)
        for vector in figure:
            self.assertEqual(self.BindingProbeToFeature.local_surface[vector[1], vector[0]], 0)
            self.assertTrue(self.BindingProbeToFeature.feature_in_aria((vector[0], vector[1]), figure))

    def test_centroid(self) -> None:
        atom_cord = (8, 9)
        self.BindingProbeToFeature.local_surface = SurfaceGenerator(20, 20, [atom_cord]).generate()
        self.BindingProbeToFeature.z_optimal_height = 21

        figure = self.BindingProbeToFeature.bypass_feature((5, 8))
        centr = self.BindingProbeToFeature.centroid(figure)

        self.assertEqual(centr, atom_cord)

    def test_feature_recognition(self) -> None:
        atom_cord = (8, 9)
        self.BindingProbeToFeature.local_surface = SurfaceGenerator(20, 20, [atom_cord]).generate()
        self.BindingProbeToFeature.z_optimal_height = 21

        figure1 = self.BindingProbeToFeature.bypass_feature((5, 8))
        figure2 = self.BindingProbeToFeature.feature_recognition((5, 8))
        self.assertEqual(figure1.all(), figure2.all())

        centr1 = self.BindingProbeToFeature.centroid(figure1)
        centr2 = self.BindingProbeToFeature.centroid(figure2)

        self.assertEqual(centr1, atom_cord)
        self.assertEqual(centr2, atom_cord)

    points_in_aria = [
        (9, 9),
        (7, 9),
        (9, 9),
        (10, 10),
        (10, 11),
        (11, 10),
        (11, 11),
    ]
    points_not_in_aria = [
        (2, 1),
        (20, 10),
        (200, 191),
        (6, 8),
    ]

    def test_feature_in_aria(self) -> None:
        self.BindingProbeToFeature.local_surface = SurfaceGenerator(20, 20, [(10, 10)]).generate()
        self.BindingProbeToFeature.z_optimal_height = 21

        figure = self.BindingProbeToFeature.bypass_feature((7, 9))

        for point in self.points_in_aria:
            self.assertTrue(self.BindingProbeToFeature.feature_in_aria(point, figure))

        for point in self.points_not_in_aria:
            self.assertFalse(self.BindingProbeToFeature.feature_in_aria(point, figure))

    def test_bind_to_feature(self) -> None:
        self.BindingProbeToFeature.global_surface = SurfaceGenerator(20, 20, [(10, 10)]).generate()
        feature = Atom((9, 9, 20), 3)

        self.BindingProbeToFeature.bind_to_feature(feature)

        print(self.BindingProbeToFeature.x_correction)
        print(self.BindingProbeToFeature.y_correction)