import pygame
import sys
import random
import menu


class Editor:
    images = {0:  pygame.image.load("Images/block.png"),
              1:  pygame.image.load("Images/block1.png"),
              2:  pygame.image.load("Images/block2.png"),
              3:  pygame.image.load("Images/block3.png"),
              4:  pygame.image.load("Images/block4.png"),
              5:  pygame.image.load("Images/block5.png"),
              10: pygame.image.load("Images/cursor.png")}
    alph = "abcdefghijklmnopqrstuvwxyz"

    def __init__(self, width, height):
        self.width = width
        self.height = height
        print(width, height)
        self.field_width = width * 20 + 20
        self.field_height = height * 20 + 20
        print(self.field_width, self.field_height)
        self.game_objects = []
        for i in range(0, self.height):
            line = []
            for j in range(0, self.width):
                line.append(' ')
            self.game_objects.append(line)
        print(len(self.game_objects), len(self.game_objects[0]))
        self.cursor = [0, 0]
        self.selected = "1"
        self.display = (self.field_width, self.field_height)
        self.background_color = "#001a82"
        self.screen = pygame.display.set_mode(self.display)
        self.bg = pygame.Surface(self.display)
        self.timer = pygame.time.Clock()
        self.ctrl_pressed = False
        self.start()

    def start(self):
        pygame.init()
        pygame.display.set_caption("Editor")
        self.bg.fill(pygame.Color("#14005e"))
        while True:
            self.timer.tick(200)
            for e in pygame.event.get():
                self.handle_keys(e)
            self.draw()

    def handle_keys(self, e):
        if e.type == pygame.QUIT:
            sys.exit()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            menu.Menu()
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_a:
            if 0 < self.cursor[1]:
                self.cursor[1] -= 1
                print(self.cursor)
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_d:
            if self.cursor[1] < self.width - 1:
                self.cursor[1] += 1
                print(self.cursor)
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_w:
            if 0 < self.cursor[0]:
                self.cursor[0] -= 1
                print(self.cursor)
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_s:
            if self.cursor[0] < self.height - 1:
                self.cursor[0] += 1
                print(self.cursor)
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_e:
            x = self.cursor[0]
            y = self.cursor[1]
            if self.selected == '0':
                self.game_objects[x][y] = ' '
            else:
                self.game_objects[x][y] = self.selected
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_LCTRL:
            self.ctrl_pressed = True
        elif e.type == pygame.KEYUP and e.key == pygame.K_LCTRL:
            self.ctrl_pressed = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_s:
            if self.ctrl_pressed:
                self.save_map()
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_1:
            self.selected = "1"
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_2:
            self.selected = "2"
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_3:
            self.selected = "3"
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_4:
            self.selected = "4"
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_5:
            self.selected = "5"
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_0:
            self.selected = "0"

    def save_map(self):
        l = random.randint(6, 12)
        name = ""
        for i in range(0, l):
            name += self.alph[random.randint(0, len(self.alph) - 1)]
        map = ""
        for i in range(0, self.width + 2):
            map += "B"
        for i in range(0, len(self.game_objects)):
            map += "\nB"
            for j in range(0, len(self.game_objects[i])):
                map += self.game_objects[i][j]
            map += "B"
        print(map)
        for i in range(0, 8):
            map += "\nB"
            for j in range(0, self.width):
                map += " "
            map += "B"
        print(map)
        file = open("CreatedLevels/{0}.txt".format(name), 'w')
        file.write(map)
        file.close()
        menu.Menu()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.bg.fill(pygame.Color(self.background_color))
        x = 10
        y = 10
        for i in range(0, self.height):
            for j in range(0, self.width):
                block = self.game_objects[i][j]
                if block == " ":
                    self.screen.blit(self.images[0], (x, y))
                else:
                    self.screen.blit(self.images[int(block)], (x, y))
                x += 20
            y += 20
            x = 10
        x = self.cursor[1]
        y = self.cursor[0]
        if self.game_objects[y][x] == ' ':
            self.screen.blit(self.images[10], (x*20 + 10, y*20 + 10))
        pygame.display.update()
