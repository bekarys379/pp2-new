import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

BLUE =(0, 0, 255)
RED=(255, 0, 0)
GREEN=(0, 255, 0)
BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
YELLOW=(255,255,0)

SPEED = 5
SCORE = 0
NCOINS=0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

screen=pygame.display.set_mode((800, 600))
screen.fill(WHITE)

bg=pygame.image.load("roadbg.png")
bg=pygame.transform.scale(bg, (800, 600))

clock=pygame.time.Clock()
FPS=60

pygame.display.set_caption("Game")

running=True

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        og_image=pygame.image.load("enemycar.png")
        self.image=pygame.transform.scale(og_image, (50, 70))
        self.rect=self.image.get_rect()
        self.rect.center=(random.randint(50, 750), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if(self.rect.top>600):
            SCORE+=1
            self.rect.top=0
            self.rect.center=(random.randint(50, 750), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        og_image=pygame.image.load("player.png")
        self.image=pygame.transform.scale(og_image, (40, 70))
        self.rect=self.image.get_rect()
        self.rect.center=(380, 530)

    def move(self):

        self.rect.move_ip(0, 2)
        pressed_keys=pygame.key.get_pressed()
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)

        if self.rect.left>0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right<800:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

class Coins(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        og_image=pygame.image.load("coin.png")
        self.image=pygame.transform.scale(og_image, (30, 30))
        self.rect=self.image.get_rect()
        self.rect.center=(random.randint(50, 750), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if(self.rect.top>600):
            self.rect.top=0
            self.rect.center=(random.randint(50, 750), 0)



P1=Player()
E1=Enemy()
C1=Coins()
coins=pygame.sprite.Group()
coins.add(C1)
enemies=pygame.sprite.Group()
enemies.add(E1)
all_sprites=pygame.sprite.Group()
all_sprites.add(E1)
all_sprites.add(P1)
all_sprites.add(C1)


INC_SPEED=pygame.USEREVENT+1
pygame.time.set_timer(INC_SPEED, 1000)


while running:
    for event in pygame.event.get():
        if event.type==INC_SPEED:
            SPEED+=0.5
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.blit(bg, (0, 0))
    coinn=font_small.render(str(NCOINS), True, YELLOW)
    screen.blit(coinn, (760, 10))
    scores=font_small.render(str(SCORE), True, BLACK)
    screen.blit(scores, (10, 10))

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    hits=pygame.sprite.spritecollide(P1, coins, True)
    for hit in hits:
        pygame.mixer.Sound('clink.wav').play()
        NCOINS += 1
        new_c = Coins()
        coins.add(new_c)
        all_sprites.add(new_c)

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(0.5)
                    
        screen.fill(RED)
        screen.blit(game_over, (30,250))
           
        pygame.display.update()
        for entity in all_sprites:
            entity.kill() 
        time.sleep(2)
        pygame.quit()
        sys.exit()  

    pygame.display.flip()
    clock.tick(FPS)
