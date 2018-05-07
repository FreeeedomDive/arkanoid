import pygame as pg


class Block(pg.sprite.Sprite):

    def __init__(self, x, y, str):
        super().__init__()
        self.x = x
        self.y = y
        self.top = self.y - 10
        self.bottom = self.y + 10
        self.left = self.x - 10
        self.right = self.x + 10
        self.strength = str
        file_name = "Images/block{0}.png".format(self.strength)
        self.image = pg.image.load(file_name)
        self.color = "#800000"

    def recount_coordinates(self):
        self.top = self.y - 10
        self.bottom = self.y + 10
        self.left = self.x - 10
        self.right = self.x + 10

    def decrease_and_check_destroying(self):
        self.strength -= 1
        if self.strength == 0:
            return True
        else:
            file_name = "Images/block{0}.png".format(self.strength)
            self.image = pg.image.load(file_name)
            return False

    def draw(self, screen):
        screen.blit(self.image, (self.left, self.top))

    def __str__(self):
        return str(self.x) + " " + str(self.y)
