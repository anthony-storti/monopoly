import pygame
from tkinter import *
from Controller import *
from Game import *

pygame.init()
game = Game(load_game()) # gets the tuple we pickled
board = game.board      # gets board from tuple
comm_chest = game.comm_chest # gets shuffled deck of community chest cards
chance = game.chance      # gets shuffled deck of chance cards



class PropertyPopup:
    def __init__(self, master, player: Player, build: bool):
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
            tile = player.inventory
            if len(tile) == 0:
                options = ["No Inventory"]
            else:
                tile_dict["Select Property"] = ""
                for prop in tile:
                    assert isinstance(prop, (Property, RailRoad, Utility))
                    if not prop.mortgaged:
                        m = f"Mortgage for ${prop.mortgage}"
                    else:
                        m = f"Unmortgage for ${prop.mortgage}"
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
        win.blit(pygame.image.load(p.image), (p.x, p.y))
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


def main():
    buttons = {"Build": button((0, 0, 0), 140, 855, 139, 45, 'Build', 'build'),
               "Mortgage": button((0, 0, 0), 280, 855, 139, 45, "Mortgage", 'mortgage'),
               "Roll": button((0, 0, 0), 0, 855, 139, 45, "Roll:", 'roll'),
               "End Turn": button((0, 0, 0), 420, 855, 139, 45, "End Turn", 'end_turn')}
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
                        if b.call == "build":
                            root = Tk()
                            my_gui = PropertyPopup(root, p1, True)
                            root.mainloop()
                        elif b.call == "rent":
                            pay_rent(p1, board.tiles[p1.location])
                            buttons.pop('rent')
                            break
                        elif b.call == "purchase":
                            purchase(p1, board.tiles[p1.location])
                            buttons.pop("purchase")
                            break
                        elif b.call == "mortgage":
                            root = Tk()
                            my_gui = PropertyPopup(root, p1, False)
                            root.mainloop()
                        elif b.call == "roll":
                            roll_dice(p1, board)
                            b.text = f"Roll: {p1.roll}"
                            buttons = create_landson_buttons(lands_on(board.tiles[p1.location], p1, chance, comm_chest), buttons)
                            p1.rolled = True
                            break
                        elif b.call == "end_turn":
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

        redrawWindow(win, p1, buttons)


main()
