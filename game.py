import pygame as pg
import sys
import platform as pl
import ball as b
import block as bl


class Game:

    def __init__(self):
        self.current_level = []
        self.create_map("Levels/level2.txt")
        self.WIN_WIDTH = len(self.current_level[0]) * 20 - 20
        self.WIN_HEIGHT = len(self.current_level) * 20
        self.DISPLAY = (self.WIN_WIDTH, self.WIN_HEIGHT)
        self.BACKGROUND_COLOR = "#001a82"
        self.BORDER_COLOR = "#000e47"
        self.platform = pl.Platform(self.WIN_WIDTH)
        self.ball = b.Ball(self.WIN_WIDTH, self.WIN_HEIGHT)
        self.blocks = []
        self.timer = pg.time.Clock()

    def create_map(self, filename):
        map = open(filename)
        self.current_level = []
        for line in map:
            self.current_level.append(line)
        map.close()

    def run(self):
        self.blocks = self.add_blocks()
        pg.init()
        screen = pg.display.set_mode(self.DISPLAY)
        pg.display.set_caption("Something")
        bg = pg.Surface(self.DISPLAY)
        bg.fill(pg.Color(self.BACKGROUND_COLOR))
        while True:
            self.timer.tick(200)
            for e in pg.event.get():
                if e.type == pg.QUIT:
                    sys.exit()
                self.check_platform_moving(e)
            self.move_platform()
            self.ball.move()
            self.reflect_ball_by_block()
            self.reflect_ball_by_wall()
            self.draw_elements(screen, bg)
            pg.display.update()

    def create_new_game(self, map):
        pass

    def add_blocks(self):
        temp = []
        i = j = 0
        for row in self.current_level:
            for col in row:
                if col.isdigit():
                    block = bl.Block(i * 20 + 10, j * 20 + 10, int(col))
                    temp.append(block)
                i += 1
            i = 0
            j += 1
        return temp

    def check_platform_moving(self, e):
        if e.type == pg.KEYDOWN and e.key == pg.K_a:
            self.platform.MOVING_LEFT = True
        if e.type == pg.KEYDOWN and e.key == pg.K_d:
            self.platform.MOVING_RIGHT = True
        if e.type == pg.KEYUP and e.key == pg.K_a:
            self.platform.MOVING_LEFT = False
        if e.type == pg.KEYUP and e.key == pg.K_d:
            self.platform.MOVING_RIGHT = False

    def move_platform(self):
        if self.platform.LEFT_COORD >= 20 and self.platform.MOVING_LEFT:
            self.platform.move(-1)
        if self.platform.RIGHT_COORD <= self.WIN_WIDTH - 20 and self.platform.MOVING_RIGHT:
            self.platform.move(1)

    def reflect_ball_by_wall(self):
        if self.ball.left == 20 or self.ball.right == self.WIN_WIDTH - 20:
            self.ball.speed[0] = -self.ball.speed[0]
        if self.ball.bottom == self.WIN_HEIGHT - 20:
            self.ball.dead()
        if self.ball.top == 20:
            self.ball.speed[1] = -self.ball.speed[1]
        if self.ball.bottom == self.WIN_HEIGHT - 40:
            if self.platform.LEFT_COORD < self.ball.left < self.platform.RIGHT_COORD or \
                    self.platform.LEFT_COORD < self.ball.right < self.platform.RIGHT_COORD:
                self.ball.speed[1] = -self.ball.speed[1]

    def reflect_ball_by_block(self):
        # if ball.speed[0] > 0 and ball.speed[1] < 0:
        #     for block in blocks:
        #         if ball.left == block.left and ball.right == block.right \
        #                 and ball.top == block.bottom:
        #             ball.speed[1] = -ball.speed[1]
        #             blocks.remove(block)
        #         elif ball.right == block.left and ball.top == block.bottom:
        #             ball.speed[0] = -ball.speed[0]
        #             ball.speed[1] = -ball.speed[1]
        #             blocks.remove(block)
        # elif ball.speed[0] < 0 and ball.speed[1] < 0:
        #     for block in blocks:
        #         if ball.left == block.left and ball.right == block.right \
        #                 and ball.top == block.bottom:
        #             ball.speed[1] = -ball.speed[1]
        #             blocks.remove(block)
        #         elif ball.left == block.right and ball.top == block.bottom:
        #             ball.speed[0] = -ball.speed[0]
        #             ball.speed[1] = -ball.speed[1]
        #             blocks.remove(block)
        # elif ball.speed[0] > 0 and ball.speed[1] > 0:
        #     for block in blocks:
        #         if ball.left == block.left and ball.right == block.right \
        #                 and ball.bottom == block.top:
        #             ball.speed[1] = -ball.speed[1]
        #             blocks.remove(block)
        #         elif ball.left == block.right and ball.bottom == block.top:
        #             ball.speed[0] = -ball.speed[0]
        #             ball.speed[1] = -ball.speed[1]
        #             blocks.remove(block)
        # else:
        #     for block in blocks:
        #         if ball.left == block.left and ball.right == block.right \
        #                 and ball.bottom == block.top:
        #             ball.speed[1] = -ball.speed[1]
        #             blocks.remove(block)
        #         elif ball.right == block.left and ball.bottom == block.top:
        #             ball.speed[0] = -ball.speed[0]
        #             ball.speed[1] = -ball.speed[1]
        #             blocks.remove(block)
        for block in self.blocks:
            if self.ball.top == block.bottom or self.ball.bottom == block.top:
                if block.left <= self.ball.left <= block.right or \
                        block.left <= self.ball.right <= block.right:
                    self.ball.speed[1] = -self.ball.speed[1]
                    if block.decrease_and_check_destroying():
                        self.blocks.remove(block)
            if self.ball.left == block.right or self.ball.right == block.left:
                if block.top < self.ball.top < block.bottom or \
                        block.top < self.ball.top < block.bottom:
                    self.ball.speed[0] = -self.ball.speed[0]
                    if block.decrease_and_check_destroying():
                        self.blocks.remove(block)
                self.check_win()

    def check_win(self):
        if len(self.blocks) == 0:
            print("gege")
            sys.exit(0)

    def draw_elements(self, screen, bg):
        screen.blit(bg, (0, 0))
        self.platform.draw(screen, self.WIN_HEIGHT)
        x = y = 0
        for row in self.current_level:
            for col in row:
                if col == "B":
                    pf = pg.Surface((20, 20))
                    pf.fill(pg.Color(self.BORDER_COLOR))
                    screen.blit(pf, (x, y))
                x += 20
            y += 20
            x = 0
        for block in self.blocks:
            block.draw(screen)
        pf = pg.Surface((20, 20))
        pf.fill(pg.Color(self.ball.color))
        screen.blit(pf, (self.ball.x - 10, self.ball.y - 10))
