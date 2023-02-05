import numpy as np


class VectorOperations:

    @staticmethod
    def calc_vectors_to_neighbors(current_center: tuple, neighbors_center: list) -> np.ndarray:
        vectors = np.array([[0, 0]])
        for center in neighbors_center:
            vectors = np.append(vectors, [
                [
                    center[0] - current_center[0],
                    center[1] - current_center[1]
                ]
            ], axis=0)
        return np.delete(vectors, 0, 0)

    @staticmethod
    def calc_vectors_cos_angle(v1: np.ndarray, v2: np.ndarray) -> float:
        dot_pr = v1.dot(v2)
        norms = np.linalg.norm(v1) * np.linalg.norm(v2)

        return dot_pr / norms

    @staticmethod
    def get_reverse_vector(v: np.ndarray) -> np.ndarray:
        return np.array([-v[0], -v[1], v[2]])

    @staticmethod
    def get_vector_between_to_point(destination_point: tuple, start_point: tuple) -> np.ndarray:
        if len(destination_point) == 2 and len(start_point) == 2:
            return np.array(
                [
                    destination_point[0] - start_point[0],
                    destination_point[1] - start_point[1],
                ]
            )
        if len(destination_point) == 3 and len(start_point) == 3:
            return np.array(
                [
                    destination_point[0] - start_point[0],
                    destination_point[1] - start_point[1],
                    destination_point[2] - start_point[2],
                ]
            )
        raise ValueError('vector_between_to_point exception')

    @staticmethod
    def get_vector_len(vector: np.ndarray) -> float:
        return np.linalg.norm(vector)
