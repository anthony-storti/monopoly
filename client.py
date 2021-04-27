import pygame
from network import Network
import pickle
import os
import time

from Controller import *
from tkinter import *

pygame.init()
pygame.font.init()
pygame.mixer.init()
width = 855
height = 900
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Monopoly")
bg = pygame.image.load("images/bord.jpg")
pygame.font.init()
pygame.mixer.init()
# butt = pygame.image.load('images/dice.png')
roll_sound = pygame.mixer.Sound(os.path.join('sound', 'diceRolling.wav'))
pygame.mixer.music.load(os.path.join('sound', 'soundtrack.wav'))

class PropertyPopup:
    def __init__(self, master, player: Player, n: Network, build: bool):
        self.master = master
        self.master.geometry("400x200")
        tile_dict = {}
        master.title("Property Selector")
        options = []
        self.clicked = StringVar()
        if build:
            tile = buildable(player)
            if len(tile) == 0:
                options = ["No Buildable Inventory"]
            else:
                tile_dict["Select Property"] = ""
                for prop in tile:
                    assert isinstance(prop, (Property, RailRoad, Utility))
                    tile_dict[prop.name] = prop
                    options.append(prop.name)
        else:
            inv = player.inventory
            if len(inv) == 0:
                options = ["No Inventory"]
            else:
                tile_dict["Select Property"] = ""
                count = 0
                for prop in inv:
                    assert isinstance(prop, (Property, RailRoad, Utility))
                    if not prop.mortgaged:
                        m = f"Mortgage for ${prop.mortgage}"
                    else:
                        m = f"Unmortgage for ${prop.mortgage}"
                    tile_dict[f"{prop.name} | {m}"] = count
                    count += 1
                    options.append(f"{prop.name} | {m}")
                    self.clicked.set(f"{prop.name} | {m}")

        self.label = Label(master, text="Select A Property").pack()
        self.label_1 = Label(master, text=f"Wallet: ${player.wallet}").pack()

        self.drop = OptionMenu(self.master, self.clicked, *options).pack()

        if len(tile_dict) > 1:
            self.select_button = Button(master, text="Select", command=lambda:
                self.execute(tile_dict[self.clicked.get()], player, master, n)).pack()


        self.close_button = Button(master, text="Close", command=master.destroy).pack()

    def execute(self, idx, player, root, n):
        if idx == "":
            pass
        else:
            n.send(["mortgage", idx])
            root.destroy()

class button():
    def __init__(self, color, x, y, width, height, text='', call=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = (255, 255, 255)
        self.call = call

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 25)
            text = font.render(self.text, True, self.text_color)
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def draw_tokens(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            img = pygame.image.load(self.text)
            win.blit(img, (
                self.x + (self.width / 2 - 32 / 2), self.y + (self.height / 2 - 32 / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def create_landson_buttons(instr, buttons):
    button_x = 560
    count = 0
    for i in instr:
        buttons[instr[count][1]] = button((0, 0, 0), button_x, 855, 139, 45, instr[count][0], instr[count][1])
        button_x += 140
        count += 1
    return buttons

def create_tokens_buttons(game, tokens):
    tokens = []
    button_x = 260
    button_y = 500
    for token in game.board.pieces:
        if button_x <= 570:
            tokens.append(button((191, 219, 174), button_x, button_y, 40, 40, token, token))
            button_x += 150
        else:
            button_x = 260
            button_y += 80
            tokens.append(button((191, 219, 174), button_x, button_y, 40, 40, token, token))
            button_x += 150

    return tokens


def redrawWindow(win, game, player, buttons, tokens):
    if not player.picked:
        win.fill((191, 219, 174))
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("2 Player Game", True, (199, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 100))
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Select Token", True, (199, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))

        for t in tokens:
            t.draw_tokens(win)
    else:
        win.fill((0, 0, 0))
        win.blit(bg, (0, 0))
        # win.blit(butt, (200, 200))
        if not game.ready:
            font = pygame.font.SysFont("comicsans", 80)
            text = font.render("Waiting for other players...", True, (255, 0, 0), True)
            win.blit(text, (width/2 - text.get_width()/2, height/2 - text.get_height()/2))
        else:
            for button in buttons.values():
                button.draw(win)
            for player in game.board.players:
                if player.image == "":
                    pass
                else:
                    win.blit(pygame.image.load(player.image), (player.x, player.y))
    pygame.display.update()



buttons_1 = {"build": button((0, 0, 0), 140, 855, 139, 45, 'Build', 'build'),
           "mortgage": button((0, 0, 0), 280, 855, 139, 45, "Mortgage", 'mortgage'),
           "roll": button((0, 0, 0), 0, 855, 139, 45, "Roll:", 'roll'),
           "end_turn": button((0, 0, 0), 420, 855, 139, 45, "End Turn", 'end_turn')}
buttons_2 = {"wait": button((0, 0, 0), 0, 855, 855, 45, '', 'wait')}


def main():
    #################################################################################
    # the network object is what gets and sends data to the server
    # the player is just the int player number given by the server
    #################################################################################
    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.getP())
    print("You are Player", player)
    tokens = []
    pygame.mixer.music.play()
    while run:
        clock.tick(60)
        try:
            game = n.send(["get"])
        except:
            run = False
            print("Couldn't get Game")
            break
        board = game.board
        p = game.board.players[player]
        players = game.board.players
        current_player = game.board.current_player
        if not p.picked:
            tokens = create_tokens_buttons(game, tokens)
        assert isinstance(p, Player)
        if board.current_player == player:
            buttons = buttons_1
        else:
            buttons = buttons_2
            buttons_2['wait'].text = f"waiting for {players[current_player].name} to finish turn"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN:
                for token in tokens:
                    if token.isOver(pos):
                        n.send(['choose_token', token.call])
                if player == current_player:
                        for butn in buttons.values():
                            if butn.isOver(pos):
                                if butn.call == "roll" and not players[player].rolled:
                                    # kinda annoying to have to update all the variables mid loop
                                    pygame.mixer.Sound.play(roll_sound)
                                    n.send([butn.call])
                                    game = n.send(['get'])
                                    board = game.board
                                    players = game.board.players
                                    location = players[player].location
                                    p = game.board.players[player]
                                    current_player = game.board.current_player

                                    butn.text = f"Roll : {p.roll}"
                                    instr = lands_on(board.tiles[location], players[player],
                                                     game.comm_chest, game.chance)
                                    buttons = create_landson_buttons(instr, buttons)
                                elif butn.call == "end_turn":
                                    n.send([butn.call])
                                    if "purchase" in buttons:
                                        buttons.pop("purchase")
                                        buttons["roll"].text = "Roll:"
                                    if "card" in buttons:
                                        buttons.pop("card")
                                    if "tax" in buttons:
                                        buttons.pop("tax")
                                    if "rent" in buttons:
                                        buttons.pop('rent')
                                elif butn.call == "purchase":
                                    print("purchased")
                                    n.send([butn.call])
                                    buttons.pop('purchase')
                                elif butn.call == "mortgage":
                                    root = Tk()
                                    my_gui = PropertyPopup(root, game.board.players[player], n,  False)
                                    root.mainloop()
                                    game = n.send(['get'])
                                else:
                                    n.send([butn.call])
                                break

            if event.type == pygame.MOUSEMOTION:
                for b in buttons.values():
                    if b.isOver(pos):
                        b.color = (0, 255, 0)
                        b.text_color = (0, 0, 0)
                    else:
                        b.color = (0, 0, 0)
                        b.text_color = (255, 255, 255)
        redrawWindow(win, game, p, buttons, tokens)

main()
