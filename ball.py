class Ball:
    x = y = 0
    speed = [1, -1]
    color = "#c8ff00"
    start_x = start_y = 0

    def __init__(self, screen_width, screen_height):
        self.start_x = self.x = screen_width / 2
        self.start_y = self.y = screen_height - 50

    def dead(self):
        self.x = self.start_x
        self.y = self.start_y
        self.speed = [1, -1]
