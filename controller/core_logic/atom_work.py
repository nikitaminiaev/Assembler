
class AtomWork:

    def __init__(self):
        self.is_it_surface = True  # todo выделить корневую логику по работе с атомами в класс
        self.is_it_atom = False  # TODO реализовать перемещение атома
        self.is_atom_captured = False
        self.__atoms_set = set()



    def atom_is_unique(self, x: int, y: int, z: int) -> bool:
        atom_len = len(self.__atoms_set)
        self.__atoms_set.add(f"{{'x':{x}, 'y':{y}, 'z':{z}}}")
        return len(self.__atoms_set) > atom_len

