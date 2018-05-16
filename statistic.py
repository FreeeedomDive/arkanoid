import pygame


class Statistic:

    def __init__(self, passed, score):
        self.passed = passed
        self.score = score
        self.display = (320, 240)
        self.screen = pygame.display.set_mode(self.display)
        self.bg = pygame.Surface(self.display)

    def draw_stats(self):
        pygame.init()
        pygame.display.set_caption("Statistic")
        font = pygame.font.Font(None, 25)
        text = font.render(self.passed, True, (0, 0, 0))
        self.screen.blit(text, [10, 15])
        text = font.render("Your final score: {0}".format(self.score), True, (0, 0, 0))
        self.screen.blit(text, [10, 40])
        while True:
            pygame.display.update()
