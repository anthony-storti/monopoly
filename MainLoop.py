from Controller import *
from Model import Tile, Property, Card, Player, Board


game = load_game()
board = game[0]
comm_chest = game[1]
chance = game[2]


player_1 = Player(name="Anthony", machine_player=False, board=board, piece="hat", location=0, wallet=1500, inventory=list())
player_2 = Player(name="Monopolizer 3000", machine_player=True, board=board, piece="hat", location=0, wallet=1500, inventory=list())

add_player(player_1, board)
add_player(player_2, board)
game_on = True

while game_on:
    print("\n")
    instr = {}
    instr["m"] = ["To Mortgage available Properties press M", mortgage()]
    instr["b"] = ["To Build on available Properties press B", build()]
    instr["q"] = ["To end turn press Q"]
    player = board.players[board.current_player]
    valid_input = False
    while not valid_input:
        val = input(player.name + " Press R to Roll: ")
        if val == "r":
            valid_input = True
            roll_dice(board, player)
            tile = board.tiles[player.location]

            print(f"{player.name} rolled {board.roll} and advanced to {tile.name}")
            print(f"{player.name}\'s Bank Balance: {player.wallet}")

            opt = lands_on(tile, player, comm_chest, chance)
            if len(opt) > 0:
                instr[opt[0]] = opt[1]
            turn = True
            while turn:
                for vals in instr.values():
                    print(vals[0])
                valid_input = False
                while not valid_input:
                    usr_in = input("Make Selection: ")
                    if usr_in == "m" or usr_in == "b":
                        print(instr[usr_in][1])
                        valid_input = True
                    elif usr_in == "p" and len(opt) > 2:
                        instr[usr_in][1](player, opt[3])
                        instr.pop(usr_in)
                        valid_input = True
                    elif usr_in == "p":
                        instr[usr_in][1](player, tile)
                        instr.pop(usr_in)
                        valid_input = True
                    elif usr_in == "q":
                        valid_input = True
                        turn = False
                    else:
                        print(f"invalid input:")
    change_player(board)
