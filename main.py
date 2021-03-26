from Game import *
from Data_Classes import Tile, Property, Card, Player, Board

board = Board(tiles=list(), current_player=0, players=list(), cards=list(), roll=0)
create_board(board)
player_1 = Player(name="Anthony", machine_player=False, board=board, piece="hat", location=0, wallet=1500, inventory=list())
player_2 = Player(name="Monopolizer 3000", machine_player=True, board=board, piece="hat", location=0, wallet=1500, inventory=list())
add_player(player_1, board)
add_player(player_2, board)
game_on = True
for tile in board.tiles:
    print(tile)
while game_on:
    val = input(board.players[board.current_player].name + " Press R to Roll: ")
    if val == "r":
        roll_dice(board)
    print(board.tiles[board.roll].name)
    val = input("press q to quit or e to end turn")
    if val == "q":
        game_on = False
