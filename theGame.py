import Tkinter
import horizontal_ai    as ai1
import random_ai        as ai2


class Player:
    """ Simple player object. Stores name & symbol attributes."""

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


class TheGame:
    """ The Game. Provides interface to play tic-tac-toe. Board is stored in a tuple dictionary e.g. (-3,100) => 'X' """

    def __init__(self, showVisual):
        self.board = {}

        self.player1 = Player('cross', 'X')
        self.player2 = Player('nought', 'O')

        # Define your AIs here
        self.player1.ai = ai1.HorizontalDummy()
        self.player2.ai = ai2.Randomer()

        self.showVisual = showVisual
        if self.showVisual:
            self.tk_app = Tkinter.Tk()
            self.init_graphics(self.tk_app)

        if self.showVisual:
            self.tk_app.mainloop()

        else:
            print 'The game begins! Brace yourselves.'
            self.game_engine(self.player1, self.player2)  # Player1 starts

    def init_graphics(self, tk_app):
        # graphic helpers
        self.canvas = Tkinter.Canvas(tk_app, height=500, width=500)
        self.canvas.grid(row=0, column=0, rowspan=10)

        description_label = Tkinter.Label(tk_app,
                                    text="This is TIC TAC TOE",
                                    justify='left').grid(row=0, column=1, sticky='s')

        this = self

        def player1_move(this):
            try:
                self.game_engine(this.player1, this.player2)
            except ValueError:
                print "Game finished."
                this.tk_app.destroy()

        def player2_move(this):
            try:
                self.game_engine(this.player2, this.player1)
            except ValueError:
                print "Game finished."
                this.tk_app.destroy()

        player1_move_button = Tkinter.Button(tk_app,
                                                  text="AI1 make a move",
                                                  command=lambda: player1_move(self)).grid(row=1,column=1)
        player2_move_button = Tkinter.Button(tk_app,
                                                  text="AI2 make a move",
                                                  command=lambda: player2_move(self)).grid(row=2,column=1)

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
        """ Game loop. Prompts ai to make a move, makes it & checks if it won."""
        while True:
            x, y = current_player.ai.move(self.board)
            if self.whats_on(x, y) is None: break

        self.make_move(current_player, x, y)

        self.check_win(current_player, x, y)

        if self.showVisual:
            self.render()
        else:
            # If playing without graphics, recursively alternates between moves.
            self.game_engine(other_player, current_player)

    def render(self):
        for field in self.board:
            print field
            self.canvas.create_text(field[0]*10+250, field[1]*10+250, text=self.board.get(field))


def run_it(repetitions, showVisual):
    for i in range(1, repetitions+1):
        try:
            TheGame(showVisual)
        except ValueError:
            print "Game {0} finished. ".format(i)