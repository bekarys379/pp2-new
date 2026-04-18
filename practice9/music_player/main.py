import pygame
from player import MusicPlayer

pygame.init()

screen = pygame.display.set_mode((500, 300))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont("Arial", 24)

player = MusicPlayer("music")

running = True
clock = pygame.time.Clock()

while running:
    screen.fill((20, 20, 20))

    # Text display
    track_text = font.render("Track: " + player.current_track_name(), True, (255, 255, 255))
    screen.blit(track_text, (20, 50))

    info = font.render("P=Play S=Stop N=Next B=Back Q=Quit", True, (180, 180, 180))
    screen.blit(info, (20, 120))

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

            elif event.key == pygame.K_p:
                player.play()

            elif event.key == pygame.K_s:
                player.stop()

            elif event.key == pygame.K_n:
                player.next_track()

            elif event.key == pygame.K_b:
                player.prev_track()

    clock.tick(30)

pygame.quit()