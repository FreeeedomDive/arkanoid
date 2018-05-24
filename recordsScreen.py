import pygame
import player
import sys
import menu


class RecordsScreen:

    def __init__(self, index):
        self.player_index = index
        f = open("records.txt", 'r')
        self.players = []
        for line in f:
            args = line.split('/')
            self.players.append(player.Player(args[0], args[1], int(args[2])))
        f.close()
        self.display = (400, 400)
        self.timer = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.display)
        self.bg = pygame.Surface(self.display)
        self.draw()

    def draw(self):
        pygame.init()
        pygame.display.set_caption("Records")
        while True:
            self.timer.tick(200)
            self.screen.blit(self.bg, (0, 0))
            font = pygame.font.Font(None, 25)
            text = font.render("Name", True, (255, 255, 255))
            self.screen.blit(text, [10, 15])
            text = font.render("Levels", True, (255, 255, 255))
            self.screen.blit(text, [150, 15])
            text = font.render("Score", True, (255, 255, 255))
            self.screen.blit(text, [250, 15])
            x = 50
            for i in range(0, min(10, len(self.players))):
                color = (255, 255, 255)
                if i == self.player_index:
                    color = (0, 255, 0)
                text = font.render(self.players[i].name, True, color)
                self.screen.blit(text, [10, x])
                text = font.render(self.players[i].levels, True, color)
                self.screen.blit(text, [150, x])
                text = font.render(str(self.players[i].score), True, color)
                self.screen.blit(text, [250, x])
                x += 25
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    menu.Menu()
            pygame.display.update()
