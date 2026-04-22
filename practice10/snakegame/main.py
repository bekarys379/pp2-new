import pygame, sys
import random

pygame.init()

CELL = 10
WIDTH, HEIGHT = 500, 500
score=0
level=1
speed=10
fpl=3
font=pygame.font.SysFont(None, 30)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake game")
clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.body = [(100, 100), (90, 100), (80, 100)]
        self.direction = (CELL, 0)
        self.grow_next = False

    def move(self):
        head_x, head_y = self.body[0]
        dx, dy = self.direction

        new_head = (head_x + dx, head_y + dy)

        self.body.insert(0, new_head)
        if not self.grow_next:
            self.body.pop()
        else:
            self.grow_next = False

    def checkcollision(self, width, height):
        head_x, head_y = self.body[0]

        if (head_x < 0 or head_x >= width or
            head_y < 0 or head_y >= height):
            return True

        if self.body[0] in self.body[1:]:
            return True

        return False

    def change_direction(self, key):
        if key == "UP" and self.direction != (0, CELL):
            self.direction = (0, -CELL)
        elif key == "DOWN" and self.direction != (0, -CELL):
            self.direction = (0, CELL)
        elif key == "LEFT" and self.direction != (CELL, 0):
            self.direction = (-CELL, 0)
        elif key == "RIGHT" and self.direction != (-CELL, 0):
            self.direction = (CELL, 0)


class Food:
    def __init__(self, width, height, cell, snake):
        self.width = width
        self.height = height
        self.cell = cell
        self.snake = snake
        self.respawn()

    def respawn(self):
        while True:
            pos = (
                random.randrange(0, self.width, self.cell),
                random.randrange(0, self.height, self.cell)
            )
            if pos not in self.snake.body:
                self.position = pos
                break



snake = Snake()
food = Food(WIDTH, HEIGHT, CELL, snake)

running=True
last_level=1

while running:
    clock.tick(speed)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction("UP")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("DOWN")
            elif event.key == pygame.K_LEFT:
                snake.change_direction("LEFT")
            elif event.key == pygame.K_RIGHT:
                snake.change_direction("RIGHT")

    snake.move()

    if snake.body[0] == food.position:
        food.respawn()
        snake.grow_next = True
        score += 1

    level = score // fpl + 1
    if level != last_level:
        speed += 2
        last_level = level

    if snake.checkcollision(WIDTH, HEIGHT):
        running = False

    # DRAW
    screen.fill(BLACK)

    for segment in snake.body:
        pygame.draw.rect(screen, GREEN, (*segment, CELL, CELL))

    pygame.draw.rect(screen, RED, (*food.position, CELL, CELL))

    # UI update (IMPORTANT)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    level_text = font.render(f"Level: {level}", True, (255, 255, 255))

    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (10, 40))

    pygame.display.update()