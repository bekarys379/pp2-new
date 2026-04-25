import pygame
import math

WIDTH, HEIGHT = 1000, 700
SIDEBAR_WIDTH = 200
CANVAS_SIZE = (WIDTH - SIDEBAR_WIDTH, HEIGHT)
CANVAS_OFFSET = (SIDEBAR_WIDTH, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gemini Paint")


canvas = pygame.Surface(CANVAS_SIZE)
canvas.fill((255, 255, 255))


tool = "brush" 
color = (0, 0, 0)
drawing = False
start_pos = None
brush_size = 5

red_btn = pygame.Rect(20, 50, 40, 40)
blue_btn = pygame.Rect(70, 50, 40, 40)
green_btn = pygame.Rect(120, 50, 40, 40)
black_btn = pygame.Rect(20, 100, 40, 40)

brush_btn = pygame.Rect(20, 200, 150, 40)
rect_btn = pygame.Rect(20, 250, 150, 40)
circ_btn = pygame.Rect(20, 300, 150, 40)
eraser_btn = pygame.Rect(20, 350, 150, 40)

def get_canvas_pos(pos):
    return (pos[0] - CANVAS_OFFSET[0], pos[1] - CANVAS_OFFSET[1])

clock=pygame.time.Clock()
FPS=200

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
           
            if red_btn.collidepoint(event.pos): color = (255, 0, 0)
            elif blue_btn.collidepoint(event.pos): color = (0, 0, 255)
            elif green_btn.collidepoint(event.pos): color = (0, 255, 0)
            elif black_btn.collidepoint(event.pos): color = (0, 0, 0)
            
            elif brush_btn.collidepoint(event.pos): tool = "brush"
            elif rect_btn.collidepoint(event.pos): tool = "rect"
            elif circ_btn.collidepoint(event.pos): tool = "circle"
            elif eraser_btn.collidepoint(event.pos): tool = "eraser"

        
            elif event.pos[0] > SIDEBAR_WIDTH:
                drawing = True
                start_pos = get_canvas_pos(event.pos)

        if event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = get_canvas_pos(event.pos)
               
                if tool == "rect":
                    r_x = min(start_pos[0], end_pos[0])
                    r_y = min(start_pos[1], end_pos[1])
                    r_w = abs(end_pos[0] - start_pos[0])
                    r_h = abs(end_pos[1] - start_pos[1])
                    pygame.draw.rect(canvas, color, (r_x, r_y, r_w, r_h), 2)
                elif tool == "circle":
                    rad = int(math.hypot(end_pos[0]-start_pos[0], end_pos[1]-start_pos[1]))
                    pygame.draw.circle(canvas, color, start_pos, rad, 2)
                
                drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
            curr_pos = get_canvas_pos(event.pos)
            if tool == "brush":
                pygame.draw.circle(canvas, color, curr_pos, brush_size)
            elif tool == "eraser":
                pygame.draw.circle(canvas, (255, 255, 255), curr_pos, 20)

    
    screen.fill((60, 60, 60))
    
    screen.blit(canvas, CANVAS_OFFSET)

    
    pygame.draw.rect(screen, (255, 0, 0), red_btn)
    pygame.draw.rect(screen, (0, 0, 255), blue_btn)
    pygame.draw.rect(screen, (0, 255, 0), green_btn)
    pygame.draw.rect(screen, (0, 0, 0), black_btn)
    
    
    pygame.draw.rect(screen, (100, 100, 100) if tool=="brush" else (200, 200, 200), brush_btn)
    pygame.draw.rect(screen, (100, 100, 100) if tool=="rect" else (200, 200, 200), rect_btn)
    pygame.draw.rect(screen, (100, 100, 100) if tool=="circle" else (200, 200, 200), circ_btn)
    pygame.draw.rect(screen, (100, 100, 100) if tool=="eraser" else (200, 200, 200), eraser_btn)

    
    if drawing:
        curr = get_canvas_pos(mouse_pos)
        
        preview_start = (start_pos[0] + CANVAS_OFFSET[0], start_pos[1] + CANVAS_OFFSET[1])
        preview_curr = (curr[0] + CANVAS_OFFSET[0], curr[1] + CANVAS_OFFSET[1])
        
        if tool == "rect":
            r_x = min(preview_start[0], preview_curr[0])
            r_y = min(preview_start[1], preview_curr[1])
            r_w = abs(preview_curr[0] - preview_start[0])
            r_h = abs(preview_curr[1] - preview_start[1])
            pygame.draw.rect(screen, color, (r_x, r_y, r_w, r_h), 2)
        elif tool == "circle":
            rad = int(math.hypot(preview_curr[0]-preview_start[0], preview_curr[1]-preview_start[1]))
            pygame.draw.circle(screen, color, preview_start, rad, 2)

    pygame.display.flip()
    clock.tick(FPS)


pygame.quit()
