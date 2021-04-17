import pygame
from Controller import *

game = load_game()    # gets the tuple we pickled
board = game[0]       # gets board from tuple
comm_chest = game[1]  # gets shuffled deck of community chest cards
chance = game[2]      # gets shuffled deck of chance cards
create_player('player 1', 'Dog', board,770, 825, "images/dog.png", False)
p1 = board.players[0]
width = 860
height = 860
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Monopoly")
bg = pygame.image.load("images/bord.jpg")


def player_input(player: Player):
    key = pygame.key.get_pressed()
    if key[pygame.K_r] and not player.rolled:
        roll_dice(player)
    # this is only here for testing
    if key[pygame.K_x]:
        player.rolled = False


def redrawWindow(win, player):
    win.fill((255, 255, 255))
    win.blit(bg, (0, 0))
    win.blit(player.image, (player.x, player.y))
    pygame.display.update()


def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        player_input(p1)
        redrawWindow(win, p1)


main()
