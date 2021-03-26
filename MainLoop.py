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
for card in chance:
    print(card)

'''    
while game_on:
    val = input(board.players[board.current_player].name + " Press R to Roll: ")
    if val == "r":
        roll_dice(board)
    print(board.tiles[board.roll].name)
    val = input("press q to quit or e to end turn")
    if val == "q":
        game_on = False
'''