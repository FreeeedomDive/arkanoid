import pygame
import sys
from pygame import *
import levels as lvl
import platform as pl
import ball as b
import block as bl

current_level = lvl.LEVEL_2
WIN_WIDTH = len(current_level[0]) * 20
WIN_HEIGHT = len(current_level) * 20
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#001a82"
BORDER_COLOR = "#000e47"
platform = pl.Platform(WIN_WIDTH)
ball = b.Ball(WIN_WIDTH, WIN_HEIGHT)
blocks = []
i = 0


def main():
    global blocks
    blocks = add_blocks()
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Something")
    bg = Surface(DISPLAY)
    bg.fill(Color(BACKGROUND_COLOR))

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            check_platform_moving(e)
        move_platform()
        move_ball()
        reflect_ball_by_wall()
        reflect_ball_by_block()
        draw_elements(screen, bg)
        pygame.display.update()


def add_blocks():
    temp = []
    i = j = 0
    for row in current_level:
        for col in row:
            if col.isdigit():
                block = bl.Block(i * 20 + 10, j * 20 + 10)
                temp.append(block)
                print("added block")
            i += 1
        i = 0
        j += 1
    return temp


def check_platform_moving(e):
    if e.type == KEYDOWN and e.key == K_a:
        platform.MOVING_LEFT = True
    if e.type == KEYDOWN and e.key == K_d:
        platform.MOVING_RIGHT = True
    if e.type == KEYUP and e.key == K_a:
        platform.MOVING_LEFT = False
    if e.type == KEYUP and e.key == K_d:
        platform.MOVING_RIGHT = False


def move_platform():
    if platform.MOVING_LEFT:
        if platform.LEFT_COORD - platform.MOVE_SPEED >= 20:
            platform.LEFT_COORD -= platform.MOVE_SPEED
            platform.RIGHT_COORD -= platform.MOVE_SPEED
    if platform.MOVING_RIGHT:
        if platform.RIGHT_COORD + platform.MOVE_SPEED <= WIN_WIDTH:
            platform.LEFT_COORD += platform.MOVE_SPEED
            platform.RIGHT_COORD += platform.MOVE_SPEED


def move_ball():
    ball.x += ball.speed[0]
    ball.y += ball.speed[1]
    ball.recount_coordinates()


def reflect_ball_by_wall():
    if ball.left == 20 or ball.right == WIN_WIDTH - 20:
        ball.speed[0] = -ball.speed[0]
    if ball.bottom == WIN_HEIGHT - 20:
        ball.dead()
    if ball.top == 20:
        ball.speed[1] = -ball.speed[1]
    if ball.bottom == WIN_HEIGHT - 40 and \
            platform.LEFT_COORD < ball.x < platform.RIGHT_COORD:
        ball.speed[1] = -ball.speed[1]


def reflect_ball_by_block():
    global i
    for block in blocks:
        if ball.top == block.bottom or ball.bottom == block.top:
            if block.left < ball.x < block.right:
                ball.speed[1] = -ball.speed[1]
                blocks.remove(block)
                i += 1
                print(str(i) + ". removed")
            elif ball.left == block.right or ball.right == block.left:
                ball.speed[0] = -ball.speed[0]
                ball.speed[1] = -ball.speed[1]
                blocks.remove(block)
                i += 1
                print(str(i) + ". removed")
        if ball.left == block.right or ball.right == block.left:
            if block.top < ball.y < block.bottom:
                ball.speed[0] = -ball.speed[0]
                blocks.remove(block)
                i += 1
                print(str(i) + ". removed")
            elif ball.top == block.bottom or ball.bottom == block.top:
                ball.speed[0] = -ball.speed[0]
                ball.speed[1] = -ball.speed[1]
                blocks.remove(block)
                i += 1
                print(str(i) + ". removed")
    check_win()


def check_win():
    if len(blocks) == 0:
        print("DEBIL")
        sys.exit(0)


def draw_elements(screen, bg):
    screen.blit(bg, (0, 0))
    pf = Surface((platform.WIDTH, 20))
    pf.fill(Color(platform.COLOR))
    screen.blit(pf, (platform.LEFT_COORD, WIN_HEIGHT - 40))
    x = y = 0
    for row in current_level:
        for col in row:
            if col == "B":
                pf = Surface((20, 20))
                pf.fill(Color(BORDER_COLOR))
                screen.blit(pf, (x, y))
            x += 20
        y += 20
        x = 0
    for block in blocks:
        pf = Surface((20, 20))
        pf.fill(Color(block.color))
        screen.blit(pf, (block.left, block.top))
    pf = Surface((20, 20))
    pf.fill(Color(ball.color))
    screen.blit(pf, (ball.x - 10, ball.y - 10))


if __name__ == "__main__":
    main()
