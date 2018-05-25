import random


class Ball:

    def __init__(self, screen_width, screen_height, x=-1, y=-1, sp0=-1,
                 sp1=-1, start=-1, power=1):
        self.screen_width = screen_width
        if x == -1:
            self.x = random.randint(40, screen_width - 40)
            self.start_y = self.y = screen_height - 60
            self.speed = [1, -1]
            self.power = 1
        else:
            self.x = x
            self.y = y
            self.speed = [sp0, sp1]
            self.start_y = start
            self.power = power
        self.basic_speed = 1
        self.top = self.y - 10
        self.bottom = self.y + 10
        self.left = self.x - 10
        self.right = self.x + 10
        self.color = "#c8ff00"

    def get_side_of_intersection(self, obj):
        if self.top == obj.bottom:
            return "top"
        if self.bottom == obj.top:
            return "bottom"
        if self.left == obj.right:
            return "left"
        if self.right == obj.left:
            return "right"

    # def __init__(self, x, y, speed0, speed1, start):
    #     self.x = x
    #     self.y = y
    #     self.start_y = start
    #     self.top = self.y - 10
    #     self.bottom = self.y + 10
    #     self.left = self.x - 10
    #     self.right = self.x + 10
    #     self.basic_speed = 1
    #     self.speed = [speed0, speed1]
    #     self.color = "#c8ff00"

    def move(self):
        self.x += self.speed[0]
        self.y += self.speed[1]
        self.recount_coordinates()

    def reincarnate(self):
        self.x = random.randint(20, self.screen_width - 20)
        self.y = self.start_y
        self.recount_coordinates()
        self.basic_speed = 1
        self.speed = [1, -1]

    def recount_coordinates(self):
        self.top = self.y - 10
        self.bottom = self.y + 10
        self.left = self.x - 10
        self.right = self.x + 10
