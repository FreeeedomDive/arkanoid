import random


class Ball:

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.x = random.randint(20, screen_width - 20)
        self.start_y = self.y = screen_height - 50
        self.top = self.y - 10
        self.bottom = self.y + 10
        self.left = self.x - 10
        self.right = self.x + 10
        self.speed = [1, -1]
        self.color = "#c8ff00"

    def move(self):
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.recount_coordinates()

    def reincarnate(self):
        self.x = random.randint(20, self.screen_width - 20)
        self.y = self.start_y
        self.recount_coordinates()
        self.speed = [1, -1]

    def recount_coordinates(self):
        self.top = self.y - 10
        self.bottom = self.y + 10
        self.left = self.x - 10
        self.right = self.x + 10
