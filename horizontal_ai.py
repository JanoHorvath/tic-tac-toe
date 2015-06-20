class HorizontalDummy:
    """ The simplest AI. Plays in 1D - always on one line"""

    def __init__(self):
        self.x = 0

    def move(self, board):
        self.x += 1

        return self.x, 0
