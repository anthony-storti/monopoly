from Game import *

board = Board()
board.create_board()
tiles = board.get_tiles()
for tile in tiles:
    print(tile.get_name())
