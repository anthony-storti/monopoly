from Model import *
import csv
import pickle

board = Board(tiles=list(), current_player=0, players=list(), cards=list(), roll=0)
with open('monopoly_squares.csv') as csv_data_file:
    csv_reader = csv.reader(csv_data_file)
    next(csv_reader, None)
    for row in csv_reader:
        if row[1] == "Property":
            tile = Property(purchasable=True, owner=None, mortgaged=False, name=row[2], color=row[5],
                            cost=int(row[6]), house_cost=int(row[7]), rent=int(row[8]), rent_1=int(row[9]),
                            rent_2=int(row[10]), rent_3=int(row[11]), rent_4=int(row[12]), rent_5=int(row[13]),
                            mortgage=int(row[14]), house_count=0, hotel_count=0)
            board.tiles.append(tile)
        elif row[1] == "Card":
            tile = Card(name=row[2], purchasable=False, action=row[2], color=row[5])
            board.tiles.append(tile)
        elif row[1] == "Go":
            tile = Go(purchasable=False, name=row[2], action=row[3], value=int(row[4]), color=row[5])
            board.tiles.append(tile)
        elif row[1] == "Tax":
            tile = Tax(purchasable=False, name=row[2], action=row[3], value=int(row[4]), color=row[5])
            board.tiles.append(tile)
        elif row[1] == "Jail":
            tile = Jail(purchasable=False, name=row[2], action=row[3], color=row[5])
            board.tiles.append(tile)
        elif row[1] == "Train":
            tile = RailRoad(purchasable=True, name=row[2], color=row[5], cost=int(row[6]), mortgage=int(row[14]),
                            owner=None)
            board.tiles.append(tile)
        elif row[1] == "Utility":
            tile = RailRoad(purchasable=True, name=row[2], color=row[5], cost=int(row[6]), mortgage=int(row[14]),
                            owner=None)
            board.tiles.append(tile)
        elif row[1] == "Free Parking":
            tile = FreeParking(purchasable=False, name=row[2], color=row[5], action=row[3])
            board.tiles.append(tile)
        elif row[1] == "Go to jail":
            tile = GoToJail(purchasable=False, name=row[2], color=row[5], action=row[3], value=int(row[4]))
            board.tiles.append(tile)

file_name = "board.pkl"

open_file = open(file_name, "wb")
pickle.dump(board, open_file)
open_file.close()

open_file = open(file_name, "rb")
loaded_list = pickle.load(open_file)
open_file.close()

print(loaded_list)