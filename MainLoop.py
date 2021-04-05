from Controller import *
from Model import Player


def main():
    game = load_game()    # gets the tuple we pickled
    board = game[0]       # gets board from tuple
    comm_chest = game[1]  # gets shuffled deck of community chest cards
    chance = game[2]      # gets shuffled deck of chance cards

    # TODO: Validate user input in below code block
    '''
    tokens = ["1: ship", "2: thimble", "3: hat", "4: car", "5: iron", "6. boot", "7: Dog", "8: wheel barrel"]
    num_players = int(input("enter number of human players: "))
    while num_players > 0:
        name = input("Enter Player Name: ")
        print(tokens)
        token = int(input('select token number:'))
        create_player(name, tokens[token - 1], board)
        tokens.remove(tokens[token - 1])
        num_players -= 1
    '''

    ''' The Player Init below is deprecated and we will delete later on but for now we don't want to manually create
    a new player every time we test mainloop, in the future we will use the above code to initialize players'''
    player_1 = Player(name="Anthony", machine_player=True, piece="hat", location=0, wallet=1500,
                      inventory=list(), roll=0, in_jail=False, jail_counter=0, extra_turns=0, extra_turn=False)
    player_2 = Player(name="Machine", machine_player=True, piece="hat", location=0, wallet=1500,
                      inventory=list(), roll=0, in_jail=False, jail_counter=0, extra_turns=0, extra_turn=False)
    add_player(player_1, board)
    add_player(player_2, board)

    while len(board.players) > 1:
        ''' Game Loop'''
        print("\n")
        instr = {}
        ''' 
        The instructions dictionary maps commands to a list of user prompts and function calls
        This is what will be used to prompt a user for action on their turn
        We always add the option to build or mortgage on every turn, except jail but that hasn't been implemented yet
        '''
        instr["m"] = ["To Mortgage/Restore available Properties press -m-", mortgage]
        instr["s"] = ["To show current inventory press -s-", show_props]
        player = board.players[board.current_player]  # current player
        valid_input = False
        if not player.in_jail:
            while not valid_input:
                '''ROLL VALIDATION LOOP'''
                if player.machine_player:  # if machine player auto-roll
                    roll_dice(player)
                    valid_input = True
                else:  # repeat loop until user enters r
                    val = input(player.name + " Press -r- to Roll: ")
                    if val == "r":
                        valid_input = True
                        roll_dice(player)
        tile = board.tiles[player.location]  # current tile
        if player.in_jail:
            print(f"{player.name} is in Jail")
        else:
            print(f"{player.name} rolled {player.roll} and advanced to {tile.name}")  # displays current tile
        if player.extra_turn:
            print(f"{player.name} Rolled Double {player.roll/2}'s You Get an extra turn")
        opt = lands_on(tile, player, comm_chest, chance)  # call lands on function
        if len(opt) == 2:  # check to see if lands on returned a prompt, if yes add it to instr
            instr[opt[0]] = opt[1]
        if len(opt) == 4:
            instr[opt[0]] = opt[1]
            instr[opt[2]] = opt[3]
        # TODO: add ability to take two commands from lands on
        instr["q"] = ["To end turn press -q-"]  # add quit turn prompt to instr
        turn = True
        while turn:
            '''PLAYER PROMPT LOOP'''
            if len(buildable(player)) > 0:
                instr["b"] = ["To Build on available Properties press -b-", build]
            print(f"Account Balance: {player.wallet}")  # displays current wallet value
            print("OPTIONS:")
            for values in instr.values():  # print all available prompts from instr
                print(f"-{values[0]}")
            valid_input = False
            while not valid_input:
                '''PLAYER INPUT VALIDATION LOOP'''
                if player.machine_player:  # if player is a machine call function to return prompt
                    usr_in = machine_algo(instr, player, tile, buildable(player))
                else:
                    usr_in = input("Make Selection: ")
                if usr_in in instr:
                    print(usr_in)
                    if usr_in == "m":  # Mortgage of Build
                        prop_list = show_props(player.inventory)
                        print(prop_list)
                        if prop_list != "Current Inventory is Empty":
                            valid_prop = False
                            prop = ""
                            while not valid_prop:
                                prop = input("Select Property or press -e- to escape: ")
                                if prop.isdigit() and int(prop) <= len(player.inventory) - 1:
                                    valid_prop = True
                                elif prop == "e":
                                    valid_prop = True
                                else:
                                    print(f"Enter property from 0 to {len(player.inventory) - 1} or e to escape")
                            if prop != "e":
                                if int(prop) <= len(player.inventory):
                                    print(instr[usr_in][1](player.inventory[int(prop)],
                                                           player))  # call the function for mortgage and build
                        valid_input = True
                    if usr_in == "b":  # Mortgage of Build
                        build_list = buildable(player)
                        print(show_props(build_list))
                        prop = ""
                        if player.machine_player:
                            print(instr[usr_in][1](build_list[0], player))
                        else:
                            valid_build = False
                            while not valid_build:
                                prop = input("Select Property or press -e- to escape: ")
                                if prop.isdigit() and int(prop) <= len(build_list) - 1:
                                    valid_build = True
                                elif prop == "e":
                                    valid_build = True
                                else:
                                    print(f"Enter property from 0 to {len(build_list) - 1} or e to escape")
                            if prop != "e":
                                if int(prop) <= len(build_list):
                                    print(instr[usr_in][1](build_list,
                                                           player))  # call the function for mortgage and build
                        valid_input = True
                    elif usr_in == "c":  # Play Card
                        ret_val = (instr[usr_in][1](player, instr[usr_in][2], board.players, board.tiles))
                        if "Go Bankrupt" in ret_val:
                            instr["g"] = ["To go bankrupt press -g-", go_bankrupt]
                        print(ret_val)
                        valid_input = True
                        if instr[usr_in][2].action == "move_to" or instr[usr_in][2].action == "move_to_closest" \
                                or instr[usr_in][2].action == "move_steps":
                            tile = board.tiles[player.location]
                            add = lands_on(tile, player, comm_chest, chance)
                            if len(add) > 0:
                                instr[add[0]] = add[1]
                        if ret_val != "insufficient funds":
                            instr.pop(usr_in)
                        valid_input = True
                    elif usr_in == "r":  # Jail roll
                        if instr[usr_in][1](tile, player, comm_chest, chance) == "You got out of jail":
                            tile = board.tiles[player.location]
                            lst = lands_on(tile, player, comm_chest, chance)
                            if len(lst) > 0:
                                instr[lst[0]] = lst[1]
                        instr.pop(usr_in)
                        valid_input = True
                    elif usr_in == "u":
                        print(instr[usr_in][1](player, comm_chest, chance))
                        instr.pop(usr_in)
                        valid_input = True
                    elif usr_in == "s":
                        print(instr[usr_in][1](player.inventory))
                        instr.pop(usr_in)
                        valid_input = True
                    elif usr_in == "p" or usr_in == "a":         # Purchase Tile or Pay Rent
                        ret_val = instr[usr_in][1](player, tile)
                        if "Go Bankrupt" in ret_val:
                            instr["g"] = ["To go bankrupt press -g-", go_bankrupt]
                        elif ret_val != "Insufficient Funds Mortgage Property or Go Bankrupt \n":
                            instr.pop(usr_in)  # remove instruction if rent payed or tile purchased
                        print(ret_val)
                        valid_input = True
                    elif usr_in == "q" and ("p" in instr or "u" in instr or "c" in instr):  # Prohibit quitting turn without playing card or paying rent
                        valid_input = True
                        print(instr[usr_in][0] + "*is not optional*")
                    elif usr_in == "g":     # Go bankrupt
                        valid_input = True
                        print(instr[usr_in][1](player, comm_chest, chance))
                        board.players.remove(player)
                        turn = False
                    elif usr_in == "q":     # Quit Turn
                        valid_input = True
                        turn = False
                else:
                    print("invalid input")
        if not player.extra_turn:
            change_player(board)
        else:
            player.extra_turn = False
    print(f"Game Over, {board.players[0].name} Won. ")


main()
