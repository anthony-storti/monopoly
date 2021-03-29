from Model import *
from typing import List, Dict
import pickle
import random


def roll_dice(player: Player):
    player.roll = random.randint(1, 6) + random.randint(1, 6)
    if player.roll + player.location < 40:
        player.location += player.roll
    else:
        player.location = (player.roll + player.location) - 40
        player.wallet += 200


def add_player(player: Player, board: Board):
    board.players.append(player)


def load_game() -> tuple:
    open_file = open("game.pkl", "rb")
    game = pickle.load(open_file)
    open_file.close()
    random.shuffle(game[1])
    random.shuffle(game[2])
    return game[0], game[1], game[2]


def lands_on(tile: Tile, player: Player, comm_chest: List[CommunityChest], chance: List[Chance]) -> List:
    ret = []
    if isinstance(tile, (Property, RailRoad, Utility)):

        if tile.purchasable:
            return ["a", [f"To acquire {tile.name} for ${tile.cost} press a", purchase]]
        elif not tile.purchasable and tile.owner != player:
            rent = get_rent(tile, player)
            return ["p", [f"To pay ${rent} to {tile.owner.name} press p", pay_rent]]
        else:
            return ret

    elif isinstance(tile, CardTile) and tile.name == "Community Chest":

        card = chance.pop()
        return ["p", [f"{card.message} press p to play card: ", play_card, card]]

    elif isinstance(tile, CardTile) and tile.name == "Chance":

        card = comm_chest.pop()
        return ["p", [f"{card.message} press p to play card: ", play_card, card]]

    elif isinstance(tile, GoToJail):
        return ret
    elif isinstance(tile, Go):
        # this is also probably good enough
        return ret
    elif isinstance(tile, Tax):
        # this will be tricky if we decide to allow the 10% option if so we will need a way to calculate net worth
        return ret
    elif isinstance(tile, FreeParking):
        # this is probably good enough
        return ret
    elif isinstance(tile, Jail):
        # this is probably good enough
        return ret


def purchase(player: Player, tile: (Property, RailRoad, Utility)) -> str:
    if player.wallet >= tile.cost:
        player.wallet -= tile.cost
        player.inventory.append(tile)
        tile.purchasable = False
        tile.owner = player
        return "successfully purchased"
    else:
        return "insufficient funds"


def play_card(player: Player, card: (CommunityChest, Chance)) -> str:
    '''
    if card.action == "move_to":
        player.location = card.value
        if card.value != 0 and player.location > card.value:
            player.wallet += 200
        return f"You have advanced to {player.location}"
    else:
        # this will need some work to figure out the mechanism to handle harder cards
    '''
    return "Card Played"


def get_rent(tile: (Property, RailRoad, Utility), player: Player):
    if isinstance(tile, Property):
        rent = [tile.rent, tile.rent_1, tile.rent_2, tile.rent_3, tile.rent_4]
        if tile.hotel_count < 1:
            return rent[tile.house_count]
        else:
            return tile.rent_5
    elif isinstance(tile, Utility):
        util = 0
        for props in tile.owner.inventory:
            if isinstance(props, Utility):
                util += 1
        if util == 1:
            rent = 4 * player.roll
        else:
            rent = 10 * player.roll
        return rent
    elif isinstance(tile, RailRoad):
        rr = 0
        rent = 25
        for props in tile.owner.inventory:
            if isinstance(props, RailRoad):
                rr += 1
                if rr > 1:
                    rent *= 2
        return rent


def pay_rent(player: Player, tile: (Property, RailRoad, Utility)) -> str:
    if isinstance(tile, Property):
        rent = get_rent(tile, player)
        if player.wallet < rent:
            return "Insufficient Funds Mortgage Property or Go Bankrupt \n"
        else:
            player.wallet -= rent
            tile.owner.wallet += rent
            return "Paid"


def change_player(board: Board):
    board.current_player = (board.current_player + 1) % len(board.players)


def machine_algo(options: Dict, player: Player) -> str:
    if "p" in options:
        return "p"
    elif "a" in options:
        return "a"
    else:
        return "q"


def mortgage(tile: Tile, player: Player):
    if isinstance(tile, (Property, RailRoad, Utility)) and not tile.mortgaged:
        player.wallet += tile.mortgage
        tile.mortgaged = True
        return f"{tile.name} has been mortgaged for ${tile.mortgage}"
    else:
        if isinstance(tile, (Property, RailRoad, Utility)) and tile.mortgaged:
            if player.wallet >= tile.mortgage:
                player.wallet -= tile.mortgage
                tile.mortgaged = False
                return f"{tile.name} has been restored to your active inventory"
            else:
                return "insufficient funds"

def build():
    pass


def create_player(name: str, token: str, board: Board, machine: bool = False):
    player = Player(name=name, machine_player=machine, piece=token, location=0, wallet=1500, inventory=list())
    board.players.append(player)
