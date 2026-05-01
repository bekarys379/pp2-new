import pygame
import math
from datetime import datetime

WIDTH, HEIGHT = 1000, 700
SIDEBAR_WIDTH = 200
CANVAS_SIZE = (WIDTH - SIDEBAR_WIDTH, HEIGHT)
CANVAS_OFFSET = (SIDEBAR_WIDTH, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint")

canvas = pygame.Surface(CANVAS_SIZE)
canvas.fill((255, 255, 255))

# -------------------------
# STATE
# -------------------------
tool = "brush"
color = (0, 0, 0)
drawing = False
start_pos = None
brush_sizes = {1: 2, 2: 5, 3: 10}
brush_size = brush_sizes[2]
last_pencil_pos = None
line_start = None

clock = pygame.time.Clock()

# -------------------------
# HELPERS
# -------------------------
def get_canvas_pos(pos):
    return (pos[0] - CANVAS_OFFSET[0], pos[1] - CANVAS_OFFSET[1])

def load_img(name, size):
    img = pygame.image.load(name).convert_alpha()
    return pygame.transform.scale(img, size)

# -------------------------
# LOAD IMAGES
# -------------------------
tool_size = (150, 40)

brush_img = load_img("brusher.png", tool_size)
eraser_img = load_img("eraser.png", tool_size)
rect_img = load_img("rect.png", tool_size)
circle_img = load_img("circle.png", tool_size)
rtria_img=load_img("rtria.png", tool_size)
eqtri_img=load_img("eqtri.png", tool_size)
rhomb_img=load_img("rhomb.png", tool_size)
pencil_img=load_img("pencil.jpg", tool_size)
line_img=load_img("line.png", tool_size)
fill_img=load_img("fill.png", tool_size)

# -------------------------
# BUTTONS
# -------------------------
red_btn = pygame.Rect(20, 50, 40, 40)
blue_btn = pygame.Rect(70, 50, 40, 40)
green_btn = pygame.Rect(120, 50, 40, 40)
black_btn = pygame.Rect(20, 100, 40, 40)

brush_btn = pygame.Rect(20, 200, 150, 40)
rect_btn = pygame.Rect(20, 250, 150, 40)
circle_btn = pygame.Rect(20, 300, 150, 40)
eraser_btn = pygame.Rect(20, 350, 150, 40)
right_tri_btn =pygame.Rect(20, 400, 150, 40)
equ_tri_btn =pygame.Rect(20, 450, 150, 40)
rhombus_btn =pygame.Rect(20, 500, 150, 40)
pencil_btn = pygame.Rect(20, 550, 150, 40)
line_btn = pygame.Rect(20, 600, 150, 40)
fill_btn = pygame.Rect(20, 650, 150, 40)


typing_text = ""
text_mode = False
text_pos = None
text_surface_preview = None
font = pygame.font.SysFont(None, 32)


#FILL

from collections import deque

def flood_fill(surface, x, y, new_color):
    width, height = surface.get_size()

    target_color = surface.get_at((x, y))

    if target_color == new_color:
        return

    queue = deque()
    queue.append((x, y))

    while queue:
        cx, cy = queue.popleft()

        if cx < 0 or cx >= width or cy < 0 or cy >= height:
            continue

        current_color = surface.get_at((cx, cy))

        if current_color != target_color:
            continue

        surface.set_at((cx, cy), new_color)

        queue.append((cx + 1, cy))
        queue.append((cx - 1, cy))
        queue.append((cx, cy + 1))
        queue.append((cx, cy - 1))


# -------------------------
# MAIN LOOP
# -------------------------
running = True
while running:

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                brush_size = brush_sizes[1]
            elif event.key == pygame.K_2:
                brush_size = brush_sizes[2]
            elif event.key == pygame.K_3:
                brush_size = brush_sizes[3]
            elif event.key == pygame.K_t:
                tool = "text"


            elif event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                filename = f"canvas_{timestamp}.png"
                pygame.image.save(canvas, filename)
                print(f"Saved as {filename}")

        # -------------------------
        # CLICK
        # -------------------------
        if event.type == pygame.MOUSEBUTTONDOWN:

            # COLORS
            if red_btn.collidepoint(event.pos):
                color = (255, 0, 0)
            elif blue_btn.collidepoint(event.pos):
                color = (0, 0, 255)
            elif green_btn.collidepoint(event.pos):
                color = (0, 255, 0)
            elif black_btn.collidepoint(event.pos):
                color = (0, 0, 0)

            # TOOLS
            elif brush_btn.collidepoint(event.pos):
                tool = "brush"
            elif rect_btn.collidepoint(event.pos):
                tool = "rect"
            elif circle_btn.collidepoint(event.pos):
                tool = "circle"
            elif eraser_btn.collidepoint(event.pos):
                tool = "eraser"
            elif right_tri_btn.collidepoint(event.pos):
                tool = "right_triangle"
            elif equ_tri_btn.collidepoint(event.pos):
                tool = "equilateral_triangle"
            elif rhombus_btn.collidepoint(event.pos):
                tool = "rhombus"
            elif pencil_btn.collidepoint(event.pos):
                tool = "pencil"
            elif line_btn.collidepoint(event.pos):
                tool = "line"
            elif fill_btn.collidepoint(event.pos):
                tool = "fill"


            if tool == "fill" and event.pos[0] > SIDEBAR_WIDTH:
                x, y = get_canvas_pos(event.pos)
                flood_fill(canvas, x, y, color)

            elif event.pos[0] > SIDEBAR_WIDTH:
                drawing = True
                start_pos = get_canvas_pos(event.pos)
                if tool == "pencil":
                    last_pencil_pos = start_pos
                    if tool == "line":
                        line_start = start_pos

            if tool == "text" and event.pos[0] > SIDEBAR_WIDTH:
                text_mode = True
                text_pos = get_canvas_pos(event.pos)
                typing_text = ""

        if event.type == pygame.KEYDOWN and text_mode:
            if event.key == pygame.K_RETURN:
                render_text = font.render(typing_text, True, color)
                canvas.blit(render_text, text_pos)
                text_mode = False
                typing_text = ""
            elif event.key == pygame.K_ESCAPE:
                text_mode = False
                typing_text = ""
            elif event.key == pygame.K_BACKSPACE:
                typing_text = typing_text[:-1]
            else:
                typing_text += event.unicode

    
        if event.type == pygame.MOUSEBUTTONUP:

            if drawing and start_pos:

                end_pos = get_canvas_pos(event.pos)

                if tool == "rect":
                    x = min(start_pos[0], end_pos[0])
                    y = min(start_pos[1], end_pos[1])
                    w = abs(end_pos[0] - start_pos[0])
                    h = abs(end_pos[1] - start_pos[1])
                    pygame.draw.rect(canvas, color, (x, y, w, h), brush_size)

                elif tool == "circle":
                    r=int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                    pygame.draw.circle(canvas, color, start_pos, r, brush_size)

                elif tool == "right_triangle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    pygame.draw.polygon(canvas, color, [(x1, y1), (x1, y2), (x2, y2)], brush_size)
                    
                elif tool == "equilateral_triangle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    base = x2 - x1
                    height = int(abs(base) * 0.866)  # √3 / 2
                    apex = (x1 + base // 2, y1 - height)
                    pygame.draw.polygon(canvas, color, [(x1, y1), (x2, y1), apex], brush_size)

                elif tool == "rhombus":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    dx = abs(x2 - x1) // 2
                    dy = abs(y2 - y1) // 2
                    pygame.draw.polygon(canvas, color, [(cx, y1), (x2, cy), (cx, y2), (x1, cy)], brush_size)

                elif tool == "line":
                    pygame.draw.line(canvas, color, start_pos, end_pos, brush_size)

            drawing = False
            start_pos = None
            last_pencil_pos=None

        # -------------------------
        # BRUSH / ERASER DRAW
        # -------------------------
        if event.type == pygame.MOUSEMOTION and drawing:
            pos = get_canvas_pos(event.pos)
            if tool in ("brush", "eraser"):
                draw_color = (255, 255, 255) if tool == "eraser" else color
                pygame.draw.circle(canvas, draw_color, pos, brush_size)
            elif tool == "pencil" and last_pencil_pos is not None:
                pygame.draw.line(canvas, color, last_pencil_pos, pos, brush_size)
                last_pencil_pos = pos

    # -------------------------
    # DRAW SCREEN
    # -------------------------
    screen.fill((60, 60, 60))
    screen.blit(canvas, CANVAS_OFFSET)

    # COLOR BUTTONS
    pygame.draw.rect(screen, (255, 0, 0), red_btn)
    pygame.draw.rect(screen, (0, 0, 255), blue_btn)
    pygame.draw.rect(screen, (0, 255, 0), green_btn)
    pygame.draw.rect(screen, (0, 0, 0), black_btn)

    # TOOL IMAGES
    screen.blit(brush_img, brush_btn.topleft)
    screen.blit(rect_img, rect_btn.topleft)
    screen.blit(circle_img, circle_btn.topleft)
    screen.blit(eraser_img, eraser_btn.topleft)
    screen.blit(rtria_img, right_tri_btn.topleft)
    screen.blit(eqtri_img, equ_tri_btn.topleft)
    screen.blit(rhomb_img, rhombus_btn.topleft)
    screen.blit(pencil_img, pencil_btn.topleft)
    screen.blit(line_img, line_btn.topleft)
    screen.blit(fill_img, fill_btn.topleft)



    # -------------------------
    # PREVIEW SHAPES
    # -------------------------
    if drawing and start_pos and tool in ("rect", "circle", "line"):

        curr = get_canvas_pos(mouse_pos)

        start_screen = (start_pos[0] + SIDEBAR_WIDTH, start_pos[1])
        curr_screen = (curr[0] + SIDEBAR_WIDTH, curr[1])

        if tool == "rect":
            x = min(start_screen[0], curr_screen[0])
            y = min(start_screen[1], curr_screen[1])
            w = abs(curr_screen[0] - start_screen[0])
            h = abs(curr_screen[1] - start_screen[1])
            pygame.draw.rect(screen, color, (x, y, w, h), 1)

        elif tool == "circle":
            r = int(math.hypot(curr_screen[0] - start_screen[0], curr_screen[1] - start_screen[1]))
            pygame.draw.circle(screen, color, start_screen, r, 1)

        elif tool == "line":
            start_screen = (start_pos[0] + SIDEBAR_WIDTH, start_pos[1])
            curr = get_canvas_pos(mouse_pos)
            curr_screen = (curr[0] + SIDEBAR_WIDTH, curr[1])
            pygame.draw.line(screen, color, start_screen, curr_screen, 1)

    pygame.display.flip()
    clock.tick(144)

pygame.quit()