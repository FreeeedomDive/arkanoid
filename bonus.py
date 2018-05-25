import pygame


class Bonus:

    images = {
        "powerup": "Images/powerup.png",
        "platform_more": "Images/platform_more.png",
        "platform_less": "Images/platform_less.png"
    }

    def __init__(self, name, x, y):
        self.name = name
        self.image = pygame.image.load(self.images[name])
        self.x = x
        self.y = y
        self.speed = [0, 1]
