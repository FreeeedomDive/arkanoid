import pygame
import os
import sys
import game
import menu


class SaveSelector:
    def __init__(self):
        self.saves = os.listdir("./Saves")
        self.cursor = 0
        height = 30
        if len(self.saves) > 0:
            height = len(self.saves) * 20
        self.display = (320, height)
        self.screen = pygame.display.set_mode(self.display)
        self.bg = pygame.Surface(self.display)
        self.timer = pygame.time.Clock()
        self.draw()

    def draw(self):
        pygame.init()
        pygame.display.set_caption("Saves")
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
                    if self.cursor < len(self.saves) - 1:
                        self.cursor += 1

                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    saved = open("Saves/" + self.saves[self.cursor], 'r')
                    g = game.Game(f=saved.read())
                    saved.close()
                    g.start()

                if e.type == pygame.KEYDOWN and e.key == pygame.K_DELETE:
                    delete = self.saves[self.cursor]
                    self.saves.remove(delete)
                    os.remove("./Saves/" + delete)
            font = pygame.font.Font(None, 20)
            if len(self.saves) == 0:
                text = font.render("No saves", True, (255, 0, 0))
                self.screen.blit(text, [10, 10])
            else:
                y = 5
                for i in range(0, len(self.saves)):
                    color = (255, 255, 255)
                    if i == self.cursor:
                        color = (0, 255, 0)
                    text = font.render(self.saves[i], True, color)
                    self.screen.blit(text, [10, y])
                    y += 20

            pygame.display.update()
