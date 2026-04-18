import pygame
from ball import Ball

pygame.init()

screen=pygame.display.set_mode((500, 500))
pygame.display.set_caption("Moving Ball Game")

clock = pygame.time.Clock()

ball=Ball(250, 250)

running=True

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball.movement(-ball.speed, 0)
    if keys[pygame.K_RIGHT]:
        ball.movement(ball.speed, 0)
    if keys[pygame.K_UP]:
        ball.movement(0, -ball.speed)
    if keys[pygame.K_DOWN]:
        ball.movement(0, ball.speed)

    screen.fill((255, 255, 255))
    ball.draw(screen)

    pygame.display.flip()

pygame.quit()