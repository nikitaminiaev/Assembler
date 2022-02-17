import unittest
from unittest import TestCase
from unittest.mock import Mock, MagicMock, call

from controller.core_logic.atom import Atom
from controller.core_logic.atom_logic import AtomsLogic
from controller.graph import GraphFrame, COLOR_ATOM, COLOR_TIP
from tests.test_graph_with_fake_atom_logic import FakeGraphFrame


class TestGraphWithRealAtomLogic(TestCase):

    def setUp(self) -> None:
        server_mock = Mock()
        attrs = {
            'type_object': 'Server',
            'external_handle_func': '',
        }
        server_mock.configure_mock(**attrs)
        self.atoms_logic = AtomsLogic(10, 10, server_mock)

    def tearDown(self) -> None:
        self.atoms_logic = None

    def test_update_graph_data_algorithm(self):
        self.atoms_logic.atom_release_event = True
        self.atoms_logic.atom_captured_event = True
        self.atoms_logic.set_is_it_atom(True)
        self.atoms_logic.set_is_it_surface(True)
        graph = self.__get_graph_obj()
        graph.update_graph_data_algorithm()

        calls = [
            call(*(0, 0, 0), s=5, c=COLOR_ATOM, marker='8'),
            call(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_TIP, marker='8'),
            call(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_ATOM, marker='8'),
            call(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_TIP, marker='8'),
            call(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_ATOM, marker='8'),
        ]
        self.atoms_logic.server.send_data_to_all_clients.assert_called_once_with('{"sensor": "servo_z", "value": "0"}')
        graph.ax.scatter.assert_has_calls(calls, any_order=False)
        self.assertFalse(self.atoms_logic.atom_release_event)
        self.assertFalse(self.atoms_logic.atom_captured_event)
        self.assertEqual(1, len(self.atoms_logic.atom_collection.atoms_list))
        self.assertFalse(self.atoms_logic.is_it_atom())
        self.assertFalse(self.atoms_logic.is_it_atom())

    def test_update_graph_another_data_algorithm(self):
        self.atoms_logic.atom_release_event = True
        self.atoms_logic.atom_captured_event = True
        self.atoms_logic.set_is_it_surface(True)
        self.atoms_logic.set_is_it_atom(False)
        graph = self.__get_graph_obj()
        graph.update_graph_data_algorithm()

        calls = [
            call(*(0, 0, 0), s=5, c=COLOR_ATOM, marker='8'),
            call(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_TIP, marker='8'),
            call(*self.atoms_logic.get_tool_coordinate(), s=5, c=COLOR_TIP, marker='8'),
        ]
        graph.ax.scatter.assert_has_calls(calls, any_order=False)

        self.atoms_logic.server.send_data_to_all_clients.assert_called_once_with('{"sensor": "servo_z", "value": "0"}')

        self.assertEqual(0, len(self.atoms_logic.atom_collection.atoms_list))
        self.assertFalse(self.atoms_logic.atom_release_event)
        self.assertFalse(self.atoms_logic.atom_captured_event)
        self.assertFalse(self.atoms_logic.is_it_atom())
        self.assertFalse(self.atoms_logic.is_it_atom())

    def __get_graph_obj(self):
        ax = Mock()
        ax.scatter = MagicMock()
        graph = FakeGraphFrame(self.atoms_logic, ax)
        ax.plot_surface = MagicMock(return_value=graph.surface)
        return graph


if __name__ == '__main__':
    unittest.main()
