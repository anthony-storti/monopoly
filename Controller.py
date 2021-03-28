from Model import *
from typing import Dict
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


def lands_on(tile: Tile, board: Board) -> Dict:
    ret: Dict[str: str] = {}
    if isinstance(tile, Property):
        if tile.purchasable:
            ret[f"{tile.name} is purchasable press p to purchase for {tile.cost}"] = "p"
            return ret
    elif isinstance(tile, Card):
        return ret
    elif isinstance(tile, GoToJail):
        board.players[board.current_player].location = 9
        return ret
    elif isinstance(tile, Go):
        return ret
    elif isinstance(tile, Tax):
        return ret
    elif isinstance(tile, FreeParking):
        return ret
    elif isinstance(tile, RailRoad):
        return ret
    elif isinstance(tile, Utility):
        return ret
    elif isinstance(tile, Jail):
        return ret




