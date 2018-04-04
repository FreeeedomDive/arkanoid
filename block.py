class Block:
    x = y = 0
    top = bottom = left = right = 0
    color = "#800000"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.recount_coordinates()

    def recount_coordinates(self):
        self.top = self.y - 10
        self.bottom = self.y + 10
        self.left = self.x - 10
        self.right = self.x + 10

    def __str__(self):
        return str(self.x) + " " + str(self.y)
