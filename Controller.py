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
    roll1 = random.randint(1, 6)
    roll2 = random.randint(1, 6)
    player.roll = roll1 + roll2
    if roll1 == roll2:
        if player.extra_turns < 3:
            player.extra_turns += 1
            player.extra_turn = True
        else:
            player.in_jail = True
            player.location = 10
            player.jail_counter = 4
            player.extra_turns = 0
    else:
        player.extra_turns = 0
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
        card = comm_chest.pop()
        comm_chest.insert(0, card)
        return ["p", [f"{card.message} press p to play card: ", play_card, card]]

    elif isinstance(tile, CardTile) and tile.name == "Chance":
        '''
        if Chance
        command: p
        prompt: card script press p to play card
        function: play_card
        note: returns card drawn
        '''
        card = chance.pop()
        if card.action != "special":
            chance.insert(0, card)
        return ["p", [f"{card.message} press p to play card: ", play_card, card]]
    elif isinstance(tile, GoToJail):
        '''
        if Go To Jail
        command: nothing
        prompt: nothing
        function: nothing
        note: the "in jail" functionality still has to be handled elsewhere
        '''
        player.in_jail = True
        player.jail_counter = 3
        player.location = 10
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
        '''
        if Tax
        command: p
        prompt: to pay $tax press p
        function: pay_rent
        note: Income tax takes either $200 or 10% of the player's net worth, whichever is lower
        '''
        if tile.name == "Income Tax":
            player_net_worth = player.wallet
            for item in player.inventory:
                if isinstance(item, (Property, RailRoad, Utility)):
                    player_net_worth += item.cost
                    if isinstance(tile, Property):
                        player_net_worth += tile.house_cost * tile.house_count
                        player_net_worth += tile.house_cost * tile.hotel_count
                else:
                    player_net_worth += item.value
            player_net_worth = player_net_worth // 10
            if player_net_worth > 200:
                return ["p", [f"To pay $200 in taxes press p", pay_tax]]
            else:
                return ["p", [f"To pay ${player_net_worth} in taxes press p", pay_tax]]
        else:
            return ["p", [f"To pay $75 in taxes press p", pay_tax]]

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
        '''
        if Jail
        command: u, p, r
        prompt: to use card press u, to pay bail press p, to try to roll doubles press r
        function: use_jail_card, pay_bail, jail_roll
        note: The "in jail" functionality is handled here
        '''
        if player.in_jail:
            if player.jail_counter == 4:
                player.jail_counter -= 1
            if player.jail_counter > 0:
                player.jail_counter -= 1
                for item in player.inventory:
                    if isinstance(item, (CommunityChest, Chance)):
                        if "Get out of Jail" in item.message:
                            return [["u", [f"To use your Get out of Jail Free card press u", use_jail_card]],
                                    ["r", [f"To try to roll doubles press r", jail_roll]]]
                return [["r", [f"To try to roll doubles press r", jail_roll]],
                        ["p", [f"To pay $50 and get out of jail press p", pay_bail]]]
            else:
                for item in player.inventory:
                    if isinstance(item, (CommunityChest, Chance)):
                        if "Get out of Jail" in item.message:
                            return ["u", [f"To use your Get out of Jail Free card press u", use_jail_card]]
                return ["p", [f"To pay $50 and get out of jail press p", pay_bail]]
        else:
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


def play_card(player: Player, card: (CommunityChest, Chance), player_list: List[Player]) -> str:
    """
    Play Card  - After this call whatever functionality of a community chest or chance card will be executed
    :param player: Player playing card
    :param card: the actual card from the deck to be executed
    :param player_list: the list of all players
    :return: str: str informing user of what happened
    """
    # initialize values
    value_list = []
    smallest = int(value_list[0])
    small_value = 10000
    card.value = card.value.rstrip('\n')
    for i in card.value:
        if i == ";":
            value_list = card.value.split(";")

    if card.action == "move_to":
        if card.value != 0 and player.location > card.value:
            player.wallet += 200
        player.location = card.value
        return f"You have advanced to {player.location}"
    elif card.action == "move_to_closest":
        for i in value_list:
            if player.location - int(value_list[i]) < small_value:
                smallest = int(value_list[i])
                small_value = player.location - int(value_list)
            elif player.location - int(value_list) == small_value:
                choice = random.randint(0, len(value_list))
                smallest = int(value_list[choice])
        player.location = smallest
        return f"You have advanced to {player.location}"
    elif card.action == "Finance_1":
        player.wallet += card.value
        if card.value < 0:
            return f"You have paid {abs(card.value)} for tax"
        else:
            return f"You have gained {card.value}"
    elif card.action == "finance":
        player.wallet += card.value
        return f"You have gained {card.value}"
    elif card.action == "finance_player":
        player.wallet -= card.value
        for p in player_list:
            if p.name != player.name:
                p.wallet -= card.value
        return f"You have paid {card.value} for each players in the game"
    elif card.action == "Finance_house":
        player.wallet += card.value
        return f"You have paid {abs(card.value)} for repairing the houses"
    elif card.action == "move_steps":
        player.location += card.value
        return f"You have moved {abs(card.value)} steps back"
    elif card.action == "special":
        player.inventory.append(card)
        return f"You have gained a jail card"
    return "Card Played"


def use_jail_card(player: Player, comm_chest: List[CommunityChest], chance: List[Chance]):
    player.in_jail = False
    for item in player.inventory:
        if isinstance(item, Chance):
            player.inventory.remove(item)
            chance.insert(0, item)
            break
        elif isinstance(item, CommunityChest):
            player.inventory.remove(item)
            comm_chest.insert(0, item)
            break


def pay_bail(player: Player):
    if player.wallet < 50:
        return "Insufficient Funds Mortgage Property or Go Bankrupt \n"
    else:
        player.wallet -= 50
        player.in_jail = False
        return "Paid"


def jail_roll(tile: Tile, player: Player, comm_chest: List[CommunityChest], chance: List[Chance]):
    roll1 = random.randint(1, 6)
    roll2 = random.randint(1, 6)
    if roll1 == roll2:
        player.in_jail = False
        player.roll = roll1 + roll2
        player.location += player.roll
        return "You got out of jail"
    else:
        if player.jail_counter == 0:
            lands_on(tile, player, comm_chest, chance)


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


def pay_tax(player: Player, tile: Tax) -> str:
    """
    Pay Tax - After this call if a player has sufficient funds the owed tax will be deducted from their wallet
    :param player: The player paying the tax
    :param tile: Tile object the tax is paid on
    :return: str: str of payment confirmation or insufficient funds
    """
    if tile.name == "Income Tax":
        player_net_worth = player.wallet
        for item in player.inventory:
            if isinstance(tile, Property):
                player_net_worth += item.cost
                player_net_worth += tile.house_cost * tile.house_count
                player_net_worth += tile.house_cost * tile.hotel_count
            elif isinstance(item, Card):
                player_net_worth += 50
        player_net_worth = player_net_worth // 10
        if player_net_worth > 200:
            if player.wallet < 200:
                return "Insufficient Funds Mortgage Property or Go Bankrupt \n"
            else:
                player.wallet -= 200
                return "Paid"
        else:
            if player.wallet < player_net_worth:
                return "Insufficient Funds Mortgage Property or Go Bankrupt \n"
            else:
                player.wallet -= player_net_worth
                return "Paid"
    else:
        if player.wallet < 75:
            return "Insufficient Funds Mortgage Property or Go Bankrupt \n"
        else:
            player.wallet -= 75
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
    player = Player(name=name, machine_player=machine, piece=token, location=0, wallet=1500,
                    inventory=list(), roll=0, in_jail=False, jail_counter=0, extra_turns=0)
    board.players.append(player)
