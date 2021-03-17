from Game import *

board = Board()
board.create_board()
player1 = Player("anthony", False, board, "hat")
board.add_player(player1)
count = 0
while count < 15:
    board.roll_dice()
    print(board.get_tiles()[player1.get_location()].get_name())
    count += 1