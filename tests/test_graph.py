import unittest
from unittest import TestCase
from unittest.mock import Mock, MagicMock
from controller.graph import GraphFrame


class FakeGraphFrame(GraphFrame):
    def __init__(self, atoms_logic, ax):
        self.atoms_logic = atoms_logic
        self.ax = ax
        self.is_new_point = False
        self.quit = False
        self.surface = None
        self.tool_tip = None
        self.captured_atom = None
        self.condition_build_surface = False


class TestSetAndValidateCoordinate(TestCase):

    def test_update_graph_data_algorithm(self):
        atoms_logic = Mock()
        atoms_logic.atom_release_event = True
        atoms_logic.atom_captured_event = False
        atoms_logic.is_new_point = MagicMock(return_value=True)
        atoms_logic.is_it_atom = MagicMock(return_value=False)
        atoms_logic.is_atom_captured = MagicMock(return_value=False)
        atoms_logic.tool_is_coming_down = MagicMock(return_value=True)
        atoms_logic.get_tool_coordinate = MagicMock(return_value=[1, 1, 1])
        self.assertTrue(atoms_logic.atom_release_event)

        ax = Mock()
        ax.scatter = MagicMock()

        graph = FakeGraphFrame(atoms_logic, ax)
        graph.update_graph_data_algorithm()

        self.assertFalse(atoms_logic.atom_release_event)


if __name__ == '__main__':
    unittest.main()
