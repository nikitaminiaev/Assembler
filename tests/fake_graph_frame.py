from unittest.mock import MagicMock, Mock

from controller.frontend.graph import GraphFrame


class FakeGraphFrame(GraphFrame):
    def __init__(self, atoms_logic, ax):
        self.atoms_logic = atoms_logic
        self.ax = ax
        self.is_new_point = False
        self.quit = False
        self.surface = Mock()
        self.surface.remove = MagicMock()
        self.tool_tip = None
        self.captured_atom = None
        self.condition_build_surface = True
        self.canvas = MagicMock(return_value=True)
        self.x_arr, self.y_arr = None, None
        self.origin = None
