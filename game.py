from images import *
import numpy as np
import random
import pygame

SIZE = input('kSize of the desk: ').split()
SIZE = list(map(int, SIZE)) if SIZE != [] else [10, 15]
SQ_SIZE = int(min(500 / SIZE[0], 400 / SIZE[1]))
LINES = 1

# get_images(3)
get_images(4)
# get_images('f')


bounds = [0, -5] + [SIZE[0] - 1, SIZE[1] - 1]
SIZE = np.array(SIZE)
sq_size = SQ_SIZE - LINES
indent_x = int(SQ_SIZE * 2)
indent_y = int(SQ_SIZE * 2)

draw_size = SIZE * SQ_SIZE + LINES
sc_size = draw_size + np.array((indent_x, indent_y)) * 2

desk = np.zeros(SIZE)


def draw_desk():
    x = indent_x + LINES
    for i in range(SIZE[0]):
        y = indent_y + LINES
        for j in range(SIZE[1]):
            color = (WHITE if desk[i, j] == 0 else figure_col[desk[i, j]])
            pygame.draw.rect(screen, color, (x, y, sq_size, sq_size))
            y += SQ_SIZE
        x += SQ_SIZE


def can_do(figure, func, args=None):
    now_poses = figure.get_poses()
    new_poses = func(now_poses, args)
    if np.any(new_poses < bounds[:2]) or np.any(new_poses > bounds[2:]) or \
            np.any([(desk[pos[0], pos[1]] if np.all(pos >= 0) else False) != 0 for pos in new_poses]):
        return False
    return True


def move(now_poses, change):
    return now_poses + change


def rotate(now_poses, per):
    if per:
        figure_now.rotate_per()
    else:
        figure_now.rotate_out()
    return figure_now.get_poses()


def new_figure():
    global figure_now, figure_num
    figure_num += 1
    figure_now = get_figure()
    figure_now = Figure(screen, figure_now, [SIZE[0] // 2, 2 - len(figure_now)],
                        [indent_x + LINES, indent_y + LINES], SQ_SIZE, sq_size, get_color())
    if random.random() < 0.5:
        figure_now.symmetry_ver()


pygame.init()
screen = pygame.display.set_mode(sc_size)
pygame.display.set_caption('Super tetris')
timer = pygame.time.Clock()

WHITE, GRAY, BLACK = (255, 255, 255), (127, 127, 127), (0, 0, 0)

score = 0
score_font = pygame.font.SysFont('Arial', SQ_SIZE)

figure_col = {}

flame = 0
figure_num = 1
new_figure()
keep_going = True
while keep_going:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False
        if event.type == pygame.KEYDOWN:
            if event.key == 276:
                if can_do(figure_now, move, [-1, 0]):
                    figure_now.pos[0] -= 1
            elif event.key == 275:
                if can_do(figure_now, move, [1, 0]):
                    figure_now.pos[0] += 1
            elif event.key == 273:
                if not can_do(figure_now, rotate, True):
                    figure_now.rotate_out()
            elif event.key == 274:
                if not can_do(figure_now, rotate, False):
                    figure_now.rotate_per()
            elif event.key == 281:
                if can_do(figure_now, move, [0, 1]):
                    figure_now.pos[1] += 1
            elif event.key == 13:
                while can_do(figure_now, move, [0, 1]):
                    figure_now.pos[1] += 1

    screen.fill(BLACK)
    pygame.draw.rect(screen, GRAY, (indent_x, indent_y, draw_size[0], draw_size[1]))
    if flame % 30 == 0:
        if can_do(figure_now, move, [0, 1]):
            figure_now.pos[1] += 1
        else:
            flame = 0
            poses = figure_now.get_poses()
            if np.any(poses[:, 1] < 0):
                keep_going = False
            else:
                score += len(figure_now.image)
                figure_col[figure_num] = figure_now.color
                for pos in poses:
                    desk[pos[0], pos[1]] = figure_num
                for i in set(poses[:, 1]):
                    if np.all(desk[:, i] != 0):
                        desk[:, :i + 1] = list([0] + list(desk[j, :i]) for j in range(SIZE[0]))
                        score += SIZE[0]
                new_figure()
    draw_desk()
    figure_now.draw()
    pygame.draw.rect(screen, BLACK, (indent_x, 0, draw_size[0], indent_y))
    text = score_font.render('Score: ' + str(score), True, WHITE)
    text_rect = text.get_rect()
    text_rect.centerx = sc_size[0] / 2
    text_rect.y = SQ_SIZE / 2
    screen.blit(text, text_rect)
    pygame.display.update()
    timer.tick(60)
    flame += 1

pygame.quit()

