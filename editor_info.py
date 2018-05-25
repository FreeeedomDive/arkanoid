import pygame
import sys
import editor
import menu


class EditorMapInfo:
    def __init__(self):
        self.display = (320, 240)
        self.screen = pygame.display.set_mode(self.display)
        self.bg = pygame.Surface(self.display)
        self.timer = pygame.time.Clock()
        self.active = 1
        self.width = 0
        self.width_text = "5"
        self.height = 0
        self.height_text = "5"
        self.active_color = "#325200"
        self.inactive_color = "#383838"
        self.start()

    def start(self):
        pygame.init()
        pygame.display.set_caption("New map info")
        self.bg.fill(pygame.Color("#14005e"))
        while True:
            self.timer.tick(200)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    menu.Menu()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                    self.active -= 1
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                    self.active += 1
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    self.width = int(self.width_text)
                    self.height = int(self.height_text)
                    if 5 <= self.width <= 25 and 5 <= self.height <= 25:
                        ed = editor.Editor(self.width, self.height)
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        if self.active % 2 == 1:
                            self.width_text = self.width_text[:-1]
                        else:
                            self.height_text = self.height_text[:-1]
                    else:
                        if self.active % 2 == 1:
                            self.width_text += e.unicode
                        else:
                            self.height_text += e.unicode
            self.screen.blit(self.bg, (0, 0))
            font = pygame.font.Font(None, 25)
            text = font.render("Input count of blocks in field",
                               True, (255, 255, 255))
            self.screen.blit(text, [10, 15])
            text = font.render("min = 5, max = 25", True, (255, 255, 255))
            self.screen.blit(text, [10, 40])
            text = font.render("Width", True, (255, 255, 255))
            self.screen.blit(text, [10, 70])
            text = font.render("Height", True, (255, 255, 255))
            self.screen.blit(text, [100, 70])
            if self.active % 2 == 1:
                font = pygame.font.Font(None, 40)

                pf = pygame.Surface((80, 50))
                pf.fill(pygame.Color(self.active_color))
                self.screen.blit(pf, (10, 100))

                text = font.render(self.width_text, True, (255, 255, 255))
                self.screen.blit(text, [30, 110])

                pf.fill(pygame.Color(self.inactive_color))
                self.screen.blit(pf, (100, 100))

                text = font.render(self.height_text, True, (255, 255, 255))
                self.screen.blit(text, [120, 110])
            else:
                font = pygame.font.Font(None, 40)

                pf = pygame.Surface((80, 50))
                pf.fill(pygame.Color(self.inactive_color))
                self.screen.blit(pf, (10, 100))

                text = font.render(self.width_text, True, (255, 255, 255))
                self.screen.blit(text, [30, 110])

                pf.fill(pygame.Color(self.active_color))
                self.screen.blit(pf, (100, 100))

                text = font.render(self.height_text, True, (255, 255, 255))
                self.screen.blit(text, [120, 110])

            try:
                self.width = int(self.width_text)
                if not 5 <= self.width <= 25:
                    pf = pygame.Surface((80, 50))
                    pf.fill(pygame.Color("#ff0000"))
                    self.screen.blit(pf, (10, 100))
                    text = font.render(self.width_text, True, (255, 255, 255))
                    self.screen.blit(text, [30, 110])
            except:
                pf = pygame.Surface((80, 50))
                pf.fill(pygame.Color("#ff0000"))
                self.screen.blit(pf, (10, 100))
                text = font.render(self.width_text, True, (255, 255, 255))
                self.screen.blit(text, [30, 110])

            try:
                self.height = int(self.height_text)
                if not 5 <= self.height <= 25:
                    pf = pygame.Surface((80, 50))
                    pf.fill(pygame.Color("#ff0000"))
                    self.screen.blit(pf, (100, 100))
                    text = font.render(self.height_text, True, (255, 255, 255))
                    self.screen.blit(text, [120, 110])
            except:
                pf = pygame.Surface((80, 50))
                pf.fill(pygame.Color("#ff0000"))
                self.screen.blit(pf, (100, 100))
                text = font.render(self.height_text, True, (255, 255, 255))
                self.screen.blit(text, [120, 110])
            pygame.display.update()
