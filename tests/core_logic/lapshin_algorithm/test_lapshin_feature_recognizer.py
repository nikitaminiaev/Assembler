import sys, os
root = sys.path[1]
path = os.path.join(root, "stub_microcontroller")
if path not in sys.path:
    sys.path.insert(0, path)
    sys.path.insert(0, os.path.abspath("../../../stub_microcontroller"))

from controller.core_logic.lapshin_algorithm.service.recognition.lapshin_feature_recognizer import LapshinFeatureRecognizer
from stub_microcontroller.surface_generator import SurfaceGenerator
from unittest import TestCase
import numpy as np


class TestLapshinFeatureRecognizer(TestCase):

    def setUp(self) -> None:
        self.feature_recognizer = LapshinFeatureRecognizer()

    entry_vectors = [
        [7, 8],
        [1, 1],
        [7, 19],
        [200, 190],
    ]

    not_entry_vectors = [
        [2, 1],
        [20, 10],
        [200, 191],
    ]

    def test_is_vector_entry(self) -> None:
        points = np.array([[1, 1], [7, 8], [7, 9], [7, 19], [200, 190]], dtype='int8')

        for vector in self.entry_vectors:
            self.assertTrue(self.feature_recognizer._LapshinFeatureRecognizer__is_vector_entry(points, np.array(vector,
                                                                                                                dtype='int8')))

        for vector in self.not_entry_vectors:
            self.assertFalse(self.feature_recognizer._LapshinFeatureRecognizer__is_vector_entry(points, np.array(vector,
                                                                                                                 dtype='int8')))

    def test_calc_optimal_height(self) -> None:
        arr = SurfaceGenerator(20, 20, [(5, 5), (10, 5), (15, 5), (5, 10), (10, 10), (15, 10)]).generate_noise_surface()

        optimal_height = self.feature_recognizer.calc_optimal_height(arr)

        self.assertEqual(21, optimal_height)

    def test_bypass_bypass_feature(self) -> None:
        surface = SurfaceGenerator(20, 20, [(10, 10)]).generate()
        optimal_height = 21

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

        figure = self.feature_recognizer._LapshinFeatureRecognizer__bypass_feature((8, 9), optimal_height, surface)
        self.assertEqual(figure_probe.all(), figure.all())

    zero_points = [
        (10, 10),
        (10, 11),
        (11, 10),
        (11, 11),
    ]

    def test_reset_to_zero_feature_area(self) -> None:
        surface = SurfaceGenerator(20, 20, [(10, 10)]).generate()
        optimal_height = 21
        figure = self.feature_recognizer._LapshinFeatureRecognizer__bypass_feature((8, 9), optimal_height, surface)

        self.feature_recognizer._LapshinFeatureRecognizer__reset_to_zero_feature_area(figure, surface)
        for vector in figure:
            self.assertEqual(surface[vector[1], vector[0]], 0)

        for x, y in self.zero_points:
            self.assertEqual(surface[x, y], 0)

    def test_reset_to_zero_feature_another_area(self) -> None:
        surface = SurfaceGenerator(12, 20, [(7, 6)]).generate()
        optimal_height = 22
        figure = self.feature_recognizer._LapshinFeatureRecognizer__bypass_feature((8, 5), optimal_height, surface)

        self.feature_recognizer._LapshinFeatureRecognizer__reset_to_zero_feature_area(figure, surface)
        for vector in figure:
            self.assertEqual(surface[vector[1], vector[0]], 0)
            self.assertTrue(self.feature_recognizer.feature_in_aria((vector[0], vector[1]), figure))

    def test_reset_to_zero_feature_another_area2(self) -> None:
        surface = np.array([[20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], [20, 20, 20, 20, 21, 21, 21, 21, 21, 20, 20, 20, 20], [20, 20, 20, 21, 21, 22, 22, 22, 21, 21, 20, 20, 20], [20, 20, 20, 21, 22, 23, 23, 23, 22, 21, 20, 20, 20], [20, 20, 20, 21, 22, 23, 24, 23, 22, 21, 20, 20, 20], [20, 20, 20, 21, 22, 23, 23, 23, 22, 21, 20, 20, 20], [20, 20, 20, 21, 21, 22, 22, 22, 21, 21, 20, 20, 20], [20, 20, 20, 20, 21, 21, 21, 21, 21, 20, 20, 20, 20], [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20], [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]])
        figure = np.array([[6, 5], [7, 5], [8, 6], [8, 7], [8, 8], [7, 9], [6, 9], [5, 9], [4, 8], [4, 7], [4, 6], [5, 5]])

        self.feature_recognizer._LapshinFeatureRecognizer__reset_to_zero_feature_area(figure, surface)
        for vector in figure:
            self.assertEqual(surface[vector[1], vector[0]], 0)
            self.assertTrue(self.feature_recognizer.feature_in_aria((vector[0], vector[1]), figure))

    def test_centroid(self) -> None:
        atom_cord = (8, 9)
        surface = SurfaceGenerator(20, 20, [atom_cord]).generate()
        optimal_height = 21

        figure = self.feature_recognizer._LapshinFeatureRecognizer__bypass_feature((10, 9), optimal_height, surface)
        centr = self.feature_recognizer.get_center(figure)

        self.assertEqual(centr, atom_cord)

    def test_feature_recognition(self) -> None:
        atom_cord = (8, 9)
        surface = SurfaceGenerator(20, 20, [atom_cord]).generate()
        optimal_height = 21

        figure1 = self.feature_recognizer._LapshinFeatureRecognizer__bypass_feature((10, 9), optimal_height, surface)
        figure2 = self.feature_recognizer.recognize_figure((6, 9), surface, optimal_height)
        self.assertEqual(figure1.all(), figure2.all())

        centr1 = self.feature_recognizer.get_center(figure1)
        centr2 = self.feature_recognizer.get_center(figure2)

        self.assertEqual(centr1, atom_cord)
        self.assertEqual(centr2, atom_cord)

    points_in_aria = [
        (9, 9),
        (10, 9),
        (11, 9),
        (10, 10),
        (10, 11),
        (11, 10),
        (11, 11),
        (8, 9),
        (11, 12),
    ]
    points_not_in_aria = [
        (2, 1),
        (20, 10),
        (200, 191),
        (6, 8),
        (8, 8),
        (12, 12),
    ]

    def test_feature_in_aria(self) -> None:
        surface = SurfaceGenerator(20, 20, [(10, 10)]).generate()
        optimal_height = 21

        figure = self.feature_recognizer._LapshinFeatureRecognizer__bypass_feature((8, 9), optimal_height, surface)

        for point in self.points_in_aria:
            self.assertTrue(self.feature_recognizer.feature_in_aria(point, figure))

        for point in self.points_not_in_aria:
            self.assertFalse(self.feature_recognizer.feature_in_aria(point, figure))
