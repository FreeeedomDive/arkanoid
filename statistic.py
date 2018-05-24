import pygame
import sys
import player
import records_screen


class Statistic:

    def __init__(self, passed, score):
        self.passed = passed
        self.score = score
        self.display = (320, 240)
        self.timer = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.display)
        self.bg = pygame.Surface(self.display)
        f = open("records.txt", 'r')
        self.records = []
        for line in f:
            args = line.split('/')
            self.records.append(player.Player(args[0], args[1], int(args[2])))
        f.close()

    def draw_stats(self):
        pygame.init()
        pygame.display.set_caption("Statistic")
        name = ""
        while True:
            self.timer.tick(200)
            self.screen.blit(self.bg, (0, 0))
            font = pygame.font.Font(None, 25)
            text = font.render("You have passed {0} levels"
                               .format(self.passed), True, (255, 255, 255))
            self.screen.blit(text, [10, 15])
            text = font.render("Your final score: {0}"
                               .format(self.score), True, (255, 255, 255))
            self.screen.blit(text, [10, 40])
            text = font.render("Enter your name", True, (255, 255, 255))
            self.screen.blit(text, [10, 65])
            text = font.render(name, True, (0, 0, 255))
            self.screen.blit(text, [10, 90])
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                    pl = player.Player(name, self.passed, self.score)
                    self.records.append(pl)
                    self.records.sort(key=lambda x: x.score, reverse=True)
                    f = open("records.txt", 'w')
                    f.truncate()
                    for p in self.records:
                        f.write(str(p) + "\n")
                    index = self.records.index(pl)
                    f.close()
                    r = records_screen.RecordsScreen(index)
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    else:
                        name += e.unicode
                    text = font.render(name, True, (0, 0, 255))
                    self.screen.blit(text, [10, 90])
            pygame.display.update()
