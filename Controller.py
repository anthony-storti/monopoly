from Model import *
from typing import List, Dict
import pickle
import random


def roll_dice(player: Player):
    """
    Roll Dice - After this call player location will be updated, if a player passes or lands on go their
    wallet will be increased by $200.
    :param player: current player object from board
    :return: nothing
    """
    player.roll = random.randint(1, 6) + random.randint(1, 6)
    if player.roll + player.location < 40:
        player.location += player.roll
    else:
        player.location = (player.roll + player.location) - 40
        player.wallet += 200


def add_player(player: Player, board: Board):
    """
     **** THIS IS DEPRECATED AND SHOULD NOT BE USED OTHER THAN FOR TESTING  ****
    Add Player - After this call players will be added to the current game board player list
    :param player: Player object to be added
    :param board: Board object to add player to
    :return: nothing
    """
    board.players.append(player)


def load_game() -> tuple:
    """
    Load Game - After this call a the game board will be initialized from the pickle file, the deck of
    community chest and chance cards will be loaded and shuffled from pickle file.
    :param
    :return: Tuple: board object, deck of shuffled community chest cards, deck of shuffled chance cards
    """
    open_file = open("game.pkl", "rb")
    game = pickle.load(open_file)
    open_file.close()
    random.shuffle(game[1])
    random.shuffle(game[2])
    return game[0], game[1], game[2]


def lands_on(tile: Tile, player: Player, comm_chest: List[CommunityChest], chance: List[Chance]) -> List:
    """
    Lands On - After this call whatever functions are available for a given tile will be returned to the user.
    :param tile: Tile object action called on
    :param player: Player object current player on board
    :param comm_chest: List/Deck of community chest cards
    :param chance: List/Deck of Chance cards
    :return: List str to call command in view, str to prompt user in view, command,
     optional card object if tile is CardTile
    """
    ret = []
    if isinstance(tile, (Property, RailRoad, Utility)):
        if tile.purchasable:
            '''
            if Property, Railroad or Utility and is Purchasable
            command: a
            prompt: To acquire tile for $cost press a
            function: purchase
            '''
            return ["a", [f"To acquire {tile.name} for ${tile.cost} press a", purchase]]
        elif not tile.purchasable and tile.owner != player and not tile.mortgaged:
            '''
            if Property, Railroad or Utility and is owned by another player, and not mortgaged
            command: p
            prompt: To pay $rent to name press p
            function: pay_rent
            '''
            rent = get_rent(tile, player)
            return ["p", [f"To pay ${rent} to {tile.owner.name} press p", pay_rent]]
        else:
            return ret
    elif isinstance(tile, CardTile) and tile.name == "Community Chest":
        '''
        if Community Chest
        command: p
        prompt: card script press p to play card
        function: play_card
        note: returns card drawn
        '''
        card = chance.pop()
        chance.insert(0, card)
        return ["p", [f"{card.message} press p to play card: ", play_card, card]]

    elif isinstance(tile, CardTile) and tile.name == "Chance":
        '''
        if Chance
        command: p
        prompt: card script press p to play card
        function: play_card
        note: returns card drawn
        '''
        card = comm_chest.pop()
        comm_chest.insert(0, card)
        return ["p", [f"{card.message} press p to play card: ", play_card, card]]
    elif isinstance(tile, GoToJail):
        # TODO: Implement
        '''
        if Go To Jail
        command: 
        prompt: 
        function: 
        note: 
        '''
        return ret
    elif isinstance(tile, Go):
        '''
        if Go
        command: nothing
        prompt: nothing
        function: nothing
        note: collect $200 is taken care of in roll dice
        '''
        return ret
    elif isinstance(tile, Tax):
        # TODO: Implement
        '''
        if Tax
        command:  
        prompt: 
        function: 
        note: This could be tricky, we will need a case for Luxury and Income Tax,
        Income tax traditionally is 10% net worth or $200
        '''
    elif isinstance(tile, FreeParking):
        '''
        if Free Parking
        command: nothing
        prompt: nothing
        function: nothing
        note: This should do and does nothing if a player lands on it
        '''
        return ret
    elif isinstance(tile, Jail):
        # TODO: Implement
        '''
        if Jail
        command: 
        prompt: 
        function: 
        note: Who ever designs Go To Jail may decide to use this for something or it will literally do nothing
        '''
        return ret


def purchase(player: Player, tile: (Property, RailRoad, Utility)) -> str:
    """
    Purchase  - After this call if a user can afford it a Purchasable tile will be added to their inventory,
    and their wallet will be deducted the cost of the Tile. The Tile's Purchasable bool will switch to false.
    :param player: Player object looking to make purchase
    :param tile: Tile object to be purchased
    :return: str: if successfully purchased or insufficient funds
    """
    if player.wallet >= tile.cost:
        player.wallet -= tile.cost
        player.inventory.append(tile)
        tile.purchasable = False
        tile.owner = player
        return "successfully purchased"
    else:
        return "insufficient funds"


def play_card(player: Player, card: (CommunityChest, Chance)) -> str:
    """
    Play Card  - After this call whatever functionality of a community chest or chance card will be executed
    :param player: Player playing card
    :param card: the actual card from the deck to be executed
    :return: str: str informing user of what happened
    """
    # TODO: Implement, will need to adjust csv files more than likely to fit what you need
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
    """
    Get Rent  - After this call the rent value of Property, Railroad and Utility will be calculated
    :param tile: tile: Tile object to calculate rent on
    :param player: Player object paying rent(to get dice roll for Utility)
    :return: int: calculated rent
    """
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
    """
    Pay Rent - After this call if a player has sufficient funds the owed rent will be deducted from their wallet
    :param player: Player paying the rent
    :param tile: Tile object rent is to be paid on
    :return: str: str of payment confirmation or insufficient funds
    """
    rent = get_rent(tile, player)
    if player.wallet < rent:
        return "Insufficient Funds Mortgage Property or Go Bankrupt \n"
    else:
        player.wallet -= rent
        tile.owner.wallet += rent
        return "Paid"


def change_player(board: Board):
    """
    Change Player - After this call the current board player will change to the next player
    :param board: Board object of current game
    :return: nothing
    """
    board.current_player = (board.current_player + 1) % len(board.players)


def machine_algo(options: Dict, player: Player) -> str:
    """
    Machine Algo - After this call the machine player will return a choice based on available options passed in
    :param options: a Dict of available choices
    :param player: Player object of machine player
    :return: str: choice made by machine
    """
    # TODO: Implement a Real Machine Player ALGO
    if "p" in options:
        return "p"
    elif "a" in options:
        return "a"
    else:
        return "q"


def mortgage(tile: Tile, player: Player):
    """
    Mortgage - After this call either a tile mortgaged property set to True and the wallet of the player increased or
    if the player has sufficient funds their wallet deducted and the tile mortgaged value set to False
    :param tile: tile object to be acted on
    :param player: Player object making call
    :return: str: information about action performed.
    """
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
    """
    Build - After this call a house or hotel will be added to a tile if a player can afford it and
    it is a legal game action
    :param
    :return: str: information about action performed.
    """
    # TODO: Implement
    pass


def create_player(name: str, token: str, board: Board, machine: bool = False):
    """
    Create Player - After this call a player object will be created and added to the game board
    :param name: str for player name
    :param token: str of player token(hat, car, etc.)
    :param board: Board object to add player on
    :param machine: bool indicating if player is a machine player
    :return: nothing
    """
    player = Player(name=name, machine_player=machine, piece=token, location=0, wallet=1500, inventory=list(), roll=0)
    board.players.append(player)
