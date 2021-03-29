from Model import *
from typing import List, Dict
import pickle
import random


def roll_dice(board: Board, player: Player):
    board.roll = random.randint(1, 6) + random.randint(1, 6)
    if board.roll + player.location < 40:
        player.location += board.roll
    else:
        player.location = (board.roll + player.location) - 40
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


def lands_on(tile: Tile, player: Player, comm_chest: List[CommunityChest], chance: List[Chance]) -> Dict:
    ret = {}
    if isinstance(tile, Property):

        if tile.purchasable:
            ret[f"{tile.name} is purchasable \n press p to purchase for ${tile.cost}"] = ["p", purchase(player, tile)]
            return ret
        if not tile.purchasable and tile.owner != player:
            rent = get_rent(tile)
            ret[f"{tile.name} is owned by {tile.owner.name} \n pay ${rent}"] = ["p", pay_rent(player, tile, rent)]

    elif isinstance(tile, CardTile) and tile.name == "Community Chest":

        card = chance.pop()
        ret[f"{card.message} press enter to play card"] = ["", play_card(player, card)]
        return ret

    elif isinstance(tile, CardTile) and tile.name == "Chance":

        card = comm_chest.pop()
        ret[f"{card.message} press enter to play card"] = ["", play_card(player, card)]
        return ret

    elif isinstance(tile, GoToJail):
        return ret
    elif isinstance(tile, Go):
        return ret
    elif isinstance(tile, Tax):
        return ret
    elif isinstance(tile, FreeParking):
        # this is probably good enough
        return ret
    elif isinstance(tile, RailRoad):
        return ret
    elif isinstance(tile, Utility):
        return ret
    elif isinstance(tile, Jail):
        # this is probably good enough
        return ret


def purchase(player: Player, tile: (Property, RailRoad, Utility)) -> str:
    if player.wallet >= tile.cost:
        player.wallet -= tile.cost
        player.inventory.append(tile)
        tile.purchasable = False
        return "successfully purchased"
    else:
        return "insufficient funds"


def play_card(player: Player, card: (CommunityChest, Chance)) -> str:
    # this will need some work to figure out the mechanism to handle harder cards
    return card.message


def get_rent(tile: Property):
    rent = [tile.rent, tile.rent_1, tile.rent_2, tile.rent_3, tile.rent_4]
    if tile.hotel_count < 1:
        return rent[tile.house_count]
    else:
        return tile.rent_5


def pay_rent(player: Player, tile: (Property, RailRoad, Utility), rent: int) -> str:
    if isinstance(tile, (Property, RailRoad)):
        if player.wallet < rent:
            return "Insufficient Funds Mortgage Property or Go Bankrupt"
        else:
            player.wallet -= rent
            tile.owner.wallet += rent


def change_player(board):
    board.current_player = (board.current_player + 1) % len(board.players)
