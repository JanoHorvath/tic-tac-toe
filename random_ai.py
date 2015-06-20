import random

class Randomer:
    """ The second simplest AI. Makes random moves"""

    def __init__(self):
        pass

    def move(self, board):
        x = random.randint(0, 100)
        y = random.randint(0, 100)

        return x, y
