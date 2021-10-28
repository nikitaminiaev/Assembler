class TouchingSurface(ValueError):
    def __init__(self, message="touching the surface"):
        self.message = message
        super().__init__(self.message)
