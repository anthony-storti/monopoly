from Controller import *
from Model import Tile, Property, Card, Player, Board


game = load_game()
board = game[0]
comm_chest = game[1]
chance = game[2]

'''
tokens = ["1: ship", "2: thimble", "3: hat", "4: car", "5: iron", "6. boot", "7: Dog", "8: wheel barrel"]
num_players = int(input("enter number of human players: "))
while num_players >= 0:
    name = input("Enter Player Name: ")
    print(tokens)
    token = int(input('select token number:'))
    create_player(name, tokens[token - 1], board)
    tokens.remove(tokens[token - 1])
    num_players -= 1
'''
player_1 = Player(name="Anthony", machine_player=False, piece="hat", location=0, wallet=1500, inventory=list())
player_2 = Player(name="Monopolizer 3000", machine_player=True, piece="hat", location=0, wallet=1500, inventory=list())

add_player(player_1, board)
add_player(player_2, board)


game_on = True

while game_on:
    print("\n")
    instr = {}
    instr["m"] = ["To Mortgage available Properties press m", mortgage()]
    instr["b"] = ["To Build on available Properties press b", build()]
    player = board.players[board.current_player]
    valid_input = False
    while not valid_input:
        val = input(player.name + " Press r to Roll: ")
        if val == "r":
            valid_input = True
            roll_dice(board, player)
            tile = board.tiles[player.location]

            print(f"{player.name} rolled {board.roll} and advanced to {tile.name}")
            print(f"{player.name}\'s Bank Balance: {player.wallet}")

            opt = lands_on(tile, player, comm_chest, chance)
            if len(opt) > 0:
                instr[opt[0]] = opt[1]
            instr["q"] = ["To end turn press q"]
            turn = True
            while turn:
                for vals in instr.values():
                    print(vals[0])
                valid_input = False
                while not valid_input:
                    usr_in = input("Make Selection: ")
                    if usr_in in instr:
                        if usr_in == "m" or usr_in == "b":
                            print(instr[usr_in][1])
                            valid_input = True
                        elif usr_in == "p" and len(opt) > 2:
                            print(instr[usr_in][1](player, opt[3]))
                            instr.pop(usr_in)
                            valid_input = True
                        elif usr_in == "p" or usr_in == "a":
                            print(instr[usr_in][1](player, tile))
                            instr.pop(usr_in)
                            valid_input = True
                        elif usr_in == "q" and "p" in instr:
                            valid_input = True
                            print(opt[0] + "*is not optional*")
                        elif usr_in == "q":
                            valid_input = True
                            turn = False
                    else:
                        print("invalid input")
    change_player(board)
