from Model import *
from typing import List, Dict
import pickle
import random
import pygame


def roll_dice(player: Player, board: Board):
    """
    Roll Dice - After this call player location will be updated, if a player passes or lands on go their
    wallet will be increased by $200.
    :param player: current player object from board
    :param board: board object to get tile coordinates from
    :return: nothing
    """
    ret = []
    if not player.rolled:
        # if player.machine_player:
        roll1 = random.randint(1, 6)
        roll2 = random.randint(1, 6)
        # else:
        #     roll1 = int(input("roll 1"))
        #     roll2 = int(input("roll 2"))

        player.roll_1 = roll1
        player.roll_2 = roll2
        player.roll = roll1 + roll2
        player.rolled = True

        if player.in_jail:
            if roll1 == roll2:
                player.in_jail = False
                player.location += player.roll

            else:
                player.roll = 0
                return ret

        else:
            if roll1 == roll2:
                if player.extra_turns < 2:
                    player.extra_turns += 1
                    player.extra_turn = True
                else:
                    player.location = 10
                    player.jail_counter = 4
                    player.extra_turns = 0
                    player.x = 70
                    player.y = 770
                    player.extra_turns = 0
                    return [["Go to Jail", "toJail"]]
            else:
                player.extra_turns = 0
            if player.roll + player.location < 40:
                player.location += player.roll
            else:
                player.location = (player.roll + player.location) - 40
                player.wallet += 200

        tile = board.tiles[player.location]
        player.x = tile.x
        player.y = tile.y
        return ret


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
            return [[f"Purchase ${tile.cost}", "purchase"]]
        elif not tile.purchasable and tile.owner != player and not tile.mortgaged:
            '''
            if Property, Railroad or Utility and is owned by another player, and not mortgaged
            command: p
            prompt: To pay $rent to name press p
            function: pay_rent
            '''
            rent = get_rent(tile, player)
            return [[f"Rent Due ${get_rent(tile, player)}", "rent"]]
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
        card = comm_chest[0]
        if not player.inventory is None:
            for item in player.inventory:
                if isinstance(item, Card):
                    card = item
        return [["Play Card", "comChest", card]]

    elif isinstance(tile, CardTile) and tile.name == "Chance":
        '''
        if Chance
        command: p
        prompt: card script press p to play card
        function: play_card
        note: returns card drawn
        '''
        card = chance[0]
        if not player.inventory is None:
            for item in player.inventory:
                if isinstance(item, Card):
                    card = item
        return [["Play Card", "chance", card]]
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
        player.x = 70
        player.y = 770
        return [["Go to Jail", "toJail"]]
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
        if tile.name == "Income tax":
            player_net_worth = player.wallet
            for item in player.inventory:
                if isinstance(item, (Property, RailRoad, Utility)):
                    player_net_worth += item.cost
                    if isinstance(tile, Property):
                        player_net_worth += tile.house_cost * tile.house_count
                        player_net_worth += tile.house_cost * tile.hotel_count
                else:
                    player_net_worth += 50
            player_net_worth = player_net_worth // 10
            if player_net_worth > 200:
                return [["Pay $200 Tax", "tax"]]
            else:
                return [[f"Pay ${player_net_worth} Tax", "tax"]]
        else:
            return [["pay $75 Tax", "tax"]]

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
            if player.jail_counter > 0 or not player.rolled:
                player.jail_counter -= 1
                for item in player.inventory:
                    if isinstance(item, (CommunityChest, Chance)):
                        if "Get out of Jail" in item.message:
                            return [["Use card (optional)", "jail_card_optional"]]
                return [["$50 bail (optional)", "pay_bail_optional"]]
            else:
                for item in player.inventory:
                    if isinstance(item, (CommunityChest, Chance)):
                        if "Get out of Jail" in item.message:
                            return [["Use card (required)", "jail_card_required"]]
                return [["$50 bail (required)", "pay_bail_required"]]
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


def pick_card(command, comm_chest: List[CommunityChest], chance: List[Chance]):
    if command == "chance":
        card = chance.pop()
        if card.action != "special":
            chance.insert(0, card)
        return card
    else:
        card = comm_chest.pop()
        if card.action != "special":
            chance.insert(0, card)
        return card


def play_card(player: Player, card: (CommunityChest, Chance), player_list: List[Player], tile_list: List[Tile], indexList: List[List[int]], command, comm_chest: List[CommunityChest], chance: List[Chance]):
    """
    Play Card  - After this call whatever functionality of a community chest or chance card will be executed
    :param player: Player playing card
    :param card: the actual card from the deck to be executed
    :param player_list: all the players that is on the board
    :param tile_list: all the tiles that is on the board
    :param indexList: the list contains all the tile locations on the board
    :return: list[int]: the coordinates on the board for update location
    """
    # initialize values
    value_list = []
    small_value = 10000
    card = pick_card(command, comm_chest, chance)
    card.value = card.value.rstrip('\n')
    instr = ""
    if ";" in card.value:
        value_list = card.value.split(";")
    value_list = [int(i) for i in value_list]

    if card.action == "move_to":
        cardTileIndex = player.location
        if int(card.value) != 0 and player.location > int(card.value):
            player.wallet += 200
            print("You have passed the go, collect $200 as reward")
        player.location = int(card.value)
        if tile_list[player.location].purchasable:
            card.cost = tile_list[player.location].cost
            tile_list[cardTileIndex].cost = tile_list[player.location].cost
        if not tile_list[player.location].purchasable and isinstance(tile_list[player.location], Property):
            if not tile_list[player.location].owner is None:
                tile_list[cardTileIndex].rent = tile_list[player.location].rent
                tile_list[cardTileIndex].rent_1 = tile_list[player.location].rent_1
                tile_list[cardTileIndex].rent_2 = tile_list[player.location].rent_2
                tile_list[cardTileIndex].rent_3 = tile_list[player.location].rent_3
                tile_list[cardTileIndex].rent_4 = tile_list[player.location].rent_4
                tile_list[cardTileIndex].rent_5 = tile_list[player.location].rent_5
        instr = lands_on(tile_list[player.location], player, comm_chest, chance)
        return indexList[player.location], card, instr
    elif card.action == "move_to_closest":
        cardTileIndex = player.location
        smallest = int(value_list[0])
        for i in value_list:
            if player.location - int(i) < small_value:
                smallest = int(i)
                small_value = player.location - int(i)
            elif player.location - int(i) == small_value:
                choice = random.randint(0, len(value_list))
                smallest = int(value_list[choice])
        player.location = smallest
        if tile_list[player.location].purchasable:
            card.cost = tile_list[player.location].cost
            tile_list[cardTileIndex].cost = tile_list[player.location].cost
        if not tile_list[player.location].purchasable and isinstance(tile_list[player.location], Property):
            if not tile_list[player.location].owner is None:
                tile_list[cardTileIndex].rent = tile_list[player.location].rent
                tile_list[cardTileIndex].rent_1 = tile_list[player.location].rent_1
                tile_list[cardTileIndex].rent_2 = tile_list[player.location].rent_2
                tile_list[cardTileIndex].rent_3 = tile_list[player.location].rent_3
                tile_list[cardTileIndex].rent_4 = tile_list[player.location].rent_4
                tile_list[cardTileIndex].rent_5 = tile_list[player.location].rent_5
        instr = lands_on(tile_list[player.location], player, comm_chest, chance)
        return indexList[player.location], card, instr
    elif card.action == "Finance":
        player.wallet += int(card.value)
        return [-1, -1], card, instr
    elif card.action == "Finance_1":
        if player.wallet + int(card.value) < 0:
            return [-1, -1], card, instr
        else:
            player.wallet += int(card.value)
        if int(card.value) < 0:
            return [-1, -1], card, instr
        else:
            return [-1, -1], card, instr
    elif card.action == "finance":
        if player.wallet + int(card.value) < 0:
            return [-1, -1], card, instr
        else:
            player.wallet += int(card.value)
        if int(card.value) < 0:
            return [-1, -1], card, instr
        else:
            return [-1, -1], card, instr
    elif card.action == "finance_player":
        if player.wallet + int(card.value) * (len(player_list) - 1) < 0:
            return [-1, -1], card, instr
        else:
            player.wallet -= int(card.value) * (len(player_list) - 1)
            for p in player_list:
                if p.name != player.name:
                    p.wallet -= int(card.value)
            return [-1, -1], card, instr
    elif card.action == "Finance_house":
        houses = 0
        hotels = 0
        for i in player.inventory:
            if isinstance(i, Property):
                houses += i.house_count
                hotels += i.hotel_count
        if player.wallet < (25 * houses + 50 * hotels):
            return [-1, -1], card, instr
        else:
            player.wallet -= (25 * houses + 50 * hotels)
            return [-1, -1], card, instr
    elif card.action == "move_steps":
        cardTileIndex = player.location
        player.location -= abs(int(card.value))
        if tile_list[player.location].purchasable:
            card.cost = tile_list[player.location].cost
            tile_list[cardTileIndex].cost = tile_list[player.location].cost
        if not tile_list[player.location].purchasable and isinstance(tile_list[player.location], Property):
            if not tile_list[player.location].owner is None:
                tile_list[cardTileIndex].rent = tile_list[player.location].rent
                tile_list[cardTileIndex].rent_1 = tile_list[player.location].rent_1
                tile_list[cardTileIndex].rent_2 = tile_list[player.location].rent_2
                tile_list[cardTileIndex].rent_3 = tile_list[player.location].rent_3
                tile_list[cardTileIndex].rent_4 = tile_list[player.location].rent_4
                tile_list[cardTileIndex].rent_5 = tile_list[player.location].rent_5
        instr = lands_on(tile_list[player.location], player, comm_chest, chance)
        return indexList[player.location], card, instr
    elif card.action == "special":
        player.inventory.append(card)
        return [-1, -1], card, instr
    return [-1, -1], card, instr


def use_jail_card(player: Player, tile: Tile, comm_chest: List[CommunityChest], chance: List[Chance]):
    """
    Use Jail Card  - After this call a player will be freed from jail if they have a get out of jail free card
    in their inventory and the card will be returned to the appropriate deck
    :param player: Player object using card
    :param tile: the Tile the player is on (should be the jail)
    :param comm_chest: deck to insert card into
    :param chance: deck to insert card into
    :return: str: confirmation of card played
    """
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
    player.x = tile.x
    return "You used your Get out of jail free card"


def pay_bail(player: Player, tile: Tile):
    """
    Pay Bail  - After this call a player will be removed from Jail, their jail counter reset, wallet balance
    adjusted by 50
    :param player: Player object paying bail
    :param tile: the Tile the Player is on (should be the jail tile)
    :return: str: confirmation of payment or notification of insufficient funds
    """
    if player.wallet < 50:
        if player.jail_counter == 0:
            return True
        else:
            return "Insufficient Funds"
    else:
        player.wallet -= 50
        player.in_jail = False
        player.x = tile.x
        player.y = tile.y
        return


def jail_roll(tile: Tile, player: Player, comm_chest: List[CommunityChest], chance: List[Chance]):
    """
    Jail Roll - After this call a player will either be freed from jail by rolling doubles and then advanced to
    the tile according to their roll or remain in jail with their roll counter being incremented
    :param tile: tile: Jail Tile
    :param player: Player object for player in Jail
    :param comm_chest: used to call the lands on function - passed through
    :param chance: used to call the lands on function - passed through
    :return: str: notification of release or further detainment
    """
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
        return "You did not get out of Jail"


def get_rent(tile: (Property, RailRoad, Utility, CardTile), player: Player):
    """
    Get Rent  - After this call the rent value of Property, Railroad and Utility will be calculated
    :param tile: tile: Tile object to calculate rent on
    :param player: Player object paying rent(to get dice roll for Utility)
    :return: int: calculated rent
    """
    rent = 0
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
    elif isinstance(tile, CardTile):
        rent = [tile.rent, tile.rent_1, tile.rent_2, tile.rent_3, tile.rent_4]
        if tile.hotel_count < 1:
            return rent[tile.house_count]
        else:
            return tile.rent_5
    return rent


def pay_rent(player: Player, tile: (Property, RailRoad, Utility)) -> bool:
    """
    Pay Rent - After this call if a player has sufficient funds the owed rent will be deducted from their wallet
    :param player: Player paying the rent
    :param tile: Tile object rent is to be paid on
    :return: str: str of payment confirmation or insufficient funds
    """
    rent = get_rent(tile, player)
    if player.wallet < rent:
        return True
    else:
        player.wallet -= rent
        tile.owner.wallet += rent
        return False


def pay_tax(player: Player, tile: Tax) -> bool:
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
                if not tile.mortgaged:
                    player_net_worth += item.cost
                    player_net_worth += tile.house_cost * tile.house_count
                    player_net_worth += tile.house_cost * tile.hotel_count
            elif isinstance(item, Card):
                player_net_worth += 50
        player_net_worth = player_net_worth // 10
        if player_net_worth > 200:
            if player.wallet < 200:
                return True
            else:
                player.wallet -= 200
                return False
        else:
            if player.wallet < player_net_worth:
                return True
            else:
                player.wallet -= player_net_worth
                return False
    else:
        if player.wallet < 75:
            return True
        else:
            player.wallet -= 75
            return False


def change_player(board: Board):
    """
    Change Player - After this call the current board player will change to the next player
    :param board: Board object of current game
    :return: nothing
    """
    board.current_player = (board.current_player + 1) % len(board.players)


def machine_algo(player: Player, board: Board, cc, chance):
    """
    Machine Algo - After this call the machine player will return a choice based on available options passed in
    :param options: a Dict of available choices
    :param player: Player object of machine player
    :return: str: choice made by machine
    """
    # TODO: Implement a Real Machine Player ALGO
    BoardLocationIndex = [[780, 800], [700, 800], [630, 800], [560, 800], [490, 800], [420, 800], [350, 800],
                          [280, 800], [210, 800],
                          [140, 800], [70, 825], [30, 700], [30, 630], [30, 560], [30, 490], [30, 420], [30, 350],
                          [30, 280],
                          [30, 210], [30, 140], [50, 40], [140, 30], [210, 30], [280, 30], [350, 30], [420, 30],
                          [490, 30], [560, 30], [630, 30], [700, 30], [780, 40], [800, 140], [800, 210], [800, 280],
                          [800, 350], [800, 420], [800, 490], [800, 560], [800, 630], [800, 700]]

    if not player.picked:
        player.image = board.pieces[0]
        player.picked = True
    roll_dice(player, board)
    tile = board.tiles[player.location]
    instr = lands_on(tile, player, cc, chance)
    if len(instr) == 1:
        choice = instr[0][1]
        if choice == "purchase" and player.wallet >= tile.cost:
            purchase(player, tile)
        if choice == "rent":
            bankrupt = pay_rent(player, board.tiles[player.location])
            if bankrupt:
                go_bankrupt(player, cc, chance)
        if choice == "tax":
            bankrupt = pay_tax(player, board.tiles[player.location])
            if bankrupt:
                go_bankrupt(player, cc, chance)
        if len(buildable(player)) > 0:
            build(buildable(player)[random.randint(0, len(buildable(player))-1)], player)
        if choice == "comChest":
            play_card(player, instr[0][2], board.players, board.tiles, BoardLocationIndex, "comchest", cc, chance)
        if choice == "chance":
            play_card(player, instr[0][2], board.players, board.tiles, BoardLocationIndex, "chance", cc, chance)
        if choice == "jail_card_optional" or choice == "jail_card_required":
            use_jail_card(player, board.tiles[player.location], chance, cc)
        if choice == 'pay_bail_optional' or choice == 'pay_bail_required':
            bankrupt = pay_bail(player, board.tiles[player.location])
            if bankrupt:
                go_bankrupt(player, cc, chance)

    change_player(board)
    player.rolled = False



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


def go_bankrupt(player: Player, comm_chest: List[CommunityChest], chance: List[Chance]):
    """
    Go Bankrupt - After this call a players inventory will be returned to its original state
    :param player: Player object going bankrupt
    :param comm_chest: Community Chest deck to return cards to if in player possession
    :param chance: Chance deck to return cards to if in player possession
    :return: str: information about action performed.
    """
    for item in player.inventory:
        if isinstance(item, Card):
            if isinstance(item, Chance):
                chance.insert(0, item)
            else:
                comm_chest.insert(0, item)
        else:
            item.owner = None
            if isinstance(item, property):
                item.mortgaged = False
                item.house_count = 0
                item.hotel_count = 0
    return "You have gone bankrupt and are out of the game"


def build(tile: Property, player: Player):
    """
    Build - After this call a house or hotel will be added to a tile if a player can afford it and
    it is a legal game action
    :param tile: tile object to be acted on
    :param player: Player object making call
    :return: str: information about action performed.
    """

    if tile.house_count < 4 and player.wallet >= tile.house_cost:
        tile.house_count += 1
        player.wallet -= tile.house_cost
    elif tile.house_count == 4 and tile.hotel_count < 1 and player.wallet >= tile.house_cost:
        tile.hotel_count += 1
        player.wallet -= tile.house_cost

def demolish(tile: Property, player: Player):
    """
    Demolish - After this call a house or hotel will be removed from a tile if it is a legal game action
    :param tile: tile object to be acted on
    :param player: Player object making call
    :return: str: information about action performed.
    """
    if tile.hotel_count > 0:
        tile.hotel_count -= 1
        player.wallet += tile.house_cost
    elif tile.house_count > 0:
        tile.house_count -= 1
        player.wallet += tile.house_cost


def create_player(name: str, token: str, board: Board,  x: int, y: int, img: str, machine: bool = False):
    """
    Create Player - After this call a player object will be created and added to the game board
    :param name: str for player name
    :param token: str of player token(hat, car, etc.)
    :param board: Board object to add player on
    :param machine: bool indicating if player is a machine player
    :return: nothing
    """
    player = Player(name=name, machine_player=machine, piece=token, location=0, wallet=1500,
                    inventory=[], roll=0, in_jail=False, jail_counter=0, extra_turns=0,
                    extra_turn=False, x=x, y=y, image=None, rolled=False, picked=False, trade_offered=False,
                    roll_1=0, roll_2=0)
    board.players.append(player)


def show_props(list) -> str:
    """
    Show Props - After this call the caller will be returned an indexed list of the players current inventory
    of tiles
    :param player: Player object seeking inventory
    :return: string of current properties in an indexed list
    """
    count = 0
    ret_str = "Current Inventory\n"
    for tile in list:  # Display Player Inventory
        if isinstance(tile, Property):
            ret_str += f"{count} - Property: {tile.name} Mortgaged: {tile.mortgaged} Mortgage Value: {tile.mortgage}" \
                       f" Houses: {tile.house_count} Hotels: {tile.hotel_count} Color: {tile.color}\n"
            count += 1
        elif isinstance(tile, (RailRoad, Utility)):
            ret_str += f"{count} - Property: {tile.name} Mortgaged: {tile.mortgaged} " \
                       f"Mortgage Value: {tile.mortgage}\n"
    if ret_str == "Current Inventory\n":
        return "Current Inventory is Empty"
    else:
        return ret_str


def buildable(player: Player):
    """
        buildable - checks a machine player's inventory for properties that can be built on
        :param player: the machine Player object being checked
        :return can_built: a list of properties that can be built on
        """
    can_build = []
    tiles = {}
    for tile in player.inventory:
        if isinstance(tile, Card):
            pass
        else:
            tiles[tile.color] = []
    for tile in player.inventory:
        if isinstance(tile, Card):
            pass
        else:
            tiles[tile.color].append(tile)
    for color, props in tiles.items():
        if (color == "blue" or color == "brown" or color == "purple") and len(tiles[color]) == 2:
            for t in tiles[color]:
                can_build.append(t)
        elif len(tiles[color]) == 3:
            for t in tiles[color]:
                can_build.append(t)
    return can_build

