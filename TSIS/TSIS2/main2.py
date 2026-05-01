import pygame
import math

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
brush_size = 5
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

# -------------------------
# MAIN LOOP
# -------------------------
running = True
while running:

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

            # START DRAW
            elif event.pos[0] > SIDEBAR_WIDTH:
                drawing = True
                start_pos = get_canvas_pos(event.pos)
                if tool == "pencil":
                    last_pencil_pos = start_pos

    
        if event.type == pygame.MOUSEBUTTONUP:

            if drawing and start_pos:

                end_pos = get_canvas_pos(event.pos)

                if tool == "rect":
                    x = min(start_pos[0], end_pos[0])
                    y = min(start_pos[1], end_pos[1])
                    w = abs(end_pos[0] - start_pos[0])
                    h = abs(end_pos[1] - start_pos[1])
                    pygame.draw.rect(canvas, color, (x, y, w, h), 2)

                elif tool == "circle":
                    r=int(math.hypot(end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                    pygame.draw.circle(canvas, color, start_pos, r, 2)

                elif tool == "right_triangle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    pygame.draw.polygon(canvas, color, [(x1, y1), (x1, y2), (x2, y2)], 2)
                    
                elif tool == "equilateral_triangle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    base = x2 - x1
                    height = int(abs(base) * 0.866)  # √3 / 2
                    apex = (x1 + base // 2, y1 - height)
                    pygame.draw.polygon(canvas, color, [(x1, y1), (x2, y1), apex], 2)

                elif tool == "rhombus":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    dx = abs(x2 - x1) // 2
                    dy = abs(y2 - y1) // 2
                    pygame.draw.polygon(canvas, color, [(cx, y1), (x2, cy), (cx, y2), (x1, cy)], 2)

            drawing = False
            start_pos = None

        # -------------------------
        # BRUSH / ERASER DRAW
        # -------------------------
        if event.type == pygame.MOUSEMOTION and drawing:
            if tool in ("brush", "eraser"):

                pos = get_canvas_pos(event.pos)

                draw_color = (255, 255, 255) if tool == "eraser" else color
                pygame.draw.circle(canvas, draw_color, pos, brush_size)
                curr_pos = get_canvas_pos(event.pos)

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



    # -------------------------
    # PREVIEW SHAPES
    # -------------------------
    if drawing and start_pos and tool in ("rect", "circle"):

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

    pygame.display.flip()
    clock.tick(144)

pygame.quit()