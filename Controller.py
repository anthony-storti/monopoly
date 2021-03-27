from Model import *
import pickle
import random


def roll_dice(board: Board):
    board.roll = random.randint(1, 6) + random.randint(1, 6)
    if board.roll + board.players[board.current_player].location < 40:
        board.players[board.current_player].location += board.roll
    else:
        board.players[board.current_player].location = (board.roll + board.players[board.current_player].location) - 40
        board.players[board.current_player].wallet += 200


def add_player(player: Player, board: Board):
    board.players.append(player)


def load_game() -> tuple:
    open_file = open("game.pkl", "rb")
    game = pickle.load(open_file)
    open_file.close()
    random.shuffle(game[1])
    random.shuffle(game[2])
    return game[0], game[1], game[2]


def lands_on(tile: Tile, board: Board):
    if isinstance(tile, Property):
        pass
    elif isinstance(tile, Card):
        pass
    elif isinstance(tile, GoToJail):
        board.players[board.current_player].location = 9
    elif isinstance(tile, Go):
        pass
    elif isinstance(tile, Tax):
        pass
    elif isinstance(tile, FreeParking):
        pass
    elif isinstance(tile, RailRoad):
        pass
    elif isinstance(tile, Utility):
        pass
    elif isinstance(tile, Jail):
        pass




