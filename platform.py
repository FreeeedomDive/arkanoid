class Platform:
    MOVE_SPEED = 1
    HEIGHT = 20
    WIDTH = 180
    COLOR = "#789ABC"
    LEFT_COORD = 0
    RIGHT_COORD = LEFT_COORD + WIDTH
    MOVING_LEFT = False
    MOVING_RIGHT = False

    def __init__(self, screen_width):
        self.LEFT_COORD = screen_width / 2 - self.WIDTH / 2
        self.RIGHT_COORD = self.LEFT_COORD + self.WIDTH
        self.MOVE_SPEED = screen_width / 1250
        self.WIDTH = screen_width / 5
