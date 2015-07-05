import Tkinter
import pickle
import horizontal_ai    as ai1
import random_ai        as ai2

class GameOver(Exception):
    pass


class InvalidMove(Exception):
    pass


class Player:
    """ Simple player object. Stores name & symbol attributes."""

    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol


class TheGame:
    """ The Game. Provides interface to play tic-tac-toe. Board is stored in a tuple dictionary e.g. (-3,100) => 'X' """

    def __init__(self, board, showVisual):
        self.board = board
        self.victoriousFields = []

        self.player1 = Player('cross', 'X')
        self.player2 = Player('nought', 'O')

        # Define your AIs here
        self.player1.ai = ai2.Randomer()
        self.player2.ai = ai1.HorizontalDummy()

        self.showVisual = showVisual
        if self.showVisual:
            self.tk_app = Tkinter.Tk()
            self.init_graphics(self.tk_app)
            self.tk_app.mainloop()
        else:
            print 'The game begins! Brace yourselves.'
            self.game_engine(self.player1, self.player2)  # Player1 starts

    def init_graphics(self, tk_app):
        # graphic helpers
        self.canvas = Tkinter.Canvas(tk_app, height=500, width=500)
        self.canvas.grid(row=0, column=0, rowspan=10)

        def human_move(event):
            try:
                x = (event.x - event.x%10 - 250)/10
                y = (event.y + 10 - event.y%10 - 250)/10
                self.graphic_game_engine(self.player1, (x, y))
                ai2_move(self)
            except InvalidMove:
                print 'Invalid move on ({0},{1}). Try again!'.format(x, y)
            except GameOver:
                print "Game finished."
                tk_app.bind("<Button-1>", close_window)

        self.canvas.bind("<Button-1>", human_move)

        def close_window(event):
            tk_app.destroy()

        def ai1_move(this):
            try:
                self.graphic_game_engine(self.player1, None)
            except GameOver:
                print "Game finished."
                tk_app.bind("<Button-1>", close_window)

        def ai2_move(this):
            try:
                self.graphic_game_engine(self.player2, None)
            except GameOver:
                print "Game finished."
                tk_app.bind("<Button-1>", close_window)

        ai1_move_button = Tkinter.Button(tk_app,
                                                  text="AI1 make a move",
                                                  command=lambda: ai1_move(self)).grid(row=1, column=1)
        ai2_move_button = Tkinter.Button(tk_app,
                                                  text="AI2 make a move",
                                                  command=lambda: ai2_move(self)).grid(row=2, column=1)

        description_label = Tkinter.Label(tk_app,
                                    text="This is TIC TAC TOE",
                                    justify='left').grid(row=0, column=1, sticky='s')

        if self.board:
            try:
                self.check_win()
            except GameOver:
                tk_app.bind("<Button-1>", close_window)

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
            self.board['last_move'] = (x, y, player)
            print "[ {0} ] played a move at: {1},{2}".format(player.name, x, y)

    def the_end(self, winner):
        if self.showVisual:
            self.render()
        print "[ {0} ] won! End of game :)".format(winner.name)
        save_board_to_file(self.board)
        raise GameOver()

    def check_win(self):
        """ Checks, if the last move made is a winning move (= whether x,y is a winning move for player)"""

        x = self.board['last_move'][0]
        y = self.board['last_move'][1]
        player = self.board['last_move'][2]

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
                for j in range(1, i+1):
                    self.victoriousFields.append((startX + j, y))
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
                for j in range(1, i+1):
                    self.victoriousFields.append((x, startY + j))
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
                for j in range(1, i+1):
                    self.victoriousFields.append((startX - j, startY + j))
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
                for j in range(0, i+1):
                    self.victoriousFields.append((startX + j, startY + j))
                self.the_end(player)

    def game_engine(self, current_player, other_player):
        """ Game loop. Prompts ai to make a move, makes it & checks if it won."""
        while True:
            x, y = current_player.ai.move(self.board)
            if self.whats_on(x, y) is None: break

        self.make_move(current_player, x, y)

        self.check_win()

        self.game_engine(other_player, current_player)

    def graphic_game_engine(self, current_player, human_move):
        if human_move:
            if self.whats_on(human_move[0], human_move[1]) is not None:
                raise InvalidMove()
            else:
                x = human_move[0]
                y = human_move[1]
        else:
            while True:
                x, y = current_player.ai.move(self.board)
                if self.whats_on(x, y) is None: break

        self.make_move(current_player, x, y)

        self.render()

        self.check_win()

    def render(self):
        self.canvas.delete('all')
        for field in self.board:
            if field == 'last_move':
                pass
            else:
                if (field[0], field[1]) in self.victoriousFields:
                    color = 'red'
                else:
                    color = 'black'

                self.canvas.create_text(field[0]*10+250, field[1]*10+250, text=self.board.get(field), fill=color)

def save_board_to_file(obj):
    with open('last_game_log.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def run_it(repetitions, showVisual):
    for i in range(1, repetitions+1):
        try:
            TheGame({}, showVisual)
        except GameOver:
            print "Game {0} finished. ".format(i)

def load_existing(board):
    try:
        TheGame(board, True).check_win()
    except Exception:
        pass

