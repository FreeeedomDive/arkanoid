import pygame as pg
import random


class Block:

    bonuses = [
        "powerup",
        "platform_more",
        "platform_less",
        "destroy_line"
    ]

    def __init__(self, x, y, str, bonus=None):
        self.x = x
        self.y = y
        if bonus is None:
            chance = random.randint(0, 14)
            if chance == 10:
                self.bonus = \
                    self.bonuses[random.randint(0, len(self.bonuses) - 1)]
            else:
                self.bonus = None
        else:
            self.bonus = bonus
        self.top = self.y - 10
        self.bottom = self.y + 10
        self.left = self.x - 10
        self.right = self.x + 10
        self.strength = str
        file_name = "Images/block{0}.png".format(self.strength)
        self.image = pg.image.load(file_name)

    def recount_coordinates(self):
        self.top = self.y - 10
        self.bottom = self.y + 10
        self.left = self.x - 10
        self.right = self.x + 10

    def decrease_and_check_destroying(self, power):
        self.strength -= power
        if self.strength <= 0:
            return True
        else:
            file_name = "Images/block{0}.png".format(self.strength)
            self.image = pg.image.load(file_name)
            return False

    def draw(self, screen):
        screen.blit(self.image, (self.left, self.top))

    def __str__(self):
        return str(self.x) + " " + str(self.y)
