from Controller import *


class Game:
    def __init__(self, game):
        self.board = game[0]
        self.comm_chest = game[1]
        self.chance = game[2]
        self.ready = False
        self.connected = False
        create_player('player 1', 'Dog', self.board, 770, 825, "", False)
        create_player('player 2', 'Car', self.board, 770, 800, "", False)

    def process(self, player: int, call):
        p = self.board.players[player]
        assert isinstance(p, Player)
        tile = self.board.tiles[p.location]

        if str(call[0]) == "roll":
            return roll_dice(self.board.players[player], self.board)
        elif str(call[0]) == "end_turn":
            self.board.players[player].rolled = False
            change_player(self.board)
        elif str(call[0]) == "purchase":
            return purchase(p, tile)
        elif str(call[0]) == "mortgage":
            return mortgage(p.inventory[call[1]], p, call[1])
        elif str(call[0]) == "choose_token":
            p.image = str(call[1])
            p.picked = True
            self.board.pieces.remove(str(call[1]))
        else:
            pass
