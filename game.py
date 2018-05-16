import pygame as pg
import sys
import platform as pl
import ball as b
import map as m
import math
import statistic
import block as bl


class Game:

    def __init__(self, id=1, score=0, life=3, f=None):
        if f is not None:
            args = f.split(";")
            self.current_level_index = int(args[0])
            self.score = int(args[1])
            self.life = int(args[2])
            self.multiplier = float(args[3])
            try:
                self.map = m.Map("Levels/level" +
                                 str(self.current_level_index) + ".txt")
            except:
                stat = statistic.Statistic("You have passed all levels",
                                           self.score)
                stat.draw_stats()
            self.current_level = self.map.map
            self.field_width = len(self.current_level[0]) * 20 - 20
            self.win_width = self.field_width + 150
            self.win_height = len(self.current_level) * 20
            self.display = (self.win_width, self.win_height)
            self.background_color = "#001a82"
            self.border_color = "#000e47"
            self.platform = pl.Platform(self.win_width, float(args[4]), float(args[5]))
            b_args = args[6].split(',')
            self.ball = b.Ball(self.field_width, self.win_height,
                               float(b_args[0]), float(b_args[1]), float(b_args[2]),
                               float(b_args[3]), float(self.win_height - 50))
            self.blocks = []
            for i in range(7, len(args)):
                if args[i] == '':
                    break
                block_args = args[i].split(',')
                self.blocks.append(bl.Block(int(block_args[0]), int(block_args[1]),
                                            int(block_args[2])))
            self.on_pause = False
            self.lose = False
            self.screen = pg.display.set_mode(self.display)
            self.bg = pg.Surface(self.display)
            self.timer = pg.time.Clock()
            self.ctrl_pressed = False
        else:
            self.current_level_index = id
            self.life = life
            self.score = score
            self.multiplier = 1.0
            try:
                self.map = m.Map("Levels/level" +
                                 str(self.current_level_index) + ".txt")
            except:
                stat = statistic.Statistic("You have passed all levels",
                                           self.score)
                stat.draw_stats()
            self.current_level = self.map.map
            self.blocks = self.map.blocks
            self.field_width = len(self.current_level[0]) * 20 - 20
            self.win_width = self.field_width + 150
            self.win_height = len(self.current_level) * 20
            self.display = (self.win_width, self.win_height)
            self.background_color = "#001a82"
            self.border_color = "#000e47"
            self.platform = pl.Platform(self.field_width)
            self.ball = b.Ball(self.field_width, self.win_height)
            self.on_pause = False
            self.lose = False
            self.screen = pg.display.set_mode(self.display)
            self.bg = pg.Surface(self.display)
            self.timer = pg.time.Clock()
            self.ctrl_pressed = False

    def start(self):
        pg.init()
        pg.display.set_caption("Arkanoid")
        self.bg.fill(pg.Color(self.background_color))
        while True:
            self.timer.tick(200)
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    sys.exit()
                self.handle_pressed_keys(e)
            if not self.on_pause:
                self.move_platform()
                self.ball.move()
                self.reflect_ball_by_block()
                self.reflect_ball_by_wall()
                self.draw_elements()
                pg.display.update()
            else:
                self.draw_pause()
                pg.display.update()

    def handle_pressed_keys(self, e):
        if e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE:
            sys.exit(0)
        if e.type == pg.KEYDOWN and e.key == pg.K_a:
            self.platform.MOVING_LEFT = True
        if e.type == pg.KEYDOWN and e.key == pg.K_d:
            self.platform.MOVING_RIGHT = True
        if e.type == pg.KEYUP and e.key == pg.K_a:
            self.platform.MOVING_LEFT = False
        if e.type == pg.KEYUP and e.key == pg.K_d:
            self.platform.MOVING_RIGHT = False
        if e.type == pg.KEYDOWN and e.key == pg.K_b:
            self.execute_cheat("decrease blocks")
        if e.type == pg.KEYDOWN and e.key == pg.K_q:
            if self.on_pause:
                self.on_pause = False
            else:
                self.on_pause = True
        if e.type == pg.KEYDOWN and e.key == pg.K_LCTRL:
            print("pressed")
            self.ctrl_pressed = True
        if e.type == pg.KEYUP and e.key == pg.K_LCTRL:
            self.ctrl_pressed = False
        if e.type == pg.KEYDOWN and e.key == pg.K_s:
            if self.ctrl_pressed:
                print("Saved")
                self.save_game()

    def save_game(self):
        game = str(self.current_level_index) + ";"
        game += str(self.score) + ";"
        game += str(self.life) + ";"
        game += str(self.multiplier) + ";"
        game += str(self.platform.LEFT_COORD) + ";"
        game += str(self.platform.WIDTH) + ";"
        game += str(self.ball.x) + ',' + str(self.ball.y) + ',' + \
            str(self.ball.speed[0]) + ',' + str(self.ball.speed[1]) + ";"
        for block in self.blocks:
            game += str(block.x) + ',' + str(block.y) + ',' + \
                    str(block.strength) + ";"
        file = open("saved.txt", 'w')
        file.write(game)
        file.close()

    def execute_cheat(self, cheat):
        if self.life == 1:
            return
        self.life -= 1
        if cheat == "decrease blocks":
            for block in self.blocks:
                if block.decrease_and_check_destroying():
                    self.blocks.remove(block)
                self.draw_elements()
                self.check_win()

    def move_platform(self):
        if self.platform.LEFT_COORD >= 20 and self.platform.MOVING_LEFT:
            self.platform.move(-1)
        if self.platform.RIGHT_COORD <= self.field_width - 20 \
                and self.platform.MOVING_RIGHT:
            self.platform.move(1)

    def reflect_ball_by_wall(self):
        if self.ball.top <= 20:
            self.ball.speed[1] = -self.ball.speed[1]
        elif self.ball.left <= 20 or self.ball.right >= self.field_width - 20:
            self.ball.speed[0] = -self.ball.speed[0]
        elif self.ball.bottom == self.win_height - 40:
            if self.platform.LEFT_COORD <= self.ball.right <= \
                    self.platform.LEFT_COORD + self.platform.WIDTH // 2 or \
                    self.platform.LEFT_COORD <= self.ball.left <= \
                    self.platform.LEFT_COORD + self.platform.WIDTH // 2:
                self.ball.speed[1] = -self.ball.speed[1]
                self.ball.speed[0] = -math.fabs(self.ball.speed[0])
                self.multiplier = 1.0
                return
            elif self.platform.LEFT_COORD + self.platform.WIDTH // 2 <= \
                    self.ball.left <= self.platform.RIGHT_COORD or \
                    self.platform.LEFT_COORD + self.platform.WIDTH // 2 <= \
                    self.ball.right <= self.platform.RIGHT_COORD:
                self.multiplier = 1.0
                self.ball.speed[1] = -self.ball.speed[1]
                self.ball.speed[0] = math.fabs(self.ball.speed[0])
                return
        elif self.ball.bottom == self.win_height - 20:
            self.score -= int(self.score // 5)
            self.multiplier = 1.0
            self.life -= 1
            if self.life == 0:
                self.on_pause = True
                self.lose = True
            else:
                self.ball.reincarnate()

    def reflect_ball_by_block(self):
        for block in self.blocks:
            if self.ball.top == block.bottom or self.ball.bottom == block.top:
                if block.left <= self.ball.left <= block.right or \
                        block.left <= self.ball.right <= block.right:
                    self.ball.speed[1] = -self.ball.speed[1]
                    self.score += int(20 * self.multiplier)
                    if block.decrease_and_check_destroying():
                        self.score += int(100 * self.multiplier)
                        self.blocks.remove(block)
                    self.multiplier += 0.1
                    self.check_win()
                    return
            elif self.ball.left == block.right or \
                    self.ball.right == block.left:
                if block.top <= self.ball.top <= block.bottom or \
                        block.top <= self.ball.bottom <= block.bottom:
                    self.ball.speed[0] = -self.ball.speed[0]
                    self.score += int(20 * self.multiplier)
                    if block.decrease_and_check_destroying():
                        self.score += int(100 * self.multiplier)
                        self.blocks.remove(block)
                    self.multiplier += 0.1
                    self.check_win()
                    return

    def check_win(self):
        if len(self.blocks) == 0:
            g = Game(self.current_level_index + 1, self.score, self.life + 1)
            g.start()
            self.timer = None

    def draw_elements(self):
        self.screen.blit(self.bg, (0, 0))
        self.platform.draw(self.screen, self.win_height)
        x = y = 0
        for row in self.current_level:
            for col in row:
                if col == "B":
                    pf = pg.Surface((20, 20))
                    pf.fill(pg.Color(self.border_color))
                    self.screen.blit(pf, (x, y))
                x += 20
            y += 20
            x = 0
        for block in self.blocks:
            block.draw(self.screen)
        pf = pg.Surface((20, 20))
        pf.fill(pg.Color(self.ball.color))
        self.screen.blit(pf, (self.ball.x - 10, self.ball.y - 10))
        font = pg.font.Font(None, 25)
        text = font.render("Level: {0}"
                           .format(self.current_level_index), True, (255, 255, 255))
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
        font = pg.font.Font(None, 45)
        text = font.render(t, True, (255, 0, 0))
        self.screen.blit(text, [self.field_width // 2 - 60, self.win_height // 2])
