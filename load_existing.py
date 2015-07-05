import theGame
import pickle

LAST_GAME_PATH = 'last_game_log.pkl'

def load_board():
    with open(LAST_GAME_PATH, 'rb') as board_file:
        return pickle.load(board_file)

board = load_board()

theGame.load_existing(board)


