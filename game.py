import pygame
import sys
import platform as pl
import ball as b
import map as m
import statistic
import block as bl
import math
import random
import menu
import datetime
import bonus


class Game:
    eps = 1.0
    music_files = {1: "Music/megalovania.mp3",
                   2: "Music/limelight.mp3",
                   3: "Music/tripel.mp3",
                   4: "Music/voiceless.mp3",
                   5: "Music/highscore.mp3",
                   6: "Music/monster.mp3",
                   7: "Music/anthem.mp3",
                   8: "Music/ethereal.mp3",
                   9: "Music/mayday.mp3",
                   10: "Music/medal.mp3"}

    def __init__(self, id=1, score=0, life=3, f=None, map=None):
        self.custom = False
        if map is not None:
            self.current_level_index = "Custom.{0}".format(map)
            self.custom = True
            self.life = life
            self.score = score
            self.multiplier = 1.0
            self.map = m.Map(map)
            self.current_level = self.map.map
            self.field_width = len(self.current_level[0]) * 20 - 20
            self.win_width = self.field_width + 150
            self.win_height = len(self.current_level) * 20
            self.blocks = self.map.blocks
            self.platform = pl.Platform(self.field_width)
            self.ball = b.Ball(self.field_width, self.win_height)
        elif f is not None:
            args = f.split(";")
            if args[0][:6] == "Custom":
                self.custom = True
            if not self.custom:
                self.current_level_index = int(args[0])
                try:
                    self.map = m.Map("Levels/level" +
                                     str(self.current_level_index) + ".txt")
                except:
                    stat = statistic.Statistic("{0}"
                                               .format
                                               (self.current_level_index),
                                               self.score)
                    stat.draw_stats()
            else:
                self.map = m.Map(args[0][7:])
            self.score = int(args[1])
            self.life = int(args[2])
            self.multiplier = float(args[3])

            self.current_level = self.map.map
            self.field_width = len(self.current_level[0]) * 20 - 20
            self.win_width = self.field_width + 150
            self.win_height = len(self.current_level) * 20
            self.platform = pl.Platform(self.win_width,
                                        float(args[4]), float(args[5]))
            b_args = args[6].split(',')
            self.ball = b.Ball(self.field_width, self.win_height,
                               float(b_args[0]), float(b_args[1]),
                               float(b_args[2]),
                               float(b_args[3]),
                               float(self.win_height - 50),
                               float(b_args[4]))
            self.blocks = []
            for i in range(7, len(args)):
                if args[i] == '':
                    break
                block_args = args[i].split(',')
                self.blocks.append(bl.Block(int(block_args[0]),
                                            int(block_args[1]),
                                            int(block_args[2])))
        else:
            self.current_level_index = id
            self.life = life
            self.score = score
            self.multiplier = 1.0
            try:
                self.map = m.Map("Levels/level" +
                                 str(self.current_level_index) + ".txt")
            except:
                stat = statistic.Statistic(
                    "{0}".format(self.current_level_index - 1),
                    self.score)
                stat.draw_stats()
            self.current_level = self.map.map
            self.field_width = len(self.current_level[0]) * 20 - 20
            self.win_width = self.field_width + 150
            self.win_height = len(self.current_level) * 20
            self.blocks = self.map.blocks
            self.platform = pl.Platform(self.field_width)
            self.ball = b.Ball(self.field_width, self.win_height)
        self.active_bonuses = []
        self.display = (self.win_width, self.win_height)
        self.background_color = "#001a82"
        self.border_color = "#000e47"
        self.on_pause = False
        self.lose = False
        self.screen = pygame.display.set_mode(self.display)
        self.bg = pygame.Surface(self.display)
        self.timer = pygame.time.Clock()
        self.ctrl_pressed = False
        self.ball_cant_drop = False

    def start(self):
        pygame.init()
        pygame.mouse.set_visible(False)
        pygame.display.set_caption("Arkanoid")
        if not self.custom:
            pygame.mixer.music.load(self.music_files[self.current_level_index])
            pygame.mixer.music.set_volume(0.00)
            pygame.mixer.music.play(25)
        self.bg.fill(pygame.Color(self.background_color))
        while True:
            self.timer.tick(200)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                self.handle_pressed_keys(e)
            if not self.on_pause:
                self.move_platform()
                self.ball.move()
                self.reflect_ball_by_wall()
                self.reflect_ball_by_block()
                self.move_bonuses()
                self.draw_elements()
                pygame.display.update()
            else:
                self.draw_pause()
                pygame.display.update()

    def handle_pressed_keys(self, e):
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            pygame.mixer.music.stop()
            menu.Menu()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_a:
            self.platform.MOVING_LEFT = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_d:
            self.platform.MOVING_RIGHT = True
        if e.type == pygame.KEYUP and e.key == pygame.K_a:
            self.platform.MOVING_LEFT = False
        if e.type == pygame.KEYUP and e.key == pygame.K_d:
            self.platform.MOVING_RIGHT = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_b:
            self.execute_cheat("destroy block")
        if e.type == pygame.KEYDOWN and e.key == pygame.K_n:
            self.execute_cheat("no lose")
        if e.type == pygame.KEYDOWN and e.key == pygame.K_i:
            self.execute_cheat("decrease speed")
        if e.type == pygame.KEYDOWN and e.key == pygame.K_o:
            self.execute_cheat("increase speed")
        if e.type == pygame.KEYDOWN and e.key == pygame.K_r:
            self.ball.reincarnate()
            self.eps = 1.0
        if e.type == pygame.KEYDOWN and e.key == pygame.K_q:
            if self.on_pause:
                self.on_pause = False
            else:
                self.on_pause = True
        if e.type == pygame.KEYDOWN and e.key == pygame.K_LCTRL:
            self.ctrl_pressed = True
        if e.type == pygame.KEYUP and e.key == pygame.K_LCTRL:
            self.ctrl_pressed = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_s:
            if self.ctrl_pressed:
                self.save_game()
        if e.type == pygame.KEYDOWN and e.key == pygame.K_KP_MINUS:
            volume = pygame.mixer.music.get_volume()
            volume -= 0.01
            pygame.mixer.music.set_volume(volume)
        if e.type == pygame.KEYDOWN and e.key == pygame.K_KP_PLUS:
            volume = pygame.mixer.music.get_volume()
            volume += 0.01
            pygame.mixer.music.set_volume(volume)

    def save_game(self):
        d = datetime.datetime.now()
        filename = "save-{0}-{1}-{2}-{3}-{4}-{5}" \
            .format(d.year, d.month, d.day, d.hour,
                    d.minute, d.second)
        game = str(self.current_level_index) + ";"
        game += str(self.score) + ";"
        game += str(self.life) + ";"
        game += str(self.multiplier) + ";"
        game += str(self.platform.LEFT_COORD) + ";"
        game += str(self.platform.WIDTH) + ";"
        game += str(self.ball.x) + ',' + str(self.ball.y) + ',' + \
            str(self.ball.speed[0]) + ',' + \
            str(self.ball.speed[1]) + ',' + \
            str(self.ball.power) + ";"
        for block in self.blocks:
            game += str(block.x) + ',' + str(block.y) + ',' + \
                    str(block.strength) + ";"
        file = open("Saves/{0}.txt".format(filename), 'w')
        file.write(game)
        file.close()

    def execute_cheat(self, cheat):
        # if self.life == 1:
        #     return
        # self.life -= 1
        if cheat == "destroy block":
            index = random.randint(0, len(self.blocks) - 1)
            self.blocks.remove(self.blocks[index])
            self.check_win()
        if cheat == "no lose":
            self.ball_cant_drop = not self.ball_cant_drop
        if cheat == "decrease speed":
            self.ball.speed[0] /= 2
            self.ball.speed[1] /= 2
            self.eps /= 2
        if cheat == "increase speed":
            self.ball.speed[0] *= 2
            self.ball.speed[1] *= 2
            self.eps *= 2

    def move_platform(self):
        if self.platform.LEFT_COORD >= 20 and self.platform.MOVING_LEFT:
            self.platform.move(-1)
        if self.platform.RIGHT_COORD <= self.field_width - 20 \
                and self.platform.MOVING_RIGHT:
            self.platform.move(1)

    def reflect_ball_by_wall(self):
        if math.fabs(self.ball.left - 20) < self.eps or \
                math.fabs(self.ball.right -
                          (self.field_width - 20)) < self.eps:
            self.ball.speed[0] = -self.ball.speed[0]
            return
        if math.fabs(self.ball.top - 20) < self.eps:
            self.ball.speed[1] = -self.ball.speed[1]
            return
        if math.fabs(self.ball.bottom - (self.win_height - 40)) < self.eps:
            self.reflect_ball_by_platform()

    def reflect_ball_by_platform(self):
        if self.ball.right < self.platform.LEFT_COORD or \
                self.ball.left > self.platform.RIGHT_COORD:
            self.multiplier = 1.0
            if not self.ball_cant_drop:
                self.eps = 1.0
                self.score -= int(self.score // 5)
                self.life -= 1
                if self.life == 0:
                    pygame.mixer.music.stop()
                    if not self.custom:
                        stats = statistic.Statistic(
                            str(self.current_level_index - 1), self.score)
                        stats.draw_stats()
                    menu.Menu()
                else:
                    self.ball.reincarnate()
            else:
                self.ball.speed[1] = -self.ball.speed[1]
            return
        self.score += int(10 * self.multiplier)
        self.multiplier = 1.0
        if self.ball.x < self.platform.LEFT_COORD:
            self.ball.speed[0] = -self.ball.basic_speed
            self.ball.speed[1] = -self.ball.basic_speed
        elif self.ball.x > self.platform.RIGHT_COORD:
            self.ball.speed[0] = self.ball.basic_speed
            self.ball.speed[1] = -self.ball.basic_speed
        else:
            middle = self.platform.WIDTH // 2
            pos = self.ball.x - self.platform.LEFT_COORD
            if pos < middle:
                angle = -1 + (pos / middle)
                self.ball.speed[0] = angle
            else:
                angle = (pos / middle) - 1
                self.ball.speed[0] = angle
            self.ball.speed[1] = \
                -math.sqrt(2 - math.pow(self.ball.speed[0], 2))
        print(self.ball.speed)

    def reflect_ball_by_block(self):
        for block in self.blocks:
            if math.fabs(self.ball.top - block.bottom) < self.eps or \
                    math.fabs(self.ball.bottom - block.top) < self.eps:
                if block.left <= self.ball.left <= block.right or \
                        block.left <= self.ball.right <= block.right:
                    self.ball.speed[1] = -self.ball.speed[1]
                    self.score += int(20 * self.multiplier)
                    if block.decrease_and_check_destroying(self.ball.power):
                        self.score += int(100 * self.multiplier)
                        if block.bonus is not None:
                            if block.bonus == "destroy_line":
                                destr = []
                                for b in self.blocks:
                                    if b.y == block.y and b != block:
                                        destr.append(b)
                                self.score += len(destr) * 150
                                for d in destr:
                                    self.blocks.remove(d)
                                destr.clear()
                            else:
                                bon = bonus.Bonus(
                                    block.bonus, block.left, block.top)
                                self.active_bonuses.append(bon)
                        self.blocks.remove(block)
                    self.multiplier += 0.1
                    self.check_win()
                    return
            elif math.fabs(self.ball.left - block.right) < self.eps or \
                    math.fabs(self.ball.right - block.left) < self.eps:
                if block.top <= self.ball.top <= block.bottom or \
                        block.top <= self.ball.bottom <= block.bottom:
                    self.ball.speed[0] = -self.ball.speed[0]
                    self.score += int(20 * self.multiplier)
                    if block.decrease_and_check_destroying(self.ball.power):
                        self.score += int(100 * self.multiplier)
                        if block.bonus is not None:
                            if block.bonus == "destroy_line":
                                destr = []
                                for b in self.blocks:
                                    if b.y == block.y and b != block:
                                        destr.append(b)
                                self.score += len(destr) * 150
                                for d in destr:
                                    self.blocks.remove(d)
                                destr.clear()
                            else:
                                bon = bonus.Bonus(
                                    block.bonus, block.left, block.top)
                                self.active_bonuses.append(bon)
                        self.blocks.remove(block)
                    self.multiplier += 0.1
                    self.check_win()
                    return

    def move_bonuses(self):
        if len(self.active_bonuses) > 0:
            for bon in self.active_bonuses:
                bon.y += bon.speed[1]
                if bon.y == self.win_height - 40:
                    if self.platform.LEFT_COORD <= bon.x <= \
                            self.platform.RIGHT_COORD:
                        if bon.name == "powerup":
                            self.ball.power *= 2
                        if bon.name == "platform_more":
                            self.platform.WIDTH = self.platform.WIDTH // 2 * 3
                            self.platform.RIGHT_COORD = \
                                self.platform.LEFT_COORD + self.platform.WIDTH
                        if bon.name == "platform_less":
                            self.platform.WIDTH //= 2
                            self.platform.RIGHT_COORD = \
                                self.platform.LEFT_COORD + self.platform.WIDTH
                    else:
                        self.active_bonuses.remove(bon)

    def check_win(self):
        if len(self.blocks) == 0:
            pygame.mixer.music.stop()
            if not self.custom:
                g = Game(self.current_level_index + 1,
                         self.score, self.life + 1)
                g.start()
                self.timer = None
            menu.Menu()

    def draw_elements(self):
        self.screen.blit(self.bg, (0, 0))
        self.platform.draw(self.screen, self.win_height)
        x = y = 0
        for row in self.current_level:
            for col in row:
                if col == "B":
                    pf = pygame.Surface((20, 20))
                    pf.fill(pygame.Color(self.border_color))
                    self.screen.blit(pf, (x, y))
                x += 20
            y += 20
            x = 0
        for block in self.blocks:
            block.draw(self.screen)
        pf = pygame.Surface((20, 20))
        pf.fill(pygame.Color(self.ball.color))
        self.screen.blit(pf, (self.ball.x - 10, self.ball.y - 10))
        if len(self.active_bonuses) > 0:
            for bon in self.active_bonuses:
                self.screen.blit(bon.image, (bon.x, bon.y))
        if self.ball_cant_drop:
            pf = pygame.Surface((self.field_width - 40, 2))
            pf.fill(pygame.Color("#ffff00"))
            self.screen.blit(pf, (20, self.win_height - 40))

        font = pygame.font.Font(None, 25)
        lvl = ""
        if self.custom:
            lvl = "Level: Custom"
        else:
            lvl = "Level: {0}".format(self.current_level_index)

        text = font.render(lvl, True, (255, 255, 255))
        self.screen.blit(text, [self.win_width - 140, 15])
        text = font.render("Score: {0}"
                           .format(self.score), True, (255, 255, 255))
        self.screen.blit(text, [self.win_width - 140, 35])
        text = font.render("Multiplier: {0}"
                           .format(self.multiplier), True, (255, 255, 255))
        self.screen.blit(text, [self.win_width - 140, 55])
        text = font.render("Balls: {0}"
                           .format(self.life), True, (255, 255, 255))
        self.screen.blit(text, [self.win_width - 140, 75])

    def draw_pause(self):
        if self.lose:
            t = "Final score: {0}".format(self.score)
        else:
            t = "Game paused"
        font = pygame.font.Font(None, 45)
        text = font.render(t, True, (255, 0, 0))
        self.screen.blit(text, [self.field_width // 2 - 60,
                                self.win_height // 2])
