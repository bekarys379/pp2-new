import pygame
import math


def drawLine(screen, start, end, width, color):
    dx = start[0] - end[0]
    dy = start[1] - end[1]
    steps = max(abs(dx), abs(dy))

    if steps == 0:
        return

    for i in range(steps):
        t = i / steps
        x = int((1 - t) * start[0] + t * end[0])
        y = int((1 - t) * start[1] + t * end[1])
        pygame.draw.circle(screen, color, (x, y), width)


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()

    tool = "brush"
    color = (0, 0, 255)

    drawing = False
    start_pos = None

    points = []
    radius = 5

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return

            # KEY CONTROLS
            if event.type == pygame.KEYDOWN:

                # tools
                if event.key == pygame.K_1:
                    tool = "brush"
                elif event.key == pygame.K_2:
                    tool = "rect"
                elif event.key == pygame.K_3:
                    tool = "circle"
                elif event.key == pygame.K_4:
                    tool = "eraser"
                elif event.key == pygame.K_5:
                    tool = "square"
                elif event.key == pygame.K_6:
                    tool = "right_triangle"
                elif event.key == pygame.K_7:
                    tool = "equilateral_triangle"
                elif event.key == pygame.K_8:
                    tool = "rhombus"

                # colors
                elif event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                elif event.key == pygame.K_y:
                    color = (255, 255, 0)
                elif event.key == pygame.K_w:
                    color = (255, 255, 255)

                elif event.key == pygame.K_ESCAPE:
                    return

            # mouse down
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos

            # mouse up → shape creation
            if event.type == pygame.MOUSEBUTTONUP:
                drawing = False
                end_pos = event.pos

                x1, y1 = start_pos
                x2, y2 = end_pos

                # RECTANGLE
                if tool == "rect":
                    pygame.draw.rect(screen, color,
                                     (min(x1, x2), min(y1, y2),
                                      abs(x2 - x1), abs(y2 - y1)), 2)

                # SQUARE
                elif tool == "square":
                    size = min(abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(screen, color,
                                     (x1, y1, size, size), 2)

                # CIRCLE
                elif tool == "circle":
                    r = int(math.hypot(x2 - x1, y2 - y1))
                    pygame.draw.circle(screen, color, start_pos, r, 2)

                # RIGHT TRIANGLE
                elif tool == "right_triangle":
                    pygame.draw.polygon(screen, color, [
                        (x1, y1),
                        (x2, y1),
                        (x1, y2)
                    ], 2)

                # EQUILATERAL TRIANGLE
                elif tool == "equilateral_triangle":
                    side = x2 - x1
                    height = int((math.sqrt(3) / 2) * side)

                    pygame.draw.polygon(screen, color, [
                        (x1, y1),
                        (x1 + side, y1),
                        (x1 + side // 2, y1 - height)
                    ], 2)

                # RHOMBUS
                elif tool == "rhombus":
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2

                    pygame.draw.polygon(screen, color, [
                        (cx, y1),
                        (x2, cy),
                        (cx, y2),
                        (x1, cy)
                    ], 2)

            # brush + eraser
            if event.type == pygame.MOUSEMOTION:
                if drawing:

                    if tool == "brush":
                        points.append(event.pos)
                        points = points[-256:]

                    elif tool == "eraser":
                        pygame.draw.circle(screen, (0, 0, 0), event.pos, 20)

        # redraw
        screen.fill((0, 0, 0))

        for i in range(len(points) - 1):
            drawLine(screen, points[i], points[i + 1], radius, color)

        pygame.display.flip()
        clock.tick(60)


main()