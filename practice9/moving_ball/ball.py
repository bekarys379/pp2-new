import pygame

class Ball():
    def __init__(self, x, y, radius=25, speed=20, width=400, height=300):
        self.x=x
        self.y=y
        self.radius=radius
        self.width=width
        self.speed=speed
        self.height=height

    def movement(self, dx, dy):
        nx=self.x+dx
        ny=self.y+dy

        if self.radius<=nx<=self.width-self.radius:
            self.x = nx

        if self.radius<=ny<=self.height-self.radius:
            self.y=ny


    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.radius)


