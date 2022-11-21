from unittest import TestCase
from unittest.mock import Mock, MagicMock

from controller.core_logic.atom_logic import AtomsLogic, DTO_Y, DTO_X, DTO_Z


class TestOrigin(TestCase):
    server_mock = None

    @classmethod
    def setUpClass(cls):
        cls.server_mock = Mock()
        attrs = {
            'type_object': 'Server',
            'external_handle_func': '',
        }
        cls.server_mock.configure_mock(**attrs)

    @classmethod
    def tearDownClass(cls):
        cls.server_mock = None

    def setUp(self) -> None:
        self.atom_logic = AtomsLogic(10, 10, self.__class__.server_mock)
        self.atom_logic.set_is_surface(False)

    def tearDown(self) -> None:
        self.atom_logic = None

    def test_set_new_origin(self):
        coord = (1, 2, 3)
        self.atom_logic.set_val_to_dto(DTO_X, coord)
        self.atom_logic.set_val_to_dto(DTO_Y, coord)
        self.atom_logic.set_val_to_dto(DTO_Z, coord)

        self.atom_logic.set_new_origin_coordinate()

        self.assertEqual(self.atom_logic.get_origin_coordinate(), coord)