import pygame
from clock import MickeyClock

pygame.init()

screen = pygame.display.set_mode((800, 800))
clock = pygame.time.Clock()

mickey = MickeyClock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    mickey.update(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()