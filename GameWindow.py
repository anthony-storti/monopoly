import pygame
from tkinter import *
from Controller import *

pygame.init()
game = load_game()    # gets the tuple we pickled
board = game[0]       # gets board from tuple
comm_chest = game[1]  # gets shuffled deck of community chest cards
chance = game[2]      # gets shuffled deck of chance cards
create_player('player 1', 'Dog', board, 770, 825, "images/dog.png", False)
create_player('player 1', 'Car', board, 770, 825, "images/car.png", False)


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
                        m = f"Mortgaged for ${prop.mortgage}"
                    else:
                        m = f"Unmortgage for ${prop.mortgage}"
                    tile_dict[f"{prop.name} | {m}"] = prop
                    options.append(f"{prop.name} | {m}")
                    self.clicked.set(prop.name)


        self.label = Label(master, text="Select A Property").pack()

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
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_color = (255, 255, 255)

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, True, self.text_color)
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


def redrawWindow(win, player, buttons):
    win.fill((255, 255, 255))
    win.blit(bg, (0, 0))
    for p in board.players:
        win.blit(p.image, (p.x, p.y))
    for b in buttons.values():
        b.draw(win)
    pygame.display.update()


def create_landson_buttons(instr, buttons):
    button_x = 560
    count = 0
    for i in instr:
        buttons[instr[count][0]] = button((0, 0, 0), button_x, 855, 139, 45, instr[count][0])
        button_x += 140
        count += 1
    return buttons


def main():
    buttons = {"Build": button((0, 0, 0), 140, 855, 139, 45, 'Build'),
               "Mortgage": button((0, 0, 0), 280, 855, 139, 45, "Mortgage"),
               "Roll": button((0, 0, 0), 0, 855, 139, 45, "Roll:"),
               "End Turn": button((0, 0, 0), 420, 855, 139, 45, "End Turn")}
    run = True
    while run:
        p1 = board.players[board.current_player]
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                assert isinstance(p1, Player)
                for b in buttons.values():
                    if b.isOver(pos):
                        if b.text == "Build":
                            root = Tk()
                            my_gui = Popup(root, p1, True)
                            root.mainloop()
                        elif b.text == "Purchase":
                            purchase(p1, board.tiles[p1.location])
                            buttons.pop("Purchase")
                            break
                        elif b.text == "Mortgage":
                            root = Tk()
                            my_gui = Popup(root, p1, False)
                            root.mainloop()
                        elif b.text == "Roll:":
                            roll_dice(p1, board)
                            b.text = f"Roll: {p1.roll}"
                            buttons = create_landson_buttons(lands_on(board.tiles[p1.location], p1, chance, comm_chest), buttons)
                            p1.rolled = True
                            break
                        elif b.text == "End Turn":
                            p1.rolled = False
                            change_player(board)
                            buttons = {"Build": button((0, 0, 0), 140, 855, 139, 45, 'Build'),
                                       "Mortgage": button((0, 0, 0), 280, 855, 139, 45, "Mortgage"),
                                       "Roll": button((0, 0, 0), 0, 855, 139, 45, "Roll:"),
                                       "End Turn": button((0, 0, 0), 420, 855, 139, 45, "End Turn")}
            if event.type == pygame.MOUSEMOTION:
                for b in buttons.values():
                    if b.isOver(pos):
                        b.color = (0, 255, 0)
                        b.text_color = (0, 0, 0)
                    else:
                        b.color = (0, 0, 0)
                        b.text_color = (255, 255, 255)

        redrawWindow(win, p1, buttons)


main()
