from Controller import *
from Model import Player

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
player_1 = Player(name="Anthony", machine_player=False, piece="hat", location=0, wallet=1500,
                  inventory=list(), roll=0, in_jail=False, jail_counter=0, extra_turns=0)
player_2 = Player(name="Machine", machine_player=True, piece="hat", location=0, wallet=1500,
                  inventory=list(), roll=0, in_jail=False, jail_counter=0, extra_turns=0)
add_player(player_1, board)
add_player(player_2, board)


game_on = True
while game_on:
    ''' Game Loop'''
    print("\n")
    instr = {}
    ''' 
    The instructions dictionary maps commands to a list of user prompts and function calls
    This is what will be used to prompt a user for action on their turn
    We always add the option to build or mortgage on every turn, except jail but that hasn't been implemented yet
    '''
    instr["m"] = ["To Mortgage/Restore available Properties press m", mortgage]
    instr["b"] = ["To Build on available Properties press b", build]
    player = board.players[board.current_player]  # current player
    valid_input = False
    while not valid_input:
        '''ROLL VALIDATION LOOP'''
        if player.machine_player:  # if machine player auto-roll
            roll_dice(player)
            valid_input = True
        else:  # repeat loop until user enters r
            val = input(player.name + " Press r to Roll: ")
            if val == "r":
                valid_input = True
                roll_dice(player)
    tile = board.tiles[player.location]  # current tile
    print(f"{player.name} rolled {player.roll} and advanced to {tile.name}")  # displays current tile
    print(f"{player.name}\'s Bank Balance: {player.wallet}")  # displays current wallet value
    opt = lands_on(tile, player, comm_chest, chance)  # call lands on function
    if len(opt) > 0:  # check to see if lands on returned a prompt, if yes add it to instr
        instr[opt[0]] = opt[1]
    instr["q"] = ["To end turn press q"]  # add quit turn prompt to instr
    turn = True
    while turn:
        '''PLAYER PROMPT LOOP'''
        for values in instr.values():  # print all available prompts from instr
            print(values[0])
        valid_input = False
        while not valid_input:
            '''PLAYER INPUT VALIDATION LOOP'''
            if player.machine_player:  # if player is a machine call function to return prompt
                usr_in = machine_algo(instr, player)
            else:
                usr_in = input("Make Selection: ")
            if usr_in in instr:
                if usr_in == "m" or usr_in == "b":  # Mortgage of Build
                    if len(player.inventory) > 0:
                        print("Current Inventory")
                        count = 0
                        for tile in player.inventory:  # Display Player Inventory
                            if isinstance(tile, Property):
                                print(f"{count} - Property: {tile.name} Mortgaged: {tile.mortgaged} "
                                      f"Mortgage Value: {tile.mortgage}  Houses: {tile.house_count} "
                                      f"Hotels: {tile.hotel_count}")
                                count += 1
                            elif isinstance(tile, (RailRoad, Utility)):
                                print(f"{count} - Property: {tile.name} Mortgaged: {tile.mortgaged} "
                                      f"Mortgage Value: {tile.mortgage}")
                        prop = int(input("Select Property: "))
                        print(instr[usr_in][1](player.inventory[prop],
                                               player))  # call the function for mortgage and build
                    else:
                        print("Current Inventory Empty")
                    valid_input = True
                elif usr_in == "p" and len(opt) > 2:  # Play Card
                    print(instr[usr_in][1](player, opt[3]))
                    instr.pop(usr_in)
                    valid_input = True
                elif usr_in == "r":
                    if instr[usr_in][1](tile, player, comm_chest, chance) == "You got out of jail":
                        tile = board[player.location]
                        lst = lands_on(tile, player, comm_chest, chance)
                        instr[lst[0]] = lst[1]
                    instr.pop(usr_in)
                    valid_input = True
                elif usr_in == "p" or usr_in == "a":         # Purchase Tile or Pay Rent
                    ret_val = instr[usr_in][1](player, tile)
                    if ret_val != "insufficient funds":
                        instr.pop(usr_in)  # remove instruction if rent payed or tile purchased
                    print(ret_val)
                    valid_input = True
                elif usr_in == "q" and ("p" in instr or "u" in instr):  # Prohibit quitting turn without playing card or paying rent
                    valid_input = True
                    print(instr["p"][0] + "*is not optional*")
                elif usr_in == "q":     # Quit Turn
                    valid_input = True
                    turn = False
            else:
                print("invalid input")
    change_player(board)
