from controller.core_logic.lapshin_algorithm.entity.feature import Feature
from controller.core_logic.lapshin_algorithm.feature_collection.direction_generator_snake import DirectionGeneratorSnake
import numpy as np


class Node:
    def __init__(self, feature: Feature):
        self.item = feature
        self.next = None
        self.prev = None


class DoublyLinkedList:
    def __init__(self):
        self.current_node = None
        self.start_node = None
        self.count = 0

    def insert_to_end(self, feature: Feature):
        if self.list_is_empty():
            new_node = Node(feature)
            self.current_node = new_node
            self.start_node = new_node
            self.count += 1
            return
        n = self.current_node

        while n.next is not None:
            n = n.next
        new_node = Node(feature)
        n.next = new_node
        new_node.prev = n
        self.current_node = new_node
        self.count += 1

    def get_current_feature(self) -> Feature or None:
        if self.list_is_empty() or self.current_node is None:
            return None
        return self.current_node.item

    def get_next_feature(self) -> Feature or None:
        if self.list_is_empty() or self.current_node.next is None:
            return None
        return self.current_node.next.item

    def get_prev_feature(self) -> Feature or None:
        if self.list_is_empty() or self.current_node.prev is None:
            return None
        return self.current_node.prev.item

    def pointer_to_next_feature(self) -> Feature or None:
        if self.list_is_empty() or self.current_node.next is None:
            return None
        self.current_node = self.current_node.next
        return self.current_node.item

    def pointer_to_prev_feature(self) -> Feature or None:
        if self.list_is_empty() or self.current_node.prev is None:
            return None
        self.current_node = self.current_node.prev
        return self.current_node.item

    def get_all_features(self) -> list or None:
        features = []
        if self.list_is_empty():
            print("The list is empty")
            return
        else:
            print(self.count)
            n = self.start_node
            features.append((60, 10))
            while n is not None:
                print("Element is: ", n.item)
                print("feature ", n.item.to_string())
                to_next = n.item.vector_to_next
                if to_next is not None:
                    feature = (features[-1][0] + int(round(to_next[0])), features[-1][1] + int(round(to_next[1])))
                    features.append(feature)
                n = n.next
        print("\n")
        return features

    def list_is_empty(self) -> bool:
        return self.start_node is None
