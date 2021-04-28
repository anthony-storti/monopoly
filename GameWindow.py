import pygame
from tkinter import *
from Controller import *
import os

pygame.init()
pygame.mixer.init()
pygame.font.init()
s = 'sound/sound'
game = load_game()    # gets the tuple we pickled
board = game[0]       # gets board from tuple
comm_chest = game[1]  # gets shuffled deck of community chest cards
chance = game[2]      # gets shuffled deck of chance cards
create_player('player 1', 'Dog', board, 770, 825, '', False)
create_player('player 2', 'Car', board, 770, 800, '', True)
roll_sound = pygame.mixer.Sound(os.path.join('sounds', 'diceRolling.wav'))
purchase_sound = pygame.mixer.Sound(os.path.join('sounds', 'purchase.wav'))
button_sound = pygame.mixer.Sound(os.path.join('sounds', 'button.wav'))
pygame.mixer.music.load(os.path.join('sounds', 'soundtrack.wav'))


class Popup_Player:
    def __init__(self, master, player: Player):
        self.master = master
        self.done = False
        self.master.geometry("400x200")
        master.title(f"{player.name} Information")
        # self.label = Label(master, text="Select A Property").pack()
        self.label_1 = Label(master, text=f"Wallet: ${player.wallet}").pack()
        self.close_button = Button(master, text="Close", command=master.destroy).pack()
        tiles = {}
        options = []
        for tile in player.inventory:
             tiles[tile.color] = []
        for tile in player.inventory:
            tiles[tile.color].append(tile)
        for color, props in tiles.items():
            self.label = Label(master, text=f"{color}", font='Helvetica 12 bold underline').pack()
            for prop in props:
                self.label = Label(master, text=f"{prop.name}").pack()





class Popup:
    def __init__(self, master, player: Player, build: bool):
        self.master = master
        self.done = False
        self.master.geometry("400x200")
        tile_dict = {}
        master.title("Selector")
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
            tile = player.inventory
            if len(tile) == 0:
                options = ["No Inventory"]
            else:
                tile_dict["Select Property"] = ""
                for prop in tile:
                    assert isinstance(prop, (Property, RailRoad, Utility))
                    if prop.mortgaged:
                        m = f"Unmortgage for ${prop.mortgage}"
                    else:
                        m = f"Mortgage for ${prop.mortgage}"
                    tile_dict[f"{prop.name} | {m}"] = prop
                    options.append(f"{prop.name} | {m}")
                    self.clicked.set(f"{prop.name} | {m}")


        self.label = Label(master, text="Select A Property").pack()
        self.label_1 = Label(master, text=f"Wallet: ${player.wallet}").pack()

        self.drop = OptionMenu(self.master, self.clicked, *options).pack()

        if len(tile_dict) > 1:
            self.select_button = Button(master, text="Select", command=lambda:
                self.execute(tile_dict[self.clicked.get()], player, master)).pack()


        self.close_button = Button(master, text="Close", command=master.destroy).pack()

    def execute(self, tile, player, root):
        if tile == "":
            pass
        else:
            mortgage(tile, player)
            root.destroy()


width = 855
height = 900
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Monopoly")
bg = pygame.image.load("images/bord.jpg")


class button():
    def __init__(self, color, x, y, width, height, text='', call='', player=None):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = (255, 255, 255)
        self.call = call
        self.player = player


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
        # if outline:
            # pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        # pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

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


def redrawWindow(win, player, buttons, tokens, btn):
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

        win.fill((255, 255, 255))
        win.blit(bg, (0, 0))
        for p in btn:
            if p.call == "":
                pass
            else:
                p.draw_tokens(win)
        for b in buttons.values():
            b.draw(win)
    pygame.display.update()


def create_landson_buttons(instr, buttons):
    button_x = 560
    count = 0
    for i in instr:
        buttons[instr[count][1]] = button((0, 0, 0), button_x, 855, 139, 45, instr[count][0], instr[count][1])
        button_x += 140
        count += 1
    return buttons

def create_tokens_buttons():
    tokens = []
    button_x = 260
    button_y = 500
    for token in board.pieces:
        if button_x <= 570:
            tokens.append(button((191, 219, 174), button_x, button_y, 40, 40, token, token))
            button_x += 150
        else:
            button_x = 260
            button_y += 80
            tokens.append(button((191, 219, 174), button_x, button_y, 40, 40, token, token))
            button_x += 150

    return tokens



def main():
    buttons = {"Build": button((0, 0, 0), 140, 855, 139, 45, 'Build', 'build'),
               "Mortgage": button((0, 0, 0), 280, 855, 139, 45, "Mortgage", 'mortgage'),
               "Roll": button((0, 0, 0), 0, 855, 139, 45, "Roll:", 'roll'),
               "End Turn": button((0, 0, 0), 420, 855, 139, 45, "End Turn", 'end_turn')}
    pygame.mixer.music.play()

    player_btn = [button((255, 255, 255), 0, 0, 40, 40), button((255, 255, 255), 0, 0, 40, 40)]
    tokens = []
    run = True
    while run:
        p1 = board.players[board.current_player]
        if not p1.picked:
            tokens = create_tokens_buttons()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                assert isinstance(p1, Player)
                for token in tokens:
                    if token.isOver(pos):
                        pygame.mixer.Sound.play(button_sound)
                        board.players[board.current_player].image = pygame.image.load(token.call)
                        board.pieces.remove(token.call)
                        player_btn[board.current_player] = button((0, 255, 255), p1.x, p1.y, 40, 40, token.call, token.call, p1)
                        board.players[board.current_player].picked = True
                for player_token in player_btn:
                    if player_token.isOver(pos):
                        pygame.mixer.Sound.play(button_sound)
                        root = Tk()
                        my_gui = Popup_Player(root, player_token.player)
                        root.mainloop()
                for b in buttons.values():
                    if b.isOver(pos):
                        if b.call == "build":
                            pygame.mixer.Sound.play(button_sound)
                            root = Tk()
                            my_gui = Popup(root, p1, True)
                            root.mainloop()
                        elif b.call == "rent":
                            pygame.mixer.Sound.play(purchase_sound)
                            pay_rent(p1, board.tiles[p1.location])
                            buttons.pop('rent')
                            break
                        elif b.call == "purchase":
                            pygame.mixer.Sound.play(purchase_sound)
                            purchase(p1, board.tiles[p1.location])
                            buttons.pop("purchase")
                            break
                        elif b.call == "mortgage":
                            pygame.mixer.Sound.play(button_sound)
                            root = Tk()
                            my_gui = Popup(root, p1, False)
                            root.mainloop()
                        elif b.call == "roll":
                            pygame.mixer.Sound.play(roll_sound)
                            roll_dice(p1, board)
                            player_btn[board.current_player].x = board.players[board.current_player].x
                            player_btn[board.current_player].y = board.players[board.current_player].y
                            b.text = f"Roll: {p1.roll}"
                            buttons = create_landson_buttons(lands_on(board.tiles[p1.location], p1, chance, comm_chest), buttons)
                            p1.rolled = True
                            break
                        elif b.call == "end_turn":
                            pygame.mixer.Sound.play(button_sound)
                            if not p1.rolled or "rent" in buttons:
                                pass
                            else:
                                p1.rolled = False
                                change_player(board)
                                buttons = {"Build": button((0, 0, 0), 140, 855, 139, 45, 'Build', 'build'),
                                           "Mortgage": button((0, 0, 0), 280, 855, 139, 45, "Mortgage", 'mortgage'),
                                           "Roll": button((0, 0, 0), 0, 855, 139, 45, "Roll:", 'roll'),
                                           "End Turn": button((0, 0, 0), 420, 855, 139, 45, "End Turn", 'end_turn')}
            if event.type == pygame.MOUSEMOTION:
                for b in buttons.values():
                    if b.isOver(pos):
                        b.color = (0, 255, 0)
                        b.text_color = (0, 0, 0)
                    else:
                        b.color = (0, 0, 0)
                        b.text_color = (255, 255, 255)

        redrawWindow(win, p1, buttons, tokens, player_btn)


main()
