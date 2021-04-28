import pygame
from tkinter import *
from Controller import *
import os

##############################
# Pygame Package Initializers
##############################
pygame.init()
pygame.mixer.init()
pygame.font.init()
###############################
# Game Initializers
###############################
game = load_game()    # gets the tuple we pickled
board = game[0]       # gets board from tuple
comm_chest = game[1]  # gets shuffled deck of community chest cards
chance = game[2]      # gets shuffled deck of chance cards
create_player('player 1', 'Dog', board, 770, 825, '', False)
create_player('player 2', 'Car', board, 770, 800, '', True)
###############################
# Sound Initializers
###############################
roll_sound = pygame.mixer.Sound(os.path.join('sounds', 'diceRolling.wav'))
purchase_sound = pygame.mixer.Sound(os.path.join('sounds', 'purchase.wav'))
button_sound = pygame.mixer.Sound(os.path.join('sounds', 'button.wav'))
pygame.mixer.music.load(os.path.join('sounds', 'soundtrack.wav'))
###############################
# Pygame Window Initializers
###############################
width = 855
height = 900
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Monopoly")
bg = pygame.image.load("images/bord.jpg")


class PopupPlayer:

    def __init__(self, master, player: Player):
        """
        Initializer - This will create a tkinter window that pops up displaying player information:
        wallet, properties grouped by color, and whatever else we want to add
        :param master: this is the tkinter tk() root
        :param player: Player object to display information about
        :return: nothing
        """
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


class PopupPropertySelector:

    def __init__(self, master, player: Player, build: bool):
        """
        Initializer - This will create a tkinter window that pops up displaying either properties to be mortgaged/mortgaged
        or properties that can be build on
        :param master: this is the tkinter tk() root
        :param player: Player object for inventory information
        :param build: bool to indicate if purpose of window is to build or mortgage
        :return: nothing
        """
        self.master = master
        self.done = False
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
                                        self.execute(tile_dict[self.clicked.get()], player)).pack()
        self.close_button = Button(master, text="Close", command=master.destroy).pack()

    def execute(self, tile, player):
        """
        execute - This will either do nothing if the tile passed in was an empty string, or it will call mortgage
        on the tile passed in and destroy the tkinter window(this function is needed to call to commands from one
        button push in a tkinter window)
        :param tile: tile object to pass to mortgage
        :param player: Player object to pass to mortgage call
        :return: nothing
        """
        if tile == "":
            pass
        else:
            mortgage(tile, player)
            self.master.destroy()


class Button:
    def __init__(self, color, x, y, width, height, text='', call='', player=None):
        """
        Initializer - This will create a button object that can display text or image.
        :param color: this is a RGB tuple to hold the color of the button
        :param x: this is the x coordinate for the button
        :param y: this is the y coordinate for the button
        :param width: this is the width of the button in pixels
        :param height: this is the height of the button in pixels
        :param text: this is a string of text to display or a file path for an image to display
        :param call: this is to hold a string that references a action to be taken when a button is clicked
        :parma player: this is a player object associated with a button. This is used for buttons that represent
        player tokens on the board
        :return: nothing
        """
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
        """
        draw - This will blit the button to the pygame surface and any text that is passed
        :param win: this is the pygame surface to blit to
        :param outline: default to none. This is for an outline of a button in pixels using ints, the outline will
        increase or decrease the height and width of a button by the supplied int of pixels
        :return: nothing
        """
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 25)
            text = font.render(self.text, True, self.text_color)
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def draw_tokens(self, win):
        """
        draw tokens- This will blit player tokens to a screen, it is similar to draw but used images instead of text
        :param win: this is the pygame surface to blit to
        :return: nothing
        """
        if self.text != '':
            img = pygame.image.load(self.text)
            win.blit(img, (
                self.x + (self.width / 2 - 32 / 2), self.y + (self.height / 2 - 32 / 2)))

    def isOver(self, pos):
        """
        is over - This will tell if a mouse cursor x,y tuple is over a button object
        param: pos: this is a x,y tuple of a mouse cursor position
        :return: bool, indicating if pos is over button
        """
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False


def redrawWindow(win, player, buttons, tokens, btn):
    """
    redraw window- This will display everything that is shown on the pygame surface
    :param win: the pygame surface to display to
    :param player: player object current game player
    :param buttons: a list of buttons that hold the current instructions for the game
    :param tokens: a list of tokens available for a user to choose from
    :param btn: a list of button objects that represent a player
    :return: nothing
    """
    if not player.picked:
        ######################################################################
        # this is the initial display screen prompting a user to pick a token
        ######################################################################
        win.fill((191, 219, 174))
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("You V. Machine", True, (199, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 100))
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Select Token", True, (199, 0, 0))
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        for t in tokens:
            t.draw_tokens(win)
    else:
        ######################################################################
        # this is the main game loop display window
        ######################################################################
        win.fill((255, 255, 255))
        win.blit(bg, (0, 0))
        for p in btn:
            if p.call == "":
                pass
            else:
                p.draw_tokens(win)
        for b in buttons.values():
            b.draw(win)
    pygame.display.update()  # this must be called no matter what


def create_landson_buttons(instr, buttons):
    """
    create lands on buttons- This call will generate a dict of buttons that represent the instructions available to
    a player on their given turn
    :param instr: the list returned from calling lands_on()
    :param buttons: a dict of buttons that already contain the instructions for roll, build, mortgage
    :return: a dict of buttons
    """
    button_x = 560
    count = 0
    for i in instr:
        buttons[instr[count][1]] = Button((0, 0, 0), button_x, 855, 139, 45, instr[count][0], instr[count][1])
        button_x += 140
        count += 1
    return buttons

def create_tokens_buttons():
    """
    create tokens buttons- This call will generate a list of buttons that represent all the tokens a player can choose
    :return: a list of buttons
    """
    tokens = []
    button_x = 260
    button_y = 500
    for token in board.pieces:
        if button_x <= 570:
            tokens.append(Button((191, 219, 174), button_x, button_y, 40, 40, token, token))
            button_x += 150
        else:
            button_x = 260
            button_y += 80
            tokens.append(Button((191, 219, 174), button_x, button_y, 40, 40, token, token))
            button_x += 150

    return tokens



def main():
    buttons = {"Build": Button((0, 0, 0), 140, 855, 139, 45, 'Build', 'build'),
               "Mortgage": Button((0, 0, 0), 280, 855, 139, 45, "Mortgage", 'mortgage'),
               "Roll": Button((0, 0, 0), 0, 855, 139, 45, "Roll:", 'roll'),
               "End Turn": Button((0, 0, 0), 420, 855, 139, 45, "End Turn", 'end_turn')}
    pygame.mixer.music.play(-1)

    player_btn = [Button((255, 255, 255), 0, 0, 40, 40), Button((255, 255, 255), 0, 0, 40, 40)]
    tokens = []
    run = True
    while run:
        p1 = board.players[board.current_player]
        assert isinstance(p1, Player)
        if p1.machine_player:
            machine_algo(p1, board, comm_chest, chance)
            player_btn[1] = Button((0, 255, 255), p1.x, p1.y, 40, 40, p1.image, p1.image, p1)
        else:
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
                            player_btn[0] = Button((0, 255, 255), p1.x, p1.y, 40, 40, token.call, token.call, p1)
                            board.players[board.current_player].picked = True
                    for player_token in player_btn:
                        if player_token.isOver(pos):
                            pygame.mixer.Sound.play(button_sound)
                            root = Tk()
                            my_gui = PopupPlayer(root, player_token.player)
                            root.mainloop()
                    for b in buttons.values():
                        if b.isOver(pos):
                            if b.call == "build":
                                pygame.mixer.Sound.play(button_sound)
                                root = Tk()
                                my_gui = PopupPropertySelector(root, p1, True)
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
                                my_gui = PopupPropertySelector(root, p1, False)
                                root.mainloop()
                            elif b.call == "roll":
                                if not p1.rolled:
                                    pygame.mixer.Sound.play(roll_sound)
                                    roll_dice(p1, board)
                                    player_btn[0].x = board.players[0].x
                                    player_btn[0].y = board.players[0].y
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
                                    buttons = {"Build": Button((0, 0, 0), 140, 855, 139, 45, 'Build', 'build'),
                                               "Mortgage": Button((0, 0, 0), 280, 855, 139, 45, "Mortgage", 'mortgage'),
                                               "Roll": Button((0, 0, 0), 0, 855, 139, 45, "Roll:", 'roll'),
                                               "End Turn": Button((0, 0, 0), 420, 855, 139, 45, "End Turn", 'end_turn')}
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
