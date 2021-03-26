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
    color: str

    def land_on(self, player: Player):
        pass


@dataclass
class Property(Tile):
    owner:  Player
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

    def land_on(self, player: Player):
        player.wallet += 200


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
    cost: 200
    mortgage: int

    def land_on(self, player: Player):
        if self.owner is None:
            print("Would you like to buy " + self.name + " for " + self.cost + "? (Y/N)")


@dataclass
class Tax(Tile):
    action: str
    value: int


@dataclass
class Utility(Tile):
    owner: Player
    cost: int
    value: int


@dataclass
class Card(Tile):
    action: str


@dataclass
class Jail(Tile):
    action: str
