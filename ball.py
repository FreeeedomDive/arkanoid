class Ball:
    x = y = 0
    top = bottom = left = right = 0
    speed = [1, -1]
    color = "#c8ff00"
    start_x = start_y = 0

    def __init__(self, screen_width, screen_height):
        self.start_x = self.x = screen_width / 2
        self.start_y = self.y = screen_height - 50
        self.recount_coordinates()

    def dead(self):
        self.x = self.start_x
        self.y = self.start_y
        self.recount_coordinates()
        self.speed = [1, -1]

    def recount_coordinates(self):
        self.top = self.y - 10
        self.bottom = self.y + 10
        self.left = self.x - 10
        self.right = self.x + 10
