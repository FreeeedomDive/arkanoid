import pygame
import sys
from pygame import *
import levels as lvl
import platform as pl
import ball as b

current_level = lvl.LEVEL_1
WIN_WIDTH = len(current_level[0]) * 20
WIN_HEIGHT = len(current_level)*20
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = "#001a82"
BORDER_COLOR = "#000e47"
platform = pl.Platform(WIN_WIDTH)
ball = b.Ball(WIN_WIDTH, WIN_HEIGHT)


def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Something")
    bg = Surface(DISPLAY)
    bg.fill(Color(BACKGROUND_COLOR))

    while True:
        for e in pygame.event.get():
            if e.type == QUIT:
                sys.exit()
            if e.type == KEYDOWN and e.key == K_a:
                platform.MOVING_LEFT = True
            if e.type == KEYDOWN and e.key == K_d:
                platform.MOVING_RIGHT = True
            if e.type == KEYUP and e.key == K_a:
                platform.MOVING_LEFT = False
            if e.type == KEYUP and e.key == K_d:
                platform.MOVING_RIGHT = False
        if platform.MOVING_LEFT:
            if platform.LEFT_COORD - platform.MOVE_SPEED >= 20:
                platform.LEFT_COORD -= platform.MOVE_SPEED
                platform.RIGHT_COORD -= platform.MOVE_SPEED
        if platform.MOVING_RIGHT:
            if platform.RIGHT_COORD + platform.MOVE_SPEED <= WIN_WIDTH - 20:
                platform.LEFT_COORD += platform.MOVE_SPEED
                platform.RIGHT_COORD += platform.MOVE_SPEED
        ball.x += ball.speed[0]
        ball.y += ball.speed[1]
        ball.recount_coordinates()
        if ball.left <= 20 or ball.right > WIN_WIDTH - 20:
            ball.speed[0] = -ball.speed[0]
        if ball.bottom >= WIN_HEIGHT - 20:
            ball.dead()
        if ball.top <= 20:
            ball.speed[1] = -ball.speed[1]
        if ball.bottom > WIN_HEIGHT - 40 and platform.LEFT_COORD < ball.x < platform.RIGHT_COORD:
            ball.speed[1] = -ball.speed[1]
        draw_elements(screen, bg)
        pygame.display.update()


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
    pf = Surface((20, 20))
    pf.fill(Color(ball.color))
    screen.blit(pf, (ball.x - 10, ball.y - 10))


if __name__ == "__main__":
    main()
