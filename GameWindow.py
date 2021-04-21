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
    def __init__(self, master, player: Player):
        self.master = master
        self.master.geometry("200x200")

        master.title("Selector")
        options = []
        if len(player.inventory) == 0:
            options = ["No Inventory"]
        else:
            for prop in player.inventory:
                assert isinstance(prop, Property)
                options.append(prop.name)

        self.label = Label(master, text="Select A Property").pack()

        self.clicked = StringVar()
        self.clicked.set("Select a Property")

        self.drop = OptionMenu(self.master, self.clicked, *options).pack()

        self.greet_button = Button(master, text="Select", command=self.greet).pack()

        self.close_button = Button(master, text="Close", command=master.destroy).pack()

    def greet(self):
        print("Greetings!")


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
            font = pygame.font.SysFont('comicsans', 40)
            text = font.render(self.text, True, self.text_color)
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

#####################################
# This is where buttons are declared
######################################
roll = button((0, 0, 0), 755, 855, 100, 45, 'Roll:')
end_turn = button((0, 0, 0), 630, 855, 125, 45, 'End Turn')


def redrawWindow(win, player, buttons):
    win.fill((255, 255, 255))
    win.blit(bg, (0, 0))
    roll.draw(win)
    end_turn.draw(win)
    for p in board.players:
        win.blit(p.image, (p.x, p.y))
    for b in buttons:
        b[0].draw(win)
    pygame.display.update()


def create_landson_buttons(instr):
    buttons = [[button((0, 0, 0), 0, 855, 175, 45, 'Build'), build], [button((0, 0, 0), 175, 855, 175, 45, "Mortgage"), mortgage]]
    button_x = 350
    count = 0
    for i in instr:
        buttons.append([button((0, 0, 0), button_x, 855, 175, 45, instr[count][0]), instr[count][1]])
        button_x += 175
        count += 1
    return buttons


def main():
    buttons = []
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
                if roll.isOver(pos):
                    roll_dice(p1, board)
                    roll.text = f"Roll: {p1.roll}"
                    buttons = create_landson_buttons(lands_on(board.tiles[p1.location], p1, chance, comm_chest))
                    p1.rolled = True
                if end_turn.isOver(pos):
                    p1.rolled = False
                    change_player(board)
                    buttons = []
                for b in buttons:
                    if b[0].isOver(pos):
                        if b[0].text == "Build":
                            root = Tk()
                            my_gui = Popup(root, p1)
                            root.mainloop()
                        elif b[0].text == "Purchase":
                            purchase(p1, board.tiles[p1.location])

            # TODO: all the button hover and click events should be set to a loop or this will get huge
            if event.type == pygame.MOUSEMOTION:
                if roll.isOver(pos):
                    roll.color = (0, 255, 0)
                    roll.text_color = (0, 0, 0)
                else:
                    roll.color = (0, 0, 0)
                    roll.text_color = (255, 255, 255)
                if end_turn.isOver(pos):
                    end_turn.color = (0, 255, 0)
                    end_turn.text_color = (0, 0, 0)
                else:
                    end_turn.color = (0, 0, 0)
                    end_turn.text_color = (255, 255, 255)
                for b in buttons:
                    if b[0].isOver(pos):
                        b[0].color = (0, 255, 0)
                        b[0].text_color = (0, 0, 0)
                    else:
                        b[0].color = (0, 0, 0)
                        b[0].text_color = (255, 255, 255)

        redrawWindow(win, p1, buttons)


main()
