import pygame, sys
import random
import time
from db import get_or_create_player, save_session, get_leaderboard, connect

# --- Initialize Pygame ---
pygame.init()

# --- Configuration & Constants ---
CELL = 20
WIDTH, HEIGHT = 600, 600
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
RED = (255, 50, 50)      # Normal Food
GOLD = (255, 215, 0)     # Strong Food / High Score
PURPLE = (160, 32, 240)  # Poison
GREEN = (0, 255, 100)    # Snake
CYAN = (0, 255, 255)     # Shield
BLUE = (50, 50, 255)     # Speed/Slow Powerups
GREY = (100, 100, 100)   # Obstacles

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake: Level 3 Obstacles Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)
large_font = pygame.font.SysFont("Arial", 36)

# --- Database & Helper Logic ---
def get_personal_best(player_id):
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute("SELECT MAX(score) FROM game_sessions WHERE player_id=%s", (player_id,))
        best = cur.fetchone()[0]
        conn.close()
        return best if best is not None else 0
    except:
        return 0

def generate_obstacles(level, snake_body):
    """Creates a list of wall positions starting at Level 3."""
    obstacles = []
    if level < 3:
        return obstacles
    
    # Increase number of blocks as level goes up
    num_blocks = (level - 2) * 5 
    while len(obstacles) < num_blocks:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        pos = (x, y)
        
        # Guardrails: Don't spawn walls on snake OR right in front of head (3-cell buffer)
        head_x, head_y = snake_body[0]
        is_near_head = abs(x - head_x) < CELL * 3 and abs(y - head_y) < CELL * 3
        
        if pos not in snake_body and not is_near_head and pos not in obstacles:
            obstacles.append(pos)
    return obstacles

# --- Game Classes ---

class Snake:
    def __init__(self):
        self.body = [(100, 100), (80, 100), (60, 100)]
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

    def check_collision(self, obstacles):
        head_x, head_y = self.body[0]
        # Wall/Obstacle/Self collision
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            return True
        if self.body[0] in self.body[1:]:
            return True
        if self.body[0] in obstacles:
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
    def __init__(self, snake):
        self.snake = snake
        self.position = (0,0)
        self.type = "normal"
        self.spawn_time = 0

    def respawn(self, obstacles):
        while True:
            pos = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
            if pos not in self.snake.body and pos not in obstacles:
                self.position = pos
                self.spawn_time = time.time()
                self.type = random.choice(["normal", "normal", "strong", "poison"])
                break

    def is_expired(self):
        return time.time() - self.spawn_time > 8

class PowerUp:
    def __init__(self, snake):
        self.snake = snake
        self.exists = False
        self.type = None
        self.position = None
        self.spawn_time = 0

    def spawn(self, obstacles):
        while True:
            pos = (random.randrange(0, WIDTH, CELL), random.randrange(0, HEIGHT, CELL))
            if pos not in self.snake.body and pos not in obstacles:
                self.position = pos
                self.type = random.choice(["speed", "slow", "shield"])
                self.spawn_time = pygame.time.get_ticks()
                self.exists = True
                break

# --- UI Screens ---

def get_username():
    input_text = ""
    while True:
        screen.fill(BLACK)
        txt = large_font.render("Enter Username:", True, WHITE)
        val = font.render(input_text + "_", True, GREEN)
        screen.blit(txt, (WIDTH//2 - 120, HEIGHT//2 - 60))
        screen.blit(val, (WIDTH//2 - 40, HEIGHT//2))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and input_text: return input_text
                elif event.key == pygame.K_BACKSPACE: input_text = input_text[:-1]
                else: 
                    if len(input_text) < 12: input_text += event.unicode

def show_leaderboard():
    leaders = get_leaderboard()
    while True:
        screen.fill(BLACK)
        title = large_font.render("LEADERBOARD", True, GOLD)
        screen.blit(title, (WIDTH//2 - 100, 50))
        
        for i, row in enumerate(leaders):
            entry = font.render(f"{i+1}. {row[0]:<12} {row[1]:<5} Lvl:{row[2]}", True, WHITE)
            screen.blit(entry, (WIDTH//2 - 150, 120 + i * 30))
            
        msg = font.render("SPACE to Restart | ESC to Quit", True, CYAN)
        screen.blit(msg, (WIDTH//2 - 140, HEIGHT - 80))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: return True
                if event.key == pygame.K_ESCAPE: return False

# --- Main Game Loop ---

def play_game(player_id, pb_score):
    snake = Snake()
    obstacles = []
    food = Food(snake)
    food.respawn(obstacles)
    powerup = PowerUp(snake)
    
    score = 0
    level = 1
    last_level_gen = 0 # Track when to rebuild walls
    base_speed = 10
    
    active_effect = None
    effect_end_time = 0
    has_shield = False
    
    running = True
    while running:
        now = pygame.time.get_ticks()
        
        # 1. Level & Obstacle Logic
        level = (score // 5) + 1
        if level != last_level_gen:
            obstacles = generate_obstacles(level, snake.body)
            last_level_gen = level
            base_speed = 10 + (level * 2)
            # Ensure food didn't spawn inside a new wall
            if food.position in obstacles: food.respawn(obstacles)

        # 2. Speed Logic
        current_fps = base_speed
        if active_effect == "speed" and now < effect_end_time:
            current_fps += 10
        elif active_effect == "slow" and now < effect_end_time:
            current_fps = max(5, base_speed - 5)
        else:
            active_effect = None 
            
        clock.tick(current_fps)

        # 3. Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: snake.change_direction("UP")
                if event.key == pygame.K_DOWN: snake.change_direction("DOWN")
                if event.key == pygame.K_LEFT: snake.change_direction("LEFT")
                if event.key == pygame.K_RIGHT: snake.change_direction("RIGHT")

        # 4. Movement
        snake.move()
        
        # Collision Check
        if snake.check_collision(obstacles):
            if has_shield:
                has_shield = False # Shield saves you
                snake.body.pop(0)  # Stop head from sitting inside the wall
            else:
                running = False

        # 5. Food Interaction
        if food.is_expired(): food.respawn(obstacles)
        if snake.body[0] == food.position:
            if food.type == "poison":
                score = max(0, score - 1)
                if len(snake.body) > 2: snake.body.pop()
            else:
                score += 2 if food.type == "strong" else 1
                snake.grow_next = True
                if food.type == "strong": snake.grow_next = True
            food.respawn(obstacles)
            
        # 6. Powerup Interaction
        if not powerup.exists and random.random() < 0.02:
            powerup.spawn(obstacles)
        if powerup.exists:
            if now - powerup.spawn_time > 8000: powerup.exists = False
            elif snake.body[0] == powerup.position:
                if powerup.type == "shield": has_shield = True
                else:
                    active_effect = powerup.type
                    effect_end_time = now + 5000
                powerup.exists = False

        # 7. Rendering
        screen.fill(BLACK)
        
        # Draw Walls
        for wall in obstacles:
            pygame.draw.rect(screen, GREY, (*wall, CELL-1, CELL-1))
        
        # Draw Snake
        for i, seg in enumerate(snake.body):
            color = GREEN if i > 0 else (WHITE if not has_shield else CYAN)
            pygame.draw.rect(screen, color, (*seg, CELL-2, CELL-2))
            
        # Draw Food
        f_color = RED if food.type=="normal" else (GOLD if food.type=="strong" else PURPLE)
        pygame.draw.rect(screen, f_color, (*food.position, CELL-2, CELL-2))
        
        # Draw Powerup
        if powerup.exists:
            p_color = CYAN if powerup.type == "shield" else BLUE
            pygame.draw.circle(screen, p_color, (powerup.position[0]+CELL//2, powerup.position[1]+CELL//2), CELL//2)

        # UI
        screen.blit(font.render(f"Score: {score}  Lvl: {level}", True, WHITE), (10, 10))
        screen.blit(font.render(f"PB: {max(score, pb_score)}", True, GOLD), (WIDTH-100, 10))
        if active_effect:
            screen.blit(font.render(f"{active_effect.upper()} ACTIVE", True, BLUE), (WIDTH//2-50, 10))

        pygame.display.update()

    save_session(player_id, score, level)

def main():
    user = get_username()
    p_id = get_or_create_player(user)
    while True:
        pb = get_personal_best(p_id)
        play_game(p_id, pb)
        if not show_leaderboard(): break
    pygame.quit()

if __name__ == "__main__":
    main()