import unittest
from unittest import TestCase
from unittest.mock import Mock, MagicMock, call

from controller.core_logic.entity.atom import Atom
from controller.frontend.graph import COLOR_ATOM, COLOR_TIP, COLOR_ORIGIN
from tests.fake_graph_frame import FakeGraphFrame


class TestGraphWithFakeAtomLogic(TestCase):

    def setUp(self) -> None:
        self.atoms_logic = Mock()
        self.atoms_logic.get_tool_coordinate = MagicMock(return_value=[1, 1, 1])
        self.atoms_logic.get_origin_coordinate = MagicMock(return_value=[0, 0, 0])
        self.atoms_logic.set_is_surface = MagicMock()
        self.atoms_logic.set_is_atom = MagicMock()
        atom0 = Atom(self.atoms_logic.get_tool_coordinate())
        atom0.is_captured = True
        atom_coord1 = (1, 2, 3)
        atom1 = Atom(atom_coord1)
        self.atoms_logic.atom_collection.atoms_list = [atom0, atom1]

    def tearDown(self) -> None:
        self.atom_logic = None

    def test_update_graph_when_is_not_new_point(self):
        self.atoms_logic.is_new_point = MagicMock(return_value=False)
        self.atoms_logic.is_surface_changed_event = False
        graph = self.__get_graph_obj()
        graph.update_graph_data_algorithm()

        graph.ax.scatter.assert_not_called()
        graph.ax.plot_surface.assert_not_called()
        graph.canvas.draw_idle.assert_not_called()
        graph.ax.mouse_init.assert_not_called()
        self.atoms_logic.set_is_surface.assert_not_called()
        self.atoms_logic.set_is_atom.assert_not_called()
        graph.surface.remove.assert_not_called()

    def test_update_graph_data_algorithm(self):
        self.atoms_logic.atom_release_event = True
        self.atoms_logic.atom_captured_event = True
        self.atoms_logic.is_new_point = MagicMock(return_value=True)
        self.atoms_logic.is_atom = MagicMock(return_value=True)
        self.atoms_logic.is_atom_captured = MagicMock(return_value=True)
        self.atoms_logic.tool_is_coming_down = MagicMock(return_value=False)

        graph = self.__get_graph_obj()
        graph.update_graph_data_algorithm()

        self.assertFalse(self.atoms_logic.atom_release_event)
        self.assertFalse(self.atoms_logic.atom_captured_event)
        calls = [
            call(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_ATOM, marker='8'),
            call(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_TIP, marker='8'),
            call(*self.atoms_logic.get_origin_coordinate(), s=5, c=COLOR_ORIGIN, marker='8'),
            call(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_ATOM, marker='8'),
            call(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_TIP, marker='8'),
            call(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_ATOM, marker='8'),
            call(*(1, 2, 3), s=5, c=COLOR_ATOM, marker='8'),
            call(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_ATOM, marker='8'),
        ]
        graph.ax.scatter.assert_has_calls(calls, any_order=False)
        graph.ax.plot_surface.assert_called_once()
        graph.canvas.draw_idle.assert_called_once()
        graph.ax.mouse_init.assert_called_once()
        graph.surface.remove.assert_called_once()
        self.atoms_logic.set_is_surface.assert_called_once_with(False)
        self.atoms_logic.set_is_atom.assert_called_once_with(False)
        self.atoms_logic.update_tool_coordinate.assert_called_once()

    def test_update_graph_another_data_algorithm(self):
        self.atoms_logic.atom_release_event = False
        self.atoms_logic.atom_captured_event = False
        self.atoms_logic.is_new_point = MagicMock(return_value=True)
        self.atoms_logic.is_atom = MagicMock(return_value=False)
        self.atoms_logic.is_atom_captured = MagicMock(return_value=False)
        self.atoms_logic.tool_is_coming_down = MagicMock(return_value=True)

        graph = self.__get_graph_obj()
        graph.update_graph_data_algorithm()

        self.assertFalse(self.atoms_logic.atom_release_event)
        self.assertFalse(self.atoms_logic.atom_captured_event)
        calls = [
            call(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_TIP, marker='8'),
            call(*self.atoms_logic.get_origin_coordinate(), s=5, c=COLOR_ORIGIN, marker='8'),
        ]
        graph.ax.scatter.assert_has_calls(calls, any_order=False)
        graph.ax.plot_surface.assert_called_once()
        graph.canvas.draw_idle.assert_called_once()
        graph.ax.mouse_init.assert_called_once()
        graph.surface.remove.assert_called_once()
        self.atoms_logic.set_is_surface.assert_not_called()
        self.atoms_logic.set_is_atom.assert_not_called()
        self.atoms_logic.update_tool_coordinate.assert_called_once()

    def __get_graph_obj(self):
        ax = Mock()
        ax.scatter = MagicMock()
        graph = FakeGraphFrame(self.atoms_logic, ax)
        ax.plot_surface = MagicMock(return_value=graph.surface)
        return graph


if __name__ == '__main__':
    unittest.main()
