from dataclasses import dataclass


@dataclass
class Board:
    tiles: list
    current_player: int
    players: list
    cards: list
    roll: int


@dataclass
class Player:
    name: str
    machine_player: bool
    board: Board
    wallet: int
    piece: str
    location: int
    inventory: list


@dataclass
class Tile:
    purchasable: bool
    name: str


@dataclass
class Property(Tile):
    owner:  Player
    mortgaged: bool
    color: str
    cost: int
    house_cost: int
    rent: int
    rent_1: int
    rent_2: int
    rent_3: int
    rent_4: int
    rent_5: int
    mortgage: int
    house_count: int
    hotel_count: int


@dataclass
class Card(Tile):
    action: str
    color: str
