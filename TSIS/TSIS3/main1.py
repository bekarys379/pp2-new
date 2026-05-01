import json
import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

BLUE =(0, 0, 255)
RED=(255, 0, 0)
GREEN=(255, 0, 0)
BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
YELLOW=(255,255,0)

SPEED = 8
SCORE = 0
NCOINS = 0
DG = 0
timer = 0

shield_active = False
shield_timer = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

screen = pygame.display.set_mode((800, 600))
screen.fill(WHITE)

bg = pygame.image.load("roadbg.png")
bg = pygame.transform.scale(bg, (800, 600))
bg_y = 0
clock = pygame.time.Clock()
FPS = 60

pygame.display.set_caption("Game")

running = True


# ================= ENEMY =================
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        og_image = pygame.image.load("enemycar.png")
        self.image = pygame.transform.scale(og_image, (50, 70))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, 750), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(50, 750), 0)


# ================= PLAYER =================
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        og_image = pygame.image.load("player.png")
        self.image = pygame.transform.scale(og_image, (40, 70))
        self.rect = self.image.get_rect()
        self.rect.center = (380, 530)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)

        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < 800 and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # ❌ removed auto movement (was breaking control)


# ================= COINS =================
class Coins(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        og_image1 = pygame.image.load("goldcoin1.png")
        og_image2 = pygame.image.load("silvercoin1.png")
        og_image3 = pygame.image.load("blackcoin.png")

        self.type = random.choice(["silver", "gold", "poison"])

        if self.type == "silver":
            self.image = pygame.transform.scale(og_image2, (70, 70))
        elif self.type == "gold":
            self.image = pygame.transform.scale(og_image1, (100, 100))
        else:
            self.image = pygame.transform.scale(og_image3, (70, 70))

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, 750), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(50, 750), 0)


# ================= OBSTACLE =================
class obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        og_image4 = pygame.image.load("oilspill.png")
        self.image = pygame.transform.scale(og_image4, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(200, 600), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(200, 600), 0)


# ================= BOOST =================
class Boost(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        og_image5 = pygame.image.load("nitro.png")
        self.image = pygame.transform.scale(og_image5, (30, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, 750), 0)

    def move(self):
        self.rect.move_ip(0, SPEED + 2)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(50, 750), 0)


class Shield(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        img = pygame.image.load("shield.png")
        self.image = pygame.transform.scale(img, (80, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, 750), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(50, 750), 0)


# ================= OBJECTS =================
P1 = Player()
E1 = Enemy()
C1 = Coins()
O1 = obstacle()
N1 = Boost()
S1 = Shield()

shields = pygame.sprite.Group(S1)
boosts = pygame.sprite.Group(N1)
coins = pygame.sprite.Group(C1)
enemies = pygame.sprite.Group(E1)
obstacles = pygame.sprite.Group(O1)

all_sprites = pygame.sprite.Group(P1, E1, C1, O1, N1, S1)


# ================= TIMERS =================
enemy_timer = 0
coin_timer = 0
obstacle_timer = 0
boost_timer = 300

def load_scores():
    try:
        with open("scores.json", "r") as f:
            return json.load(f)
    except:
        return []


def save_score(score):
    data = load_scores()
    data.append(score)
    data = sorted(data, reverse=True)[:10]
    with open("scores.json", "w") as f:
        json.dump(data, f)


def show_leaderboard():
    screen.fill(WHITE)
    font = pygame.font.SysFont("Verdana", 30)

    scores = load_scores()

    y = 100
    for i, s in enumerate(scores):
        text = font.render(f"{i+1}. Score: {s}", True, BLACK)
        screen.blit(text, (250, y))
        y += 40

    pygame.display.update()
    time.sleep(5)


# ================= GAME LOOP =================
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(bg, (0, bg_y))
    screen.blit(bg, (0, bg_y - 600))

    coinn = font_small.render(str(NCOINS), True, YELLOW)
    screen.blit(coinn, (760, 10))

    scores = font_small.render(str(SCORE), True, BLACK)
    screen.blit(scores, (10, 10))

    bg_y += SPEED / 2
    if bg_y >= 600:
        bg_y -= 600

    # FIXED: separate movement
    for entity in all_sprites:
        if entity != P1:
            entity.move()
    P1.move()

    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)

    # ================= COINS =================
    hits = pygame.sprite.spritecollide(P1, coins, True)
    for hit in hits:
        pygame.mixer.Sound('clink.wav').play()

        if hit.type == "silver":
            NCOINS += 1
        elif hit.type == "poison":
            NCOINS -= 1
        elif hit.type == "gold":
            NCOINS += 3

        new_c = Coins()
        coins.add(new_c)
        all_sprites.add(new_c)

    # ================= LEVEL =================
    level = NCOINS // 5 + 1
    SPEED = 5 + level * 0.5

    # ================= OBSTACLE =================
    if pygame.sprite.spritecollideany(P1, obstacles):
        SPEED -= 3

    # ================= BOOST =================
    hit = pygame.sprite.spritecollideany(P1, boosts)
    if hit:
        hit.kill()
        timer = 180

    if timer > 0:
        SPEED = 10
        timer -= 1

    # ================= SHIELD =================
    hit = pygame.sprite.spritecollideany(P1, shields)
    if hit:
        hit.kill()
        shield_timer = 300
        shield_active = True

    if shield_timer > 0:
        shield_timer -= 1
    else:
        shield_active = False

    if shield_active:
        pygame.draw.ellipse(screen, (0, 200, 255), P1.rect.inflate(30, 30), 3)

    # ================= ENEMY =================
    hit_enemy = pygame.sprite.spritecollideany(P1, enemies)
    if hit_enemy:
        if shield_active:
            hit_enemy.kill()
        else:
            print("SAVING SCORE:", SCORE)
            pygame.mixer.Sound('crash.wav').play()
            time.sleep(0.5)
  
            save_score(SCORE)
            screen.fill(RED)
            screen.blit(game_over, (30, 250))
            pygame.display.update()
            show_leaderboard() 
            time.sleep(2)
            pygame.quit()
            sys.exit()

    # ================= SPAWN =================
    enemy_timer -= 1
    if enemy_timer <= 0:
        new_enemy = Enemy()
        enemies.add(new_enemy)
        all_sprites.add(new_enemy)
        enemy_timer = max(20, 80 - level * 5)
    
    pygame.display.flip()
    clock.tick(FPS)