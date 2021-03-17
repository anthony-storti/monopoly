from typing import List, Tuple
import csv
import random


class Board:

    def __init__(self):
        self._board: List[Tile] = list()             # list of all tile objects on the board
        self._current_player: int = 0                # number of current player
        self._players: List[Player] = list()         # list of all current player objects
        self._cards: List[Card] = list()             # list of all card objects
        self._roll: int = 0                          # value of current dice roll
        # add the rest of the board attributes and class methods

    def roll_dice(self):
        self._roll = random.randint(1, 12)
        self._players[self._current_player].advance(self._roll)

    def add_player(self, player):
        self._players.append(player)

    def create_board(self):
        with open('monopoly_squares.csv') as csv_data_file:
            csv_reader = csv.reader(csv_data_file)
            next(csv_reader, None)
            for row in csv_reader:
                tile = Tile(row[0], None, False, row[2], row[5], row[1], row[3], row[4], row[6], row[7], row[8],
                            row[9], row[10], row[11], row[12], row[13], row[14])
                self.set_tile(tile)

    def get_tiles(self):
        return self._board

    def set_tile(self, tile):
        self._board.append(tile)

class Player:

    def __init__(self, name: str, machine_player: bool, board: Board, piece: str):
        self._name = name
        self._machine_player = machine_player
        self._board = board
        self._wallet = 1500
        self._piece = piece
        self._location = 0
        self._inventory = list()
        # add class methods

    def advance(self, distance: int):
        if self._location + distance <= 39:
            self._location += distance
        else:
            self._location = (self._location + distance) % 39

    def get_location(self) -> int:
        return self._location



class Tile:

    def __init__(self, purchasable: bool, owner: Player, mortgaged: bool, name: str, color: str, type: str, action_type: str,
                 action_value: int, cost: int, house_cost: int, rent: int, rent_1: int, rent_2: int, rent_3: int,
                 rent_4: int, rent_5: int, mortgage: int):
        self._purchasable = purchasable
        self._owner = owner
        self._mortgaged = mortgaged
        self._name = name
        self._color = color
        self._type = type
        self._action_type = action_type
        self._action_value = action_value
        self._cost = cost
        self._house_cost = house_cost
        self._rent = rent
        self._rent_house_1 = rent_1
        self._rent_house_2 = rent_2
        self._rent_house_3 = rent_3
        self._rent_house_4 = rent_4
        self._rent_hotel = rent_5
        self._mortgage = mortgage

    def get_name(self) -> str:
        return self._name
        # add class methods



class Card:

    def __init__(self, type: str, msg: str, action_type: str, action_value: Tuple[str, int]):
        self._type = type
        self._msg = msg
        self._action_type = action_type
        self._action_value = action_value
        # add class methods