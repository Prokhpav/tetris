import numpy as np
import random
import pygame

images = {}
all_images = []


def get_image(size, num: int):
    f = open('figures/%s' % str(size), 'r').read().split('\n\n')[num].split('\n')
    a = list(map(lambda i: i.split(' '), f[:-1]))
    poses = []
    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] == '#':
                poses.append([i, j])
    return np.array(poses) - list(map(int, f[-1].split(' ')))


def get_images(num):
    f = open('figures/%s' % str(num), 'r').read().split('\n\n')
    if num not in images:
        images[num] = []
    for i in range(len(f)):
        image = get_image(num, i)
        images[num].append(image)
        all_images.append(image)


def get_figure():
    return random.choice(all_images)


def get_color():
    col = [32, 32, 32]
    col[random.randint(0, 2)] = random.randint(191, 223)
    for i in range(3):
        col[i] += random.randint(-32, 32)
    return col


class Figure:
    def __init__(self, parent, image, pos, ppos, size, sq_size, color=(255, 255, 255)):
        self.parent = parent
        self.image = image
        self.pos = np.array(pos)
        self.ppos = ppos
        self.size = size
        self.sq_size = sq_size
        self.color = color

    def draw(self):
        for pos in self.image:
            x, y = (self.pos + pos) * self.size + self.ppos
            pygame.draw.rect(self.parent, self.color, (x, y, self.sq_size, self.sq_size))

    def get_poses(self):
        return self.image + self.pos

    def rotate_per(self):
        self.image[:, 1], self.image[:, 0] = self.image[:, 0], -self.image[:, 1]
    def rotate_out(self):
        self.image[:, 0], self.image[:, 1] = self.image[:, 1], -self.image[:, 0]
    def symmetry_hor(self):
        self.image[:, 1] = -self.image[:, 1]
    def symmetry_ver(self):
        self.image[:, 0] = -self.image[:, 0]

    def copy(self):
        return Figure(self.parent, self.image, self.pos, self.ppos, self.size, self.sq_size, self.color)


def collision(desk, figure: Figure, bounds, change, func):  # bounds: [min_x, min_y, max_x, max_y]
    now_poses = figure.get_poses()
    new_poses = now_poses + change
    if np.any(new_poses < bounds[:2]) or np.any(new_poses > bounds[2:]) or np.any([np.all(desk[pos[0], pos[1]] != (0, 0, 0)) for pos in new_poses]):
        return func(now_poses, new_poses, figure, change)
    figure.pos += change
    return False
