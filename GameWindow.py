import pygame
from Controller import *

pygame.init()
game = load_game()    # gets the tuple we pickled
board = game[0]       # gets board from tuple
comm_chest = game[1]  # gets shuffled deck of community chest cards
chance = game[2]      # gets shuffled deck of chance cards
create_player('player 1', 'Dog', board, 770, 825, "images/dog.png", False)
p1 = board.players[0]
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


roll = button((0, 0, 0), 755, 855, 100, 45, 'Roll:')


def redrawWindow(win, player):
    win.fill((255, 255, 255))
    win.blit(bg, (0, 0))
    roll.draw(win)
    # win.blit(roll_display.textsurface, roll_display.textRect)
    win.blit(player.image, (player.x, player.y))
    pygame.display.update()


def main():
    run = True
    while run:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if roll.isOver(pos):
                    assert isinstance(p1, Player)
                    roll_dice(p1, board)
                    roll.text = f"Roll: {p1.roll}"
                    p1.rolled = False
            if event.type == pygame.MOUSEMOTION:
                if roll.isOver(pos):
                    roll.color = (0, 255, 0)
                    roll.text_color = (0, 0, 0)
                else:
                    roll.color = (0, 0, 0)
                    roll.text_color = (255, 255, 255)

        redrawWindow(win, p1)


main()
