import pygame
import time

class MickeyClock:
    def __init__(self):
        self.center = (400, 400)
        
        
        self.bg = pygame.image.load("images/mickeyclock2.jpg")
        self.bg = pygame.transform.scale(self.bg, (800, 800))

        self.sec_hand = pygame.image.load("images/left_hand.png").convert_alpha()
        self.min_hand = pygame.image.load("images/right_hand.png").convert_alpha()

        
        self.sec_hand = pygame.transform.scale(self.sec_hand, (140, 140))
        self.min_hand = pygame.transform.scale(self.min_hand, (220, 220))

    def rotate(self, image, angle):
        rotated = pygame.transform.rotate(image, angle)
        rect = rotated.get_rect(center=self.center)
        return rotated, rect

    def update(self, screen):
        t = time.localtime()
        seconds = t.tm_sec
        minutes = t.tm_min

        sec_angle = -seconds * 6
        min_angle = -minutes * 6

        sec_img, sec_rect = self.rotate(self.sec_hand, sec_angle)
        min_img, min_rect = self.rotate(self.min_hand, min_angle)

        screen.blit(self.bg, (0, 0))
        screen.blit(min_img, min_rect)
        screen.blit(sec_img, sec_rect)

        pygame.draw.circle(screen, (255, 0, 0), self.center, 5)