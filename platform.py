import pygame as pg


class Platform:

    def __init__(self, screen_width, left=-1, width=-1):
        self.MOVING_LEFT = False
        self.MOVING_RIGHT = False
        self.COLOR = "#789ABC"
        self.HEIGHT = 20
        if width == -1:
            self.WIDTH = screen_width / 4
        else:
            self.WIDTH = width
        if left == -1:
            self.LEFT_COORD = screen_width / 2 - self.WIDTH / 2
        else:
            self.LEFT_COORD = left
        self.RIGHT_COORD = self.LEFT_COORD + self.WIDTH
        self.MOVE_SPEED = screen_width / 250

    def move(self, rotation):
        self.LEFT_COORD += rotation * self.MOVE_SPEED
        self.RIGHT_COORD += rotation * self.MOVE_SPEED

    def draw(self, screen, height):
        pf = pg.Surface((self.WIDTH, 20))
        pf.fill(pg.Color(self.COLOR))
        screen.blit(pf, (self.LEFT_COORD, height - 40))
