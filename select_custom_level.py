import pygame
import os
import sys
import game
import menu


class CustomLevelSelector:
    def __init__(self):
        self.levels = os.listdir("./CreatedLevels")
        self.cursor = 0
        height = 30
        if len(self.levels) > 0:
            height = len(self.levels) * 20
        self.display = (320, height)
        self.screen = pygame.display.set_mode(self.display)
        self.bg = pygame.Surface(self.display)
        self.timer = pygame.time.Clock()
        self.draw()

    def draw(self):
        pygame.init()
        pygame.display.set_caption("Created levels")
        self.bg.fill(pygame.Color("#14005e"))
        while True:
            self.timer.tick(200)
            self.screen.blit(self.bg, (0, 0))
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()

                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    menu.Menu()

                if e.type == pygame.KEYDOWN and e.key == pygame.K_UP:
                    if 0 < self.cursor:
                        self.cursor -= 1

                if e.type == pygame.KEYDOWN and e.key == pygame.K_DOWN:
                    if self.cursor < len(self.levels) - 1:
                        self.cursor += 1

                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    g = game.Game(map="CreatedLevels/" +
                                      self.levels[self.cursor])
                    g.start()

                if e.type == pygame.KEYDOWN and e.key == pygame.K_DELETE:
                    delete = self.levels[self.cursor]
                    self.levels.remove(delete)
                    os.remove("./CreatedLevels/" + delete)
            font = pygame.font.Font(None, 20)
            if len(self.levels) == 0:
                text = font.render("No levels", True, (255, 0, 0))
                self.screen.blit(text, [10, 10])
            else:
                y = 5
                for i in range(0, len(self.levels)):
                    color = (255, 255, 255)
                    if i == self.cursor:
                        color = (0, 255, 0)
                    text = font.render(self.levels[i], True, color)
                    self.screen.blit(text, [10, y])
                    y += 20

            pygame.display.update()
