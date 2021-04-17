import pygame

width = 860
height = 860
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Monopoly")
bg = pygame.image.load("bord.jpg")
# img = pygame.image.load('monopoly_token_car.png')


def redrawWindow(win):
    win.fill((255, 255, 255))
    win.blit(bg, (0, 0))
    pygame.display.update()


def main():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        redrawWindow(win)


main()
