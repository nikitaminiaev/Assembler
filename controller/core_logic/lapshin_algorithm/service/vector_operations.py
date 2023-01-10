import numpy as np


class VectorOperations:

    @staticmethod
    def calc_vectors_to_neighbors(current_center: tuple, neighbors_center: list) -> np.ndarray:
        vectors = np.array([[0, 0]], dtype='int8')
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
