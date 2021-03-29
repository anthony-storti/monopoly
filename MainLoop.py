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
            for prompt, value in opt.items():
                valid_input = False
                while not valid_input:
                    usr_in = input(prompt)
                    if usr_in == "":
                        valid_input = True
                    elif usr_in == value[0]:
                        print(value[1])
                        valid_input = True
                    else:
                        print(f"invalid input:")
        change_player(board)
