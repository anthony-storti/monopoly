from Model import *
import csv
import random
import pickle


def roll_dice(board: Board):
    board.roll = random.randint(1, 12)
    board.players[board.current_player].location += board.roll


def add_player(player: Player, board: Board):
    board.players.append(player)


def load_board():
    open_file = open("board.pkl", "rb")
    board = pickle.load(open_file)
    open_file.close()
    return board


def lands_on(tile: Tile):
    if isinstance(tile, Property):
        pass
    if isinstance(tile, Card):
        pass




