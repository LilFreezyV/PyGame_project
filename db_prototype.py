import os
import sys
from random import randrange
import pygame
import sqlite3

with sqlite3.connect('database11.db') as db:
    pass


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


# координаты блока: 102, 97____698, 982

pygame.init()
size = width, height = 797, 780
screen = pygame.display.set_mode(size)
FPS = 30
max_x = width
max_y = height

player_1_purse = 0
player_2_purse = 0

cursor = db.cursor()

player_user = ''

field_image = load_image('field.jpg')
player_image_1 = load_image('mar.png')
player_image_2 = load_image('player_2.png')

all_sides_of_the_cube = {1: 'cube1.png', 2: 'cube2.png', 3: 'cube3.png', 4: 'cube4.png', 5: 'cube5.png', 6: 'cube6.png'}


def dice():
    list_of_all_sides_of_the_cube = list(all_sides_of_the_cube.keys())
    key1 = list_of_all_sides_of_the_cube[randrange(len(list_of_all_sides_of_the_cube))]
    key2 = list_of_all_sides_of_the_cube[randrange(len(list_of_all_sides_of_the_cube))]
    step = key1 + key2
    return load_image(all_sides_of_the_cube[key1]), load_image(all_sides_of_the_cube[key2]), key1, key2, step


class ScreenFrame(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.rect = (0, 0, 500, 500)


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


clock = pygame.time.Clock()

sprite_group = SpriteGroup()
hero_group = SpriteGroup()
dice_group = SpriteGroup()

all_sprites = SpriteGroup()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


class Player_1(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image_1
        self.rect = self.image.get_rect().move(pos_x + 15, pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            self.pos[0] + 15, self.pos[1] + 5)


class Player_2(Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image_2
        self.rect = self.image.get_rect().move(pos_x + 15, pos_y + 5)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            self.pos[0] + 15, self.pos[1] + 5)


class Dice_1(Sprite):
    def __init__(self, dice_name1, pos_x, pos_y):
        super().__init__(dice_group)
        self.image = dice_name1
        self.rect = self.image.get_rect().move(pos_x + 15, pos_y + 5)
        self.pos = (pos_x, pos_y)


class Dice_2(Sprite):
    def __init__(self, dice_name2, pos_x, pos_y):
        super().__init__(dice_group)
        self.image = dice_name2
        self.rect = self.image.get_rect().move(pos_x + 15, pos_y + 5)
        self.pos = (pos_x, pos_y)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(all_sprites)
        if x1 == x2:
            self.add(vertical_borders)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.add(horizontal_borders)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


# координаты блока: 102, 97____698, 682
# 797x780

Border(102, 97, 102, 682)
Border(102, 682, 698, 682)
Border(102, 97, 698, 97)
Border(698, 97, 698, 682)

Border(0, 0, 797, 0)
Border(0, 0, 0, 780)
Border(0, 780, 797, 780)
Border(797, 0, 797, 780)


def terminate():
    pygame.quit()
    sys.exit


def start_screen():
    intro_text = ["Добро пожаловать в монополию!!!", "",
                  "Марио приветствует вас!!!",
                  "Чтобы начать игру, нажмите любую. клавишу"]

    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('cyan'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def end_screen(player_loser):
    intro_text = ["Игра окончена!", "",
                  f"Проиграл игрок {player_loser}"]

    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def buy_or_not():
    intro_text = ["Покупать будешь?",
                  '1 - да. 2 - нет.']

    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('cyan'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    print('yes')
                    return
                elif event.type == pygame.K_2:
                    print('no')
        pygame.display.flip()
        clock.tick(FPS)


def move(hero, movement):
    x, y = hero.pos
    if movement == "up":
        if y > 0:
            hero.move(x, y - 65)
    elif movement == "down":
        if y < max_y - 1:
            hero.move(x, y + 65)
    elif movement == "left":
        if x > 0:
            hero.move(x - 65, y)
    elif movement == "right":
        if x < max_x - 1:
            hero.move(x + 65, y)


def to_jail(hero):
    hero.move(49, 690)


def switch_motion(motion):
    if motion == 1:
        motion = 2
    elif motion == 2:
        motion = 1
    return motion


start_screen()

font = pygame.font.Font(None, 30)
purses = [str(player_1_purse), str(player_2_purse)]
text_coord = 50

hero_1 = Player_1(706, 700)
hero_2 = Player_2(706, 700)

motion = 1

count_1 = 0
count_2 = 0
count_motion = 0

step = -1

double = False
double_count_1 = 0
double_count_2 = 0

in_jail_1 = False
in_jail_2 = False

running = True

person_1_steps = 0
person_2_steps = 0

dict = {'mediterranean_avenue': 0,
        'baltic_avenue': 0,
        'oriental_avenue': 0,
        'vermont_avenue': 0,
        'connecticut_avenue': 0,
        'st_charles_place': 0,
        'states_avenue': 0,
        'virginia_avenue': 0,
        'st_james_place': 0,
        'tennesee_avenue': 0,
        'new_york_avenue': 0,
        'kentucky_avenue': 0,
        'indiana_avenue': 0,
        'illinois_avenue': 0,
        'atlantic_avenue': 0,
        'ventor_avenue': 0,
        'marvin_avenue': 0,
        'pacific_avenue': 0,
        'nc_avenue': 0,
        'pennsylvania_avenue': 0,
        'park_place': 0,
        'boardwalk': 0}

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                end_screen(player_loser=player_user)
                running = False
            if event.key == pygame.K_SPACE:
                dice1_image, dice2_image, key1, key2, step = dice()
                dice_1 = Dice_1(dice1_image, 150, 550)
                dice_2 = Dice_2(dice2_image, 350, 550)
                if key1 == key2:
                    double = True
                    if motion == 1:
                        double_count_1 += 1
                    if motion == 2:
                        double_count_2 += 1
                else:
                    double = False
                    if motion == 1:
                        double_count_1 = 0
                    if motion == 2:
                        double_count_2 = 0
                if double_count_1 == 3:
                    in_jail_1 = True
                    to_jail(hero_1)
                    motion = switch_motion(motion)
                if double_count_2 == 3:
                    in_jail_2 = True
                    to_jail(hero_2)
                    motion = switch_motion(motion)
            if event.key == pygame.K_0:
                motion = switch_motion(motion)

            if motion == 1 and count_motion <= step:
                if event.key == pygame.K_UP:
                    move(hero_1, "up")
                    count_1 += 1
                    count_motion += 1
                    person_1_steps += 1
                elif event.key == pygame.K_DOWN:
                    move(hero_1, "down")
                    count_1 += 1
                    count_motion += 1
                    person_1_steps += 1
                elif event.key == pygame.K_LEFT:
                    move(hero_1, "left")
                    count_1 += 1
                    count_motion += 1
                    person_1_steps += 1
                elif event.key == pygame.K_RIGHT:
                    move(hero_1, "right")
                    count_1 += 1
                    count_motion += 1
                    person_1_steps += 1
                if person_1_steps == step:
                    query = f""" SELECT name FROM expenses WHERE id = {count_1}"""
                    cursor.execute(query)
                    for res in cursor:
                        print(res[0])
                    person_1_steps = 0
                    dict[1] = key1
                    buy_or_not()
            if motion == 2 and count_motion <= step:
                if event.key == pygame.K_UP:
                    move(hero_2, "up")
                    count_2 += 1
                    count_motion += 1
                    person_2_steps += 1
                elif event.key == pygame.K_DOWN:
                    move(hero_2, "down")
                    count_2 += 1
                    count_motion += 1
                    person_2_steps += 1
                elif event.key == pygame.K_LEFT:
                    move(hero_2, "left")
                    count_2 += 1
                    count_motion += 1
                    person_2_steps += 1
                elif event.key == pygame.K_RIGHT:
                    move(hero_2, "right")
                    count_2 += 1
                    count_motion += 1
                    person_2_steps += 1
                if person_2_steps == step:
                    query = f""" SELECT name FROM expenses WHERE id = {count_2}"""
                    cursor.execute(query)
                    for res in cursor:
                        print(res[0])
                    person_2_steps = 0
                    buy_or_not()

            if count_1 == 40:
                player_1_purse += 200
                count_1 = 0
            if count_2 == 40:
                player_2_purse += 200
                count_2 = 0

            if count_motion == step and double:
                count_motion = 0
                step = -10
            elif count_motion == step:
                motion = switch_motion(motion)
                count_motion = 0
                step = -10

    # координаты блока: 102, 97____698, 982
    string_rendered_1 = font.render(f'motion: {str(motion)}', 1, pygame.Color('black'))
    string_rendered_2 = font.render(f'step: {str(step)}', 1, pygame.Color('black'))
    string_rendered_3 = font.render(f'count_motion: {str(count_motion)}', 1, pygame.Color('black'))
    string_rendered_4 = font.render(f'count: {str(count_1), str(count_2)}', 1, pygame.Color('black'))
    string_rendered_5 = font.render(f'is double: {str(double)}', 1, pygame.Color('black'))

    screen.blit(field_image, (0, 0))
    screen.blit(string_rendered_1, (450, 100))
    screen.blit(string_rendered_2, (450, 150))
    screen.blit(string_rendered_3, (450, 200))
    screen.blit(string_rendered_4, (450, 250))
    screen.blit(string_rendered_5, (450, 300))

    sprite_group.draw(screen)
    hero_group.draw(screen)
    dice_group.draw(screen)

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
