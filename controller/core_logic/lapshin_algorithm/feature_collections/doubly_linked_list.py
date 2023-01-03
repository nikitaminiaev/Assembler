from controller.core_logic.entity.feature import Feature


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
            #todo добавить физический переход к next
        new_node = Node(feature)
        n.next = new_node
        new_node.prev = n
        self.current_node = n
        self.count += 1

    def get_next_feature(self) -> Feature or None:
        if self.list_is_empty() or self.current_node.next is None:
            return None
        self.current_node = self.current_node.next
        return self.current_node.item

    def get_prev_feature(self) -> Feature or None:
        if self.list_is_empty() or self.current_node.prev is None:
            return None
        self.current_node = self.current_node.prev
        return self.current_node.item

    def display(self):
        if self.list_is_empty():
            print("The list is empty")
            return
        else:
            print(self.count)
            n = self.start_node
            while n is not None:
                print("Element is: ", n.item)
                n = n.next
        print("\n")

    def list_is_empty(self) -> bool:
        return self.start_node is None
