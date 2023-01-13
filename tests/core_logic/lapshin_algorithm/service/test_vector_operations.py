import sys, os


root = sys.path[1]
path = os.path.join(root, "stub_microcontroller")
if path not in sys.path:
    sys.path.insert(0, path)
    sys.path.insert(0, os.path.abspath("../../../stub_microcontroller"))

from unittest import TestCase
from controller.core_logic.lapshin_algorithm.service.vector_operations import VectorOperations
import numpy as np


class TestVectorOperations(TestCase):
    def test_calc_vectors_to_neighbors(self):
        current_center = (5, 5)
        neighbors_center = [(10, 10), (15, 15), (-10, -10), (-15, -15)]
        vectors = VectorOperations.calc_vectors_to_neighbors(current_center, neighbors_center)
        for key, vector in enumerate(vectors):
            self.assertEqual(vector[0], neighbors_center[key][0] - current_center[0])
            self.assertEqual(vector[1], neighbors_center[key][1] - current_center[1])

    vectors_data = [
        (0, np.array([5, 5], dtype='int8'), np.array([10, 10], dtype='int8')),
        (90, np.array([-5, 5], dtype='int8'), np.array([10, 10], dtype='int8')),
        (135, np.array([-5, 0], dtype='int8'), np.array([10, 10], dtype='int8')),
        (180, np.array([-5, -5], dtype='int8'), np.array([5, 5], dtype='int8')),
        (45, np.array([5, 5], dtype='int8'), np.array([10, 0], dtype='int8')),
        (45, np.array([5, 5], dtype='int8'), np.array([0, 10], dtype='int8')),
        (72, np.array([5, 5], dtype='int8'), np.array([-5, 10], dtype='int8')),
    ]

    def test_calc_vectors_cos_angle(self):
        for vectors in self.vectors_data:
            self.assertEqual(
                vectors[0],
                round(np.rad2deg(np.arccos(VectorOperations.calc_vectors_cos_angle(vectors[1], vectors[2]))))
            )
