from dataclasses import dataclass


@dataclass
class Board:
    tiles: list
    current_player: int
    players: list
    cards: list


@dataclass
class Player:
    wallet: int
    name: str
    machine_player: bool
    piece: str
    location: int
    inventory: list
    roll: int
    in_jail: bool
    jail_counter: int
    extra_turns: int
    extra_turn: bool


@dataclass
class Tile:
    purchasable: bool
    name: str
    color: str


@dataclass
class Property(Tile):
    owner: Player
    mortgaged: bool
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
class Go(Tile):
    action: str
    value: int


@dataclass
class GoToJail(Tile):
    action: str
    value: int


@dataclass
class FreeParking(Tile):
    action: str


@dataclass
class RailRoad(Tile):
    owner: Player
    cost: int
    mortgage: int
    mortgaged: bool


@dataclass
class Tax(Tile):
    action: str
    value: int


@dataclass
class Utility(Tile):
    owner: Player
    cost: int
    value: int
    mortgaged: bool


@dataclass
class CardTile(Tile):
    action: str


@dataclass
class Jail(Tile):
    action: str


@dataclass
class Card:
    action: str
    value: str


@dataclass
class CommunityChest(Card):
    message: str


@dataclass
class Chance(Card):
    message: str
