import horizontal_ai    as ai1
import random_ai        as ai2

class Player:
    """ Simple player object. Stores name & symbol attributes."""

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


class TheGame:
    """ The Game. Provides interface to play tic-tac-toe. Board is stored in a tuple dictionary e.g. (-3,100) => 'X' """

    def __init__(self):
        self.board = {}

        player1 = Player('cross', 'X')
        player2 = Player('nought', 'O')

        # Define your AIs here
        player1.ai = ai1.HorizontalDummy()
        player2.ai = ai2.Randomer()

        print 'The game begins! Brace yourselves.'
        self.game_engine(player1, player2)  # Cross starts

    def whats_on(self, x, y):
        """ Returns symbol on (x, y) if there is one, None otherwise. """
        try:
            result = self.board[(x, y)]
        except KeyError:
            result = None

        return result

    def make_move(self, player, x, y):
        """ Adds player's symbol to the board, if that spot is empty. """
        if self.whats_on(x, y) is None:
            self.board[(x, y)] = player.symbol
            print "[ {0} ] played a move at: {1},{2}".format(player.name, x, y)

    def the_end(self, winner):
        print "[ {0} ] won! End of game :)".format(winner.name)
        raise ValueError('End of game')

    def check_win(self, player, x, y):
        """ Checks, whether x,y is a winning move for player"""
        print "[ {0} ] check_win".format(player.name)

        """ Horizontal check """
        startX = x - 5
        count = 0
        for i in range(1, 10):
            if self.whats_on(startX + i, y) == player.symbol:
                count += 1
            else:
                count = 0

            if count == 5:
                self.the_end(player)

        """ Vertical check """
        startY = y - 5
        count = 0
        for i in range(1, 10):
            if self.whats_on(x, startY + i) == player.symbol:
                count += 1
            else:
                count = 0

            if count == 5:
                self.the_end(player)

        """ Diagonal \ check """
        startX = x + 5
        startY = y - 5
        count = 0
        for i in range(1, 10):
            if self.whats_on(startX - i, startY + i) == player.symbol:
                count += 1
            else:
                count = 0

            if count == 5:
                self.the_end(player)

        """ Diagonal / check """
        startX = x - 5
        startY = y - 5
        count = 0
        for i in range(1, 10):
            if self.whats_on(startX + i, startY + i) == player.symbol:
                count += 1
            else:
                count = 0

            if count == 5:
                self.the_end(player)

    def game_engine(self, current_player, other_player):
        """ Game loop. Recursively alternates between moves. Prompts ai to make a move, makes it & checks if it won."""
        while True:
            x, y = current_player.ai.move(self.board)
            if self.whats_on(x, y) is None: break

        self.make_move(current_player, x, y)

        self.check_win(current_player, x, y)

        self.game_engine(other_player, current_player)
