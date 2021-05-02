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
# Global Variables
###############################
BoardLocationIndex = [[780, 800], [700, 800], [630, 800], [560, 800], [490, 800], [420, 800], [350, 800], [280, 800], [210, 800],
                      [140, 800], [70, 825], [30, 700], [30, 630], [30, 560], [30, 490], [30, 420], [30, 350], [30, 280],
                      [30, 210], [30, 140], [50, 40], [140, 30], [210, 30], [280, 30], [350, 30], [420, 30],
                      [490, 30], [560, 30], [630, 30], [700, 30], [780, 40], [800, 140], [800, 210], [800, 280],
                      [800, 350], [800, 420], [800, 490], [800, 560], [800, 630], [800, 700]]
###############################
# Sound Initializers
###############################
roll_sound = pygame.mixer.Sound(os.path.join('sounds', 'diceRolling.wav'))
purchase_sound = pygame.mixer.Sound(os.path.join('sounds', 'purchase.wav'))
button_sound = pygame.mixer.Sound(os.path.join('sounds', 'button.wav'))
card_sound = pygame.mixer.Sound(os.path.join('sounds', 'shuffleCards.wav'))
pygame.mixer.music.load(os.path.join('sounds', 'soundtrack.wav'))
###############################
# Pygame Window Initializers
###############################
width = 905
height = 900
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Monopoly")
bg = pygame.image.load("images/bord1.jpg")


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
        master.title(f"{player.name} Information")
        # self.label = Label(master, text="Select A Property").pack()
        self.label_1 = Label(master, text=f"Wallet: ${player.wallet}").pack()
        tiles = {}
        h = 75
        self.label = Label(master, text="Inventory", font='Helvetica 12 bold underline').pack()
        for tile in player.inventory:
            if isinstance(tile, Card):
                self.label = Label(master, text="Get out of Jail Free Card").pack()
                h += 40
            else:
                tiles[tile.color] = []
        for tile in player.inventory:
            if isinstance(tile, Card):
                pass
            else:
                tiles[tile.color].append(tile)
        for color, props in tiles.items():
            self.label = Label(master, text=f"{color}", font='Helvetica 10 underline').pack()
            for prop in props:
                self.label = Label(master, text=f"{prop.name}").pack()
                h += 40
        self.close_button = Button(master, text="Close", command=master.destroy).pack()
        self.master.geometry(f"400x{h}")

class PopupPropertySelector:

    def __init__(self, master, player: Player, building: bool):
        """
        Initializer - This will create a tkinter window that pops up displaying either properties to be
        mortgaged/mortgaged or properties that can be build on
        :param master: this is the tkinter tk() root
        :param player: Player object for inventory information
        :param building: bool to indicate if purpose of window is to build or mortgage
        :return: nothing
        """
        self.master = master
        self.done = False
        self.master.geometry("400x200")
        tile_dict = {}
        master.title("Property Selector")
        options = []
        self.clicked = StringVar()
        if building:
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
                        m = f"Un-mortgage for ${prop.mortgage}"
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
                                        self.execute(tile_dict[self.clicked.get()], player, building)).pack()
        self.close_button = Button(master, text="Close", command=master.destroy).pack()

    def execute(self, tile, player, building: bool):
        """
        execute - This will either do nothing if the tile passed in was an empty string, or it will call mortgage
        on the tile passed in and destroy the tkinter window(this function is needed to call to commands from one
        button push in a tkinter window)
        :param tile: tile object to pass to mortgage
        :param player: Player object to pass to mortgage call
        :param building: bool to indicate if player intends to build or mortgage
        :return: nothing
        """
        if tile == "":
            pass
        elif building:
            build(tile, player)
            self.master.destroy()
        else:
            mortgage(tile, player)
            self.master.destroy()


class GameButton:
    def __init__(self, color, x, y, button_width, button_height, text='', call='', player=None, card=None):
        """
        Initializer - This will create a button object that can display text or image.
        :param color: this is a RGB tuple to hold the color of the button
        :param x: this is the x coordinate for the button
        :param y: this is the y coordinate for the button
        :param button_width: this is the width of the button in pixels
        :param button_height: this is the height of the button in pixels
        :param text: this is a string of text to display or a file path for an image to display
        :param call: this is to hold a string that references a action to be taken when a button is clicked
        :parma player: this is a player object associated with a button. This is used for buttons that represent
        player tokens on the board
        :return: nothing
        """
        self.color = color
        self.x = x
        self.y = y
        self.width = button_width
        self.height = button_height
        self.text = text
        self.text_color = (255, 255, 255)
        self.call = call
        self.player = player
        self.card = card

    def draw(self, window, outline=None):
        """
        draw - This will blit the button to the pygame surface and any text that is passed
        :param window: this is the pygame surface to blit to
        :param outline: default to none. This is for an outline of a button in pixels using ints, the outline will
        increase or decrease the height and width of a button by the supplied int of pixels
        :return: nothing
        """
        if outline:
            pygame.draw.rect(window, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '' and self.card is None:
            font = pygame.font.SysFont('comicsans', 25)
            text = font.render(self.text, True, self.text_color)
            window.blit(text, (
                        self.x + (self.width / 2 - text.get_width() / 2), self.y +
                        (self.height / 2 - text.get_height() / 2)))
        if self.text == "Play Card":
            font = pygame.font.SysFont('comicsans', 25)
            text = font.render(self.text, True, self.text_color)
            window.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y +
                (self.height / 2 - text.get_height() / 2)))
        if not self.card is None and self.text != "Play Card":
            font = pygame.font.SysFont('comicsans', 17)
            text = font.render(self.text, True, self.text_color)
            window.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y +
                (self.height / 2 - text.get_height() / 2)))

    def draw_image(self, window):
        """
        draw tokens- This will blit player tokens to a screen, it is similar to draw but used images instead of text
        :param window: this is the pygame surface to blit to
        :return: nothing
        """
        if self.text != '':
            img = pygame.image.load(self.text)
            window.blit(img, (
                self.x + (self.width / 2 - 32 / 2), self.y + (self.height / 2 - 32 / 2)))

    def is_over(self, pos):
        """
        is over - This will tell if a mouse cursor x,y tuple is over a button object
        param: pos: this is a x,y tuple of a mouse cursor position
        :return: bool, indicating if pos is over button
        """
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


def redraw_window(window, player, buttons, tokens, btn, sound, dice_imgs, card, comChest, is_card, is_chest):
    """
    redraw window- This will display everything that is shown on the pygame surface
    :param window: the pygame surface to display to
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
        window.fill((191, 219, 174))
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("You V. Machine", True, (199, 0, 0))
        window.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2 - 100))
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Select Token", True, (199, 0, 0))
        window.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
        for t in tokens:
            t.draw_image(window)
    else:
        ######################################################################
        # this is the main game loop display window
        ######################################################################
        window.fill((255, 255, 255))
        window.blit(bg, (0, 0))
        for p in btn:
            if p.call == "":
                pass
            else:
                p.draw_image(window)
        for b in buttons.values():
            b.draw(window)
        sound.draw_image(window)
        if player.rolled:
            for die in dice_imgs:
                die.draw_image(window)
        if is_card:
            card.draw(window)
        if is_chest:
            comChest.draw(window)
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
        buttons[i[1]] = GameButton((199, 0, 0), button_x, 855, 139, 45, i[0], i[1])
        if i[1] == "chance" or i[1] == "comChest":
            buttons[i[1]].card = i[2]
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
            tokens.append(GameButton((191, 219, 174), button_x, button_y, 40, 40, token, token))
            button_x += 150
        else:
            button_x = 260
            button_y += 80
            tokens.append(GameButton((191, 219, 174), button_x, button_y, 40, 40, token, token))
            button_x += 150

    return tokens


def main():
    """
    main - This call will run the main game window. All checks for events and and logic on events is handled here.
    :return: nothing
    """
    #########################################
    # Initialize Main Loop Constants
    #########################################
    buttons = {"Build": GameButton((199, 0, 0), 140, 855, 139, 45, 'Build', 'build'),
               "Mortgage": GameButton((199, 0, 0), 280, 855, 139, 45, "Mortgage", 'mortgage'),
               "Roll": GameButton((199, 0, 0), 0, 855, 139, 45, "Roll", 'roll'),
               "End Turn": GameButton((199, 0, 0), 420, 855, 139, 45, "End Turn", 'end_turn')}
    # pygame.mixer.music.play(-1)
    volume_button = GameButton((0, 255, 255), 860, 25, 40, 40, 'images/volume.png', 'no')
    die_1 = GameButton((0, 255, 255), 400, 500, 40, 40, 'images/die_1.png', 'no')
    card = GameButton((255, 103, 0), 500, 545, 200, 100, 'this is a chance card')
    comChest = GameButton((255, 103, 0), 150, 175, 200, 100, 'this is a community chance card')
    is_card = False
    is_chest = False
    die_2 = GameButton((0, 255, 255), 430, 530, 40, 40, 'images/die_1.png', 'no')
    dice = [die_1, die_2]
    player_btn = [GameButton((255, 255, 255), 0, 0, 40, 40), GameButton((255, 255, 255), 0, 0, 40, 40)]
    tokens = []
    fx = True
    run = True
    # board.players[0].inventory.append(Chance("special", "0", "Get out of Jail Free. "))
    while run:
        if len(board.players) == 1:
            game_on = False
            if board.players[0].machine_player:
                winner = "Machine"
            else:
                winner = "Player 1"
        if game_on:
            p1 = board.players[board.current_player]
            assert isinstance(p1, Player)
            #####################################################################
            # Machine Logic Happens Here or is sent to machine algo in controller
            #####################################################################
            if p1.machine_player:
                machine_algo(p1, board, comm_chest, chance)
                player_btn[1] = GameButton((0, 255, 255), p1.x, p1.y, 30, 30, p1.image, p1.image, p1)
                if board.players[0].location == board.players[1].location:
                    if board.players[0].y < 117 and board.players[0].x < 114:
                        player_btn[0].x = board.players[0].x - 25
                        player_btn[0].y = board.players[0].y
                        player_btn[1].x = board.players[1].x + 25
                        player_btn[1].y = board.players[1].y
                    elif board.players[0].y < 117 and board.players[0].x > 741:
                        player_btn[0].x = board.players[0].x - 25
                        player_btn[0].y = board.players[0].y
                        player_btn[1].x = board.players[1].x + 25
                        player_btn[1].y = board.players[1].y
                    elif board.players[0].y > 738 and board.players[0].x > 741:
                        player_btn[0].x = board.players[0].x - 25
                        player_btn[0].y = board.players[0].y
                        player_btn[1].x = board.players[1].x + 25
                        player_btn[1].y = board.players[1].y
                    elif board.players[0].x < 114 or board.players[0].x > 741:
                        player_btn[0].x = board.players[0].x
                        player_btn[0].y = board.players[0].y - 20
                        player_btn[1].x = board.players[1].x
                        player_btn[1].y = board.players[1].y + 20
                    elif board.players[0].y < 117 or board.players[0].y > 738:
                        player_btn[0].x = board.players[0].x - 25
                        player_btn[0].y = board.players[0].y
                        player_btn[1].x = board.players[1].x + 25
                        player_btn[1].y = board.players[1].y
                    elif board.players[0].x < 34 or board.players[0].y < 38:
                        player_btn[0].x = board.players[0].x - 25
                        player_btn[0].y = board.players[0].y
                        player_btn[1].x = board.players[1].x + 25
                        player_btn[1].y = board.players[1].y
            else:
                if not p1.picked:
                    tokens = create_tokens_buttons()  # creates list of tokens if player has not picked token
                ####################################
                # Handles Closing Window
                ####################################
                for event in pygame.event.get():
                    pos = pygame.mouse.get_pos()
                    if event.type == pygame.QUIT:
                        run = False
                        pygame.quit()
                    ########################################
                    # Handle Mouse Click Events
                    ########################################
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        assert isinstance(p1, Player)
                        ########################################################
                        # Here is where we pick the tokens on the opening screen
                        ########################################################
                        if not p1.picked:
                            for token in tokens:
                                if token.is_over(pos):
                                    pygame.mixer.Sound.play(button_sound)
                                    board.players[board.current_player].image = pygame.image.load(token.call)
                                    board.pieces.remove(token.call)
                                    player_btn[0] = GameButton((0, 255, 255), p1.x, p1.y, 30, 30, token.call, token.call, p1)
                                    board.players[board.current_player].picked = True
                        ######################################################
                        # Here is where we handle clicking on a players token
                        ######################################################
                        for player_token in player_btn:
                            if player_token.is_over(pos):
                                if fx:
                                    pygame.mixer.Sound.play(button_sound)
                                root = Tk()  # used to create root for tkinter window
                                player_window = PopupPlayer(root, player_token.player)  # create popup player object
                                root.mainloop()  # run tkinter window until killed
                        #################################################################
                        # Pause Game Music and FX
                        #################################################################
                        if volume_button.is_over(pos):
                            if volume_button.call == "no":
                                fx = False
                                pygame.mixer.music.pause()
                                volume_button.call = "yes"
                                volume_button.text = "images/mute.png"
                            else:
                                fx = True
                                pygame.mixer.music.unpause()
                                volume_button.call = "no"
                                volume_button.text = "images/volume.png"
                        ###################################################################
                        # Here is where we put our cases for handling clicking game buttons
                        ###################################################################
                        for b in buttons.values():
                            if b.is_over(pos):
                                if b.call == "build":
                                    if fx:
                                        pygame.mixer.Sound.play(button_sound)
                                    root = Tk()
                                    build_window = PopupPropertySelector(root, p1, True)
                                    root.mainloop()
                                elif b.call == "rent":
                                    if fx:
                                        pygame.mixer.Sound.play(purchase_sound)
                                    bankrupt = pay_rent(p1, board.tiles[p1.location])
                                    if bankrupt:
                                        buttons["Bankrupt"] = GameButton((199, 0, 0), 140, 855, 139, 45, 'Go Bankrupt',
                                                                         'bankrupt')
                                    else:
                                        buttons.pop('rent')
                                        break
                                elif b.call == "bankrupt":
                                    if fx:
                                        pygame.mixer.Sound.play(button_sound)
                                    go_bankrupt(p1, comm_chest, chance)
                                    board.players.remove(p1)
                                elif b.call == "tax":
                                    if fx:
                                        pygame.mixer.Sound.play(purchase_sound)
                                    bankrupt = pay_tax(p1, board.tiles[p1.location])
                                    if bankrupt:
                                        buttons["Bankrupt"] = GameButton((199, 0, 0), 140, 855, 139, 45, 'Go Bankrupt',
                                                                         'bankrupt')
                                    else:
                                        buttons.pop("tax")
                                    break
                                elif b.call == "pay_bail_optional" or b.call == "pay_bail_required":
                                    if fx:
                                        pygame.mixer.Sound.play(purchase_sound)
                                    pay_bail(p1, board.tiles[p1.location])
                                    count = 0
                                    for i in BoardLocationIndex:
                                        if i[0] == board.players[0].x and i[1] == board.players[0].y:
                                            player_btn[0].player.location = count
                                        count += 1
                                    if board.players[0].location == board.players[1].location:
                                        if board.players[0].y < 117 and board.players[0].x < 114:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].y < 117 and board.players[0].x > 741:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].y > 738 and board.players[0].x > 741:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].x < 114 or board.players[0].x > 741:
                                            player_btn[0].x = board.players[0].x
                                            player_btn[0].y = board.players[0].y - 20
                                            player_btn[1].x = board.players[1].x
                                            player_btn[1].y = board.players[1].y + 20
                                        elif board.players[0].y < 117 or board.players[0].y > 738:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].x < 34 or board.players[0].y < 38:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                    else:
                                        player_btn[0].x = board.players[0].x
                                        player_btn[0].y = board.players[0].y
                                    buttons.pop("pay_bail_optional")
                                    buttons.pop("pay_bail_required")
                                    break
                                elif b.call == "jail_card_optional" or b.call == "jail_card_required":
                                    if fx:
                                        pygame.mixer.Sound.play(card_sound)
                                    use_jail_card(p1, board.tiles[p1.location], comm_chest, chance)
                                elif b.call == "chance":
                                    if fx:
                                        pygame.mixer.Sound.play(card_sound)
                                    is_card = True
                                    assert isinstance(b.card, Card)
                                    coord, cardObj, instruction = play_card(player_btn[0].player, player_btn[0].card, board.players, board.tiles, BoardLocationIndex, "chance", comm_chest, chance)
                                    card.card = cardObj
                                    card.text = card.card.message
                                    if coord[0] != -1 and coord[1] != -1:
                                        player_btn[0].x = coord[0]
                                        player_btn[0].y = coord[1]
                                        count = 0
                                        for i in BoardLocationIndex:
                                            if i[0] == board.players[0].x and i[1] == board.players[0].y:
                                                player_btn[0].player.location = count
                                            count += 1
                                        if board.players[0].location == board.players[1].location:
                                            if board.players[0].y < 117 and board.players[0].x < 114:
                                                player_btn[0].x = board.players[0].x - 25
                                                player_btn[0].y = board.players[0].y
                                                player_btn[1].x = board.players[1].x + 25
                                                player_btn[1].y = board.players[1].y
                                            elif board.players[0].y < 117 and board.players[0].x > 741:
                                                player_btn[0].x = board.players[0].x - 25
                                                player_btn[0].y = board.players[0].y
                                                player_btn[1].x = board.players[1].x + 25
                                                player_btn[1].y = board.players[1].y
                                            elif board.players[0].y > 738 and board.players[0].x > 741:
                                                player_btn[0].x = board.players[0].x - 25
                                                player_btn[0].y = board.players[0].y
                                                player_btn[1].x = board.players[1].x + 25
                                                player_btn[1].y = board.players[1].y
                                            elif board.players[0].x < 114 or board.players[0].x > 741:
                                                player_btn[0].x = board.players[0].x
                                                player_btn[0].y = board.players[0].y - 20
                                                player_btn[1].x = board.players[1].x
                                                player_btn[1].y = board.players[1].y + 20
                                            elif board.players[0].y < 117 or board.players[0].y > 738:
                                                player_btn[0].x = board.players[0].x - 25
                                                player_btn[0].y = board.players[0].y
                                                player_btn[1].x = board.players[1].x + 25
                                                player_btn[1].y = board.players[1].y
                                            elif board.players[0].x < 34 or board.players[0].y < 38:
                                                player_btn[0].x = board.players[0].x - 25
                                                player_btn[0].y = board.players[0].y
                                                player_btn[1].x = board.players[1].x + 25
                                                player_btn[1].y = board.players[1].y
                                    buttons.pop('chance')
                                    if instruction != "":
                                        buttons = create_landson_buttons(instruction, buttons)
                                    break
                                elif b.call == "comChest":
                                    if fx:
                                        pygame.mixer.Sound.play(card_sound)
                                    is_chest = True
                                    assert isinstance(b.card, Card)
                                    coord, cardObj, instruction = play_card(player_btn[0].player, player_btn[0].card, board.players, board.tiles, BoardLocationIndex, "comChest", comm_chest, chance)
                                    comChest.card = cardObj
                                    comChest.text = comChest.card.message
                                    if coord[0] != -1 and coord[1] != -1:
                                        player_btn[0].x = coord[0]
                                        player_btn[0].y = coord[1]
                                        count = 0
                                        for i in BoardLocationIndex:
                                            if i[0] == board.players[0].x and i[1] == board.players[0].y:
                                                player_btn[0].player.location = count
                                            count += 1
                                        if board.players[0].location == board.players[1].location:
                                            if board.players[0].y < 117 and board.players[0].x < 114:
                                                player_btn[0].x = board.players[0].x - 25
                                                player_btn[0].y = board.players[0].y
                                                player_btn[1].x = board.players[1].x + 25
                                                player_btn[1].y = board.players[1].y
                                            elif board.players[0].y < 117 and board.players[0].x > 741:
                                                player_btn[0].x = board.players[0].x - 25
                                                player_btn[0].y = board.players[0].y
                                                player_btn[1].x = board.players[1].x + 25
                                                player_btn[1].y = board.players[1].y
                                            elif board.players[0].y > 738 and board.players[0].x > 741:
                                                player_btn[0].x = board.players[0].x - 25
                                                player_btn[0].y = board.players[0].y
                                                player_btn[1].x = board.players[1].x + 25
                                                player_btn[1].y = board.players[1].y
                                            elif board.players[0].x < 114 or board.players[0].x > 741:
                                                player_btn[0].x = board.players[0].x
                                                player_btn[0].y = board.players[0].y - 20
                                                player_btn[1].x = board.players[1].x
                                                player_btn[1].y = board.players[1].y + 20
                                            elif board.players[0].y < 117 or board.players[0].y > 738:
                                                player_btn[0].x = board.players[0].x - 25
                                                player_btn[0].y = board.players[0].y
                                                player_btn[1].x = board.players[1].x + 25
                                                player_btn[1].y = board.players[1].y
                                            elif board.players[0].x < 34 or board.players[0].y < 38:
                                                player_btn[0].x = board.players[0].x - 25
                                                player_btn[0].y = board.players[0].y
                                                player_btn[1].x = board.players[1].x + 25
                                                player_btn[1].y = board.players[1].y
                                    buttons.pop('comChest')
                                    if instruction != "":
                                        buttons = create_landson_buttons(instruction, buttons)
                                    break
                                elif b.call == "purchase":
                                    if fx:
                                        pygame.mixer.Sound.play(purchase_sound)
                                    purchase(p1, board.tiles[p1.location])
                                    buttons.pop("purchase")
                                    break
                                elif b.call == "mortgage":
                                    if fx:
                                        pygame.mixer.Sound.play(button_sound)
                                    root = Tk()
                                    mortgage_window = PopupPropertySelector(root, p1, False)
                                    root.mainloop()
                                elif b.call == "roll":
                                    if not p1.rolled:
                                        if fx:
                                            pygame.mixer.Sound.play(roll_sound)
                                        create_landson_buttons(roll_dice(p1, board), buttons)
                                        dice[0].text = f"images/die_{p1.roll_1}.png"
                                        dice[1].text = f"images/die_{p1.roll_2}.png"
                                        if board.players[0].location == board.players[1].location:
                                            count = 0
                                            for i in BoardLocationIndex:
                                                if i[0] == board.players[0].x and i[1] == board.players[0].y:
                                                    player_btn[0].player.location = count
                                                count += 1
                                            if board.players[0].y < 117 and board.players[0].x < 114:
                                                player_btn[0].x = board.players[0].x - 25
                                                player_btn[0].y = board.players[0].y
                                                player_btn[1].x = board.players[1].x + 25
                                                player_btn[1].y = board.players[1].y
                                            elif board.players[0].y < 117 and board.players[0].x > 741:
                                                player_btn[0].x = board.players[0].x - 25
                                                player_btn[0].y = board.players[0].y
                                                player_btn[1].x = board.players[1].x + 25
                                                player_btn[1].y = board.players[1].y
                                            elif board.players[0].y > 738 and board.players[0].x > 741:
                                                player_btn[0].x = board.players[0].x - 25
                                                player_btn[0].y = board.players[0].y
                                                player_btn[1].x = board.players[1].x + 25
                                                player_btn[1].y = board.players[1].y
                                            elif board.players[0].x < 114 or board.players[0].x > 741:
                                                player_btn[0].x = board.players[0].x
                                                player_btn[0].y = board.players[0].y - 20
                                                player_btn[1].x = board.players[1].x
                                                player_btn[1].y = board.players[1].y + 20
                                            elif board.players[0].y < 117 or board.players[0].y > 738:
                                                player_btn[0].x = board.players[0].x - 25
                                                player_btn[0].y = board.players[0].y
                                                player_btn[1].x = board.players[1].x + 25
                                                player_btn[1].y = board.players[1].y
                                            elif board.players[0].x < 34 or board.players[0].y < 38:
                                                player_btn[0].x = board.players[0].x - 25
                                                player_btn[0].y = board.players[0].y
                                                player_btn[1].x = board.players[1].x + 25
                                                player_btn[1].y = board.players[1].y
                                        else:
                                            if board.players[0].location != board.players[1].location:
                                                count = 0
                                                for i in BoardLocationIndex:
                                                    if i[0] == board.players[0].x and i[1] == board.players[0].y:
                                                        player_btn[0].player.location = count
                                                    count += 1
                                            player_btn[0].x = board.players[0].x
                                            player_btn[0].y = board.players[0].y
                                        buttons = create_landson_buttons(lands_on(board.tiles[p1.location], p1, chance,
                                                                                  comm_chest), buttons)
                                        p1.rolled = True
                                        break
                                elif b.call == "toJail":
                                    if fx:
                                        pygame.mixer.Sound.play(button_sound)
                                    player_btn[0].x = board.players[0].x
                                    player_btn[0].y = board.players[0].y
                                    if board.players[0].location == board.players[1].location:
                                        count = 0
                                        for i in BoardLocationIndex:
                                            if i[0] == board.players[0].x and i[1] == board.players[0].y:
                                                player_btn[0].player.location = count
                                            count += 1
                                        if board.players[0].y < 117 and board.players[0].x < 114:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].y < 117 and board.players[0].x > 741:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].y > 738 and board.players[0].x > 741:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].x < 114 or board.players[0].x > 741:
                                            player_btn[0].x = board.players[0].x
                                            player_btn[0].y = board.players[0].y - 20
                                            player_btn[1].x = board.players[1].x
                                            player_btn[1].y = board.players[1].y + 20
                                        elif board.players[0].y < 117 or board.players[0].y > 738:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].x < 34 or board.players[0].y < 38:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                    buttons.pop("toJail")
                                    break
                                elif b.call == "end_turn":
                                    if fx:
                                        pygame.mixer.Sound.play(button_sound)
                                    if (not p1.rolled or "rent" in buttons or "chance" in buttons or "commChest" in buttons or "tax" in buttons or
                                            "pay_bail_required" in buttons or "jail_card_required" in buttons):
                                        pass
                                    if p1.extra_turn:
                                        p1.extra_turn = False
                                    else:
                                        p1.rolled = False
                                        is_card = False
                                        is_chest = False
                                        change_player(board)
                                        buttons = {"Build": GameButton((199, 0, 0), 140, 855, 139, 45, 'Build', 'build'),
                                                   "Mortgage":
                                                       GameButton((199, 0, 0), 280, 855, 139, 45, "Mortgage", 'mortgage'),
                                                   "Roll":
                                                       GameButton((199, 0, 0), 0, 855, 139, 45, "Roll", 'roll'),
                                                   "End Turn":
                                                       GameButton((199, 0, 0), 420, 855, 139, 45, "End Turn", 'end_turn')}
                    ######################################################################################
                    # Handle Mouse Movement events for our purposes this is where the buttons change color
                    #######################################################################################
                    if event.type == pygame.MOUSEMOTION:
                        for b in buttons.values():
                            if b.is_over(pos):
                                b.color = (191, 219, 174)
                                b.text_color = (0, 0, 0)
                            else:
                                b.color = (199, 0, 0)
                                b.text_color = (255, 255, 255)
            #############################################
            # ***BELOW CODE MUST BE CALLED EVERY LOOP***
            #############################################
            redraw_window(win, p1, buttons, tokens, player_btn, volume_button, dice, card, comChest, is_card, is_chest)
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
            font = pygame.font.SysFont("comicsans", 80)
            text = font.render(f"{winner} won the game", True, (199, 0, 0))
            win.blit(text, (width / 2 - text.get_width() / 2 - 30, height / 2 - text.get_height() / 2 + 100))
            pygame.display.update()
        p1 = board.players[board.current_player]
        assert isinstance(p1, Player)
        #####################################################################
        # Machine Logic Happens Here or is sent to machine algo in controller
        #####################################################################
        if p1.machine_player:
            machine_algo(p1, board, comm_chest, chance)
            player_btn[1] = GameButton((0, 255, 255), p1.x, p1.y, 40, 40, p1.image, p1.image, p1)
            if board.players[0].location == board.players[1].location:
                if board.players[0].y < 117 and board.players[0].x < 114:
                    player_btn[0].x = board.players[0].x - 25
                    player_btn[0].y = board.players[0].y
                    player_btn[1].x = board.players[1].x + 25
                    player_btn[1].y = board.players[1].y
                elif board.players[0].y < 117 and board.players[0].x > 741:
                    player_btn[0].x = board.players[0].x - 25
                    player_btn[0].y = board.players[0].y
                    player_btn[1].x = board.players[1].x + 25
                    player_btn[1].y = board.players[1].y
                elif board.players[0].y > 738 and board.players[0].x > 741:
                    player_btn[0].x = board.players[0].x - 25
                    player_btn[0].y = board.players[0].y
                    player_btn[1].x = board.players[1].x + 25
                    player_btn[1].y = board.players[1].y
                elif board.players[0].x < 34 or board.players[0].y < 38:
                    player_btn[0].x = board.players[0].x - 25
                    player_btn[0].y = board.players[0].y
                    player_btn[1].x = board.players[1].x + 25
                    player_btn[1].y = board.players[1].y
                elif board.players[0].x < 114 or board.players[0].x > 741:
                    player_btn[0].x = board.players[0].x
                    player_btn[0].y = board.players[0].y - 20
                    player_btn[1].x = board.players[1].x
                    player_btn[1].y = board.players[1].y + 20
                elif board.players[0].y < 117 or board.players[0].y > 738:
                    player_btn[0].x = board.players[0].x - 25
                    player_btn[0].y = board.players[0].y
                    player_btn[1].x = board.players[1].x + 25
                    player_btn[1].y = board.players[1].y
        else:
            if not p1.picked:
                tokens = create_tokens_buttons()  # creates list of tokens if player has not picked token
            ####################################
            # Handles Closing Window
            ####################################
            for event in pygame.event.get():
                pos = pygame.mouse.get_pos()
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                ########################################
                # Handle Mouse Click Events
                ########################################
                if event.type == pygame.MOUSEBUTTONDOWN:
                    assert isinstance(p1, Player)
                    ########################################################
                    # Here is where we pick the tokens on the opening screen
                    ########################################################
                    if not p1.picked:
                        for token in tokens:
                            if token.is_over(pos):
                                pygame.mixer.Sound.play(button_sound)
                                board.players[board.current_player].image = pygame.image.load(token.call)
                                board.pieces.remove(token.call)
                                player_btn[0] = GameButton((0, 255, 255), p1.x, p1.y, 40, 40, token.call, token.call, p1)
                                board.players[board.current_player].picked = True
                    ######################################################
                    # Here is where we handle clicking on a players token
                    ######################################################
                    for player_token in player_btn:
                        if player_token.is_over(pos):
                            pygame.mixer.Sound.play(button_sound)
                            root = Tk()  # used to create root for tkinter window
                            player_window = PopupPlayer(root, player_token.player)  # create popup player object
                            root.mainloop()  # run tkinter window until killed
                    #################################################################
                    # Pause Game Music and FX
                    #################################################################
                    if volume_button.is_over(pos):
                        if volume_button.call == "no":
                            fx = False
                            pygame.mixer.music.pause()
                            volume_button.call = "yes"
                            volume_button.text = "images/mute.png"
                        else:
                            fx = True
                            pygame.mixer.music.unpause()
                            volume_button.call = "no"
                            volume_button.text = "images/volume.png"
                    ###################################################################
                    # Here is where we put our cases for handling clicking game buttons
                    ###################################################################
                    for b in buttons.values():
                        if b.is_over(pos):
                            if b.call == "build":
                                if fx:
                                    pygame.mixer.Sound.play(button_sound)
                                root = Tk()
                                build_window = PopupPropertySelector(root, p1, True)
                                root.mainloop()
                            elif b.call == "rent":
                                if fx:
                                    pygame.mixer.Sound.play(purchase_sound)
                                pay_rent(p1, board.tiles[p1.location])
                                buttons.pop('rent')
                                break
                            elif b.call == "tax":
                                if fx:
                                    pygame.mixer.Sound.play(purchase_sound)
                                pay_tax(p1, board.tiles[p1.location])
                                buttons.pop("tax")
                                break
                            elif b.call == "pay_bail_optional" or b.call == "pay_bail_required":
                                if fx:
                                    pygame.mixer.Sound.play(purchase_sound)
                                pay_bail(p1, board.tiles[p1.location])
                                count = 0
                                for i in BoardLocationIndex:
                                    if i[0] == board.players[0].x and i[1] == board.players[0].y:
                                        player_btn[0].player.location = count
                                    count += 1
                                if board.players[0].location == board.players[1].location:
                                    if board.players[0].y < 117 and board.players[0].x < 114:
                                        player_btn[0].x = board.players[0].x - 25
                                        player_btn[0].y = board.players[0].y
                                        player_btn[1].x = board.players[1].x + 25
                                        player_btn[1].y = board.players[1].y
                                    elif board.players[0].y < 117 and board.players[0].x > 741:
                                        player_btn[0].x = board.players[0].x - 25
                                        player_btn[0].y = board.players[0].y
                                        player_btn[1].x = board.players[1].x + 25
                                        player_btn[1].y = board.players[1].y
                                    elif board.players[0].y > 738 and board.players[0].x > 741:
                                        player_btn[0].x = board.players[0].x - 25
                                        player_btn[0].y = board.players[0].y
                                        player_btn[1].x = board.players[1].x + 25
                                        player_btn[1].y = board.players[1].y
                                    elif board.players[0].x < 34 or board.players[0].y < 38:
                                        player_btn[0].x = board.players[0].x - 25
                                        player_btn[0].y = board.players[0].y
                                        player_btn[1].x = board.players[1].x + 25
                                        player_btn[1].y = board.players[1].y
                                    elif board.players[0].x < 114 or board.players[0].x > 741:
                                        player_btn[0].x = board.players[0].x
                                        player_btn[0].y = board.players[0].y - 20
                                        player_btn[1].x = board.players[1].x
                                        player_btn[1].y = board.players[1].y + 20
                                    elif board.players[0].y < 117 or board.players[0].y > 738:
                                        player_btn[0].x = board.players[0].x - 25
                                        player_btn[0].y = board.players[0].y
                                        player_btn[1].x = board.players[1].x + 25
                                        player_btn[1].y = board.players[1].y
                                else:
                                    player_btn[0].x = board.players[0].x
                                    player_btn[0].y = board.players[0].y
                                buttons.pop("pay_bail_optional")
                                buttons.pop("pay_bail_required")
                                break
                            elif b.call == "jail_card_optional" or b.call == "jail_card_required":
                                if fx:
                                    pygame.mixer.Sound.play(card_sound)
                                use_jail_card(p1, board.tiles[p1.location], comm_chest, chance)
                            elif b.call == "chance":
                                if fx:
                                    pygame.mixer.Sound.play(card_sound)
                                is_card = True
                                assert isinstance(b.card, Card)
                                coord, cardObj, instruction = play_card(player_btn[0].player, player_btn[0].card, board.players, board.tiles, BoardLocationIndex, "chance", comm_chest, chance)
                                card.card = cardObj
                                card.text = card.card.message
                                if coord[0] != -1 and coord[1] != -1:
                                    player_btn[0].x = coord[0]
                                    player_btn[0].y = coord[1]
                                    count = 0
                                    for i in BoardLocationIndex:
                                        if i[0] == board.players[0].x and i[1] == board.players[0].y:
                                            player_btn[0].player.location = count
                                        count += 1
                                    if player_btn[0].x == player_btn[1].x and player_btn[0].y == player_btn[1].y:
                                        if board.players[0].y < 117 and board.players[0].x < 114:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].y < 117 and board.players[0].x > 741:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].y > 738 and board.players[0].x > 741:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].x < 34 or board.players[0].y < 38:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].x < 114 or board.players[0].x > 741:
                                            player_btn[0].x = board.players[0].x
                                            player_btn[0].y = board.players[0].y - 20
                                            player_btn[1].x = board.players[1].x
                                            player_btn[1].y = board.players[1].y + 20
                                        elif board.players[0].y < 117 or board.players[0].y > 738:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                buttons.pop('chance')
                                if instruction != "":
                                    buttons = create_landson_buttons(instruction, buttons)
                                break
                            elif b.call == "comChest":
                                if fx:
                                    pygame.mixer.Sound.play(card_sound)
                                is_chest = True
                                assert isinstance(b.card, Card)
                                coord, cardObj, instruction = play_card(player_btn[0].player, player_btn[0].card, board.players, board.tiles, BoardLocationIndex, "comChest", comm_chest, chance)
                                comChest.card = cardObj
                                comChest.text = comChest.card.message
                                if coord[0] != -1 and coord[1] != -1:
                                    player_btn[0].x = coord[0]
                                    player_btn[0].y = coord[1]
                                    count = 0
                                    for i in BoardLocationIndex:
                                        if i[0] == board.players[0].x and i[1] == board.players[0].y:
                                            player_btn[0].player.location = count
                                        count += 1
                                    if board.players[0].location == board.players[1].location:
                                        if board.players[0].y < 117 and board.players[0].x < 114:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].y < 117 and board.players[0].x > 741:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].y > 738 and board.players[0].x > 741:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].x < 34 or board.players[0].y < 38:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].x < 114 or board.players[0].x > 741:
                                            player_btn[0].x = board.players[0].x
                                            player_btn[0].y = board.players[0].y - 20
                                            player_btn[1].x = board.players[1].x
                                            player_btn[1].y = board.players[1].y + 20
                                        elif board.players[0].y < 117 or board.players[0].y > 738:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                buttons.pop('comChest')
                                if instruction != "":
                                    buttons = create_landson_buttons(instruction, buttons)
                                break
                            elif b.call == "purchase":
                                if fx:
                                    pygame.mixer.Sound.play(purchase_sound)
                                purchase(p1, board.tiles[p1.location])
                                buttons.pop("purchase")
                                break
                            elif b.call == "mortgage":
                                if fx:
                                    pygame.mixer.Sound.play(button_sound)
                                root = Tk()
                                mortgage_window = PopupPropertySelector(root, p1, False)
                                root.mainloop()
                            elif b.call == "roll":
                                if not p1.rolled:
                                    if fx:
                                        pygame.mixer.Sound.play(roll_sound)
                                    create_landson_buttons(roll_dice(p1, board), buttons)
                                    dice[0].text = f"images/die_{p1.roll_1}.png"
                                    dice[1].text = f"images/die_{p1.roll_2}.png"
                                    if board.players[0].location == board.players[1].location:
                                        count = 0
                                        for i in BoardLocationIndex:
                                            if i[0] == board.players[0].x and i[1] == board.players[0].y:
                                                player_btn[0].player.location = count
                                            count += 1
                                        if board.players[0].y < 117 and board.players[0].x < 114:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].y < 117 and board.players[0].x > 741:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].y > 738 and board.players[0].x > 741:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].x < 34 or board.players[0].y < 38:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                        elif board.players[0].x < 114 or board.players[0].x > 741:
                                            player_btn[0].x = board.players[0].x
                                            player_btn[0].y = board.players[0].y - 20
                                            player_btn[1].x = board.players[1].x
                                            player_btn[1].y = board.players[1].y + 20
                                        elif board.players[0].y < 117 or board.players[0].y > 738:
                                            player_btn[0].x = board.players[0].x - 25
                                            player_btn[0].y = board.players[0].y
                                            player_btn[1].x = board.players[1].x + 25
                                            player_btn[1].y = board.players[1].y
                                    else:
                                        if board.players[0].location != board.players[1].location:
                                            count = 0
                                            for i in BoardLocationIndex:
                                                if i[0] == board.players[0].x and i[1] == board.players[0].y:
                                                    player_btn[0].player.location = count
                                                count += 1
                                        player_btn[0].x = board.players[0].x
                                        player_btn[0].y = board.players[0].y
                                    buttons = create_landson_buttons(lands_on(board.tiles[p1.location], p1, chance,
                                                                              comm_chest), buttons)
                                    p1.rolled = True
                                    break
                            elif b.call == "toJail":
                                if fx:
                                    pygame.mixer.Sound.play(button_sound)
                                player_btn[0].x = board.players[0].x
                                player_btn[0].y = board.players[0].y
                                if board.players[0].location == board.players[1].location:
                                    count = 0
                                    for i in BoardLocationIndex:
                                        if i[0] == board.players[0].x and i[1] == board.players[0].y:
                                            player_btn[0].player.location = count
                                        count += 1
                                    if board.players[0].y < 117 and board.players[0].x < 114:
                                        player_btn[0].x = board.players[0].x - 25
                                        player_btn[0].y = board.players[0].y
                                        player_btn[1].x = board.players[1].x + 25
                                        player_btn[1].y = board.players[1].y
                                    elif board.players[0].y < 117 and board.players[0].x > 741:
                                        player_btn[0].x = board.players[0].x - 25
                                        player_btn[0].y = board.players[0].y
                                        player_btn[1].x = board.players[1].x + 25
                                        player_btn[1].y = board.players[1].y
                                    elif board.players[0].y > 738 and board.players[0].x > 741:
                                        player_btn[0].x = board.players[0].x - 25
                                        player_btn[0].y = board.players[0].y
                                        player_btn[1].x = board.players[1].x + 25
                                        player_btn[1].y = board.players[1].y
                                    elif board.players[0].x < 34 or board.players[0].y < 38:
                                        player_btn[0].x = board.players[0].x - 25
                                        player_btn[0].y = board.players[0].y
                                        player_btn[1].x = board.players[1].x + 25
                                        player_btn[1].y = board.players[1].y
                                    elif board.players[0].x < 114 or board.players[0].x > 741:
                                        player_btn[0].x = board.players[0].x
                                        player_btn[0].y = board.players[0].y - 20
                                        player_btn[1].x = board.players[1].x
                                        player_btn[1].y = board.players[1].y + 20
                                    elif board.players[0].y < 117 or board.players[0].y > 738:
                                        player_btn[0].x = board.players[0].x - 25
                                        player_btn[0].y = board.players[0].y
                                        player_btn[1].x = board.players[1].x + 25
                                        player_btn[1].y = board.players[1].y
                                buttons.pop("toJail")
                                break
                            elif b.call == "end_turn":
                                if fx:
                                    pygame.mixer.Sound.play(button_sound)
                                if (not p1.rolled or "rent" in buttons or "chance" in buttons or "commChest" in buttons or "tax" in buttons or
                                        "pay_bail_required" in buttons or "jail_card_required" in buttons):
                                    pass
                                if p1.extra_turn:
                                    p1.extra_turn = False
                                else:
                                    p1.rolled = False
                                    is_card = False
                                    is_chest = False
                                    change_player(board)
                                    buttons = {"Build": GameButton((199, 0, 0), 140, 855, 139, 45, 'Build', 'build'),
                                               "Mortgage":
                                                   GameButton((199, 0, 0), 280, 855, 139, 45, "Mortgage", 'mortgage'),
                                               "Roll":
                                                   GameButton((199, 0, 0), 0, 855, 139, 45, "Roll", 'roll'),
                                               "End Turn":
                                                   GameButton((199, 0, 0), 420, 855, 139, 45, "End Turn", 'end_turn')}
                ######################################################################################
                # Handle Mouse Movement events for our purposes this is where the buttons change color
                #######################################################################################
                if event.type == pygame.MOUSEMOTION:
                    for b in buttons.values():
                        if b.is_over(pos):
                            b.color = (191, 219, 174)
                            b.text_color = (0, 0, 0)
                        else:
                            b.color = (199, 0, 0)
                            b.text_color = (255, 255, 255)
        #############################################
        # ***BELOW CODE MUST BE CALLED EVERY LOOP***
        #############################################
        redraw_window(win, p1, buttons, tokens, player_btn, volume_button, dice, card, comChest, is_card, is_chest)


main()
