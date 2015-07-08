import random

class Randomer:
    """ The second simplest AI. Makes random moves"""

    def __init__(self):
        pass

    def move(self, board):
        x = random.randint(-10, 10)
        y = random.randint(-10, 10)

        return x, y

    def render(self, canvas):
        pass
