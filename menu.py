import pygame
import game
import sys
import editor_info
import select_custom_level
import select_save


class Menu:

    def __init__(self):
        self.display = (220, 120)
        self.screen = pygame.display.set_mode(self.display)
        self.bg = pygame.Surface(self.display)
        self.background_color = "#14005e"
        self.item1 = "1: Start new game"
        self.item2 = "2: Load game"
        self.item3 = "3: Create new level"
        self.item4 = "4: Browse created levels"
        self.timer = pygame.time.Clock()
        self.draw_main_menu()

    def draw_main_menu(self):
        pygame.init()
        pygame.display.set_caption("Main menu")
        self.bg.fill(pygame.Color(self.background_color))
        while True:
            self.timer.tick(200)
            self.screen.blit(self.bg, (0, 0))
            font = pygame.font.Font(None, 25)
            text = font.render(self.item1, True, (255, 255, 255))
            self.screen.blit(text, [10, 15])
            text = font.render(self.item2, True, (255, 255, 255))
            self.screen.blit(text, [10, 40])
            text = font.render(self.item3, True, (255, 255, 255))
            self.screen.blit(text, [10, 65])
            text = font.render(self.item4, True, (255, 255, 255))
            self.screen.blit(text, [10, 90])
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                self.handle_keys(e)
            pygame.display.update()

    def handle_keys(self, e):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            sys.exit(0)
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_1:
            g = game.Game(id=1, score=0, life=3)
            g.start()
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_2:
            select_save.SaveSelector()
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_3:
            editor_info.EditorMapInfo()
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_4:
            select_custom_level.CustomLevelSelector()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            sys.exit(0)
