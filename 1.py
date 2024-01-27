from random import randrange
import os

import pygame


def load_image(name, color_key=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname).convert_alpha()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


all_sides_of_the_cube = {1: 'cube1.png', 2: 'cube2.png', 3: 'cube3.png', 4: 'cube4.png', 5: 'cube5.png', 6: 'cube6.png'}


def dice():
    list_of_all_sides_of_the_cube = list(all_sides_of_the_cube.keys())
    key1 = list_of_all_sides_of_the_cube[randrange(len(list_of_all_sides_of_the_cube))]
    key2 = list_of_all_sides_of_the_cube[randrange(len(list_of_all_sides_of_the_cube))]
    step = key1 + key2
    print(f'key1 = {key1}')
    print(f'key2 = {key2}')
    print(f'step = {step}')
    return load_image(all_sides_of_the_cube[key1]), load_image(all_sides_of_the_cube[key2]), key1, key2, step


dice1_image, dice2_image, key1, key2, step = dice()
print(key1)
print(key2)
print(step)

