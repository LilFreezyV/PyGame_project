import os
import random
import sys
from random import choice, randrange
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

player_1_purse = 1500
player_2_purse = 1500

cursor = db.cursor()

player_user = ''

answer = ''

field_image = load_image('field.jpg')
player_image_1 = load_image('mar.png')
player_image_2 = load_image('player_2.png')

all_sides_of_the_cube = {1: 'cube1.png', 2: 'cube2.png', 3: 'cube3.png', 4: 'cube4.png', 5: 'cube5.png', 6: 'cube6.png'}
chances = {1: 'chance1.png', 2: 'chance2.png'}


def chance():
    global tax
    list_chances = list(chances.keys())
    _index = list_chances[randrange(len(list_chances))]
    if _index == 1:
        tax = 100
    if _index == 2:
        tax = 50
    return load_image(chances[_index]), tax


def get_chance(image):
    fon = image
    screen.blit(fon, (int((height / 2) - 75), int((width / 2) - 100)))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


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
    global answer
    intro_text = ["Покупать будешь?",
                  '1 - да. 2 - нет.']

    fon = pygame.transform.scale(load_image('fon.jpg'), size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 75)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 10, pygame.Color('cyan'))
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
                    answer = 'yes'
                    print(answer)
                    return
                if event.key == pygame.K_2:
                    answer = 'no'
                    print(answer)
                    return
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

list_of_numbers_renta = [1, 3, 6, 8, 9, 11, 13, 14, 16, 18, 19, 21, 23, 24, 26, 27, 29, 31, 32, 34, 37, 39]

dict = {'Meditieval avenue': 0,
        'Baltic avenue': 0,
        'Oriental avenue': 0,
        'Vermont avenue': 0,
        'Connecticut avenue': 0,
        'St. Charles place': 0,
        'States avenue': 0,
        'Virginia avenue': 0,
        'St. James place': 0,
        'Tennesee avenue': 0,
        'New York avenue': 0,
        'Kentucky avenue': 0,
        'Indiana avenue': 0,
        'Illinois avenue': 0,
        'Atlantic avenue': 0,
        'Ventor avenue': 0,
        'Marvin gardens': 0,
        'Pacific avenue': 0,
        'North Carolina avenue': 0,
        'Pennsylvania avenue': 0,
        'Park place': 0,
        'Boardwalk': 0}

cost_dict = {'Meditieval avenue': 60,
             'Baltic avenue': 60,
             'Oriental avenue': 100,
             'Vermont avenue': 100,
             'Connecticut avenue': 120,
             'St. Charles place': 140,
             'States avenue': 140,
             'Virginia avenue': 160,
             'St. James place': 160,
             'Tennesee avenue': 180,
             'New York avenue': 220,
             'Kentucky avenue': 220,
             'Indiana avenue': 220,
             'Illinois avenue': 240,
             'Atlantic avenue': 260,
             'Ventor avenue': 260,
             'Marvin gardens': 280,
             'Pacific avenue': 300,
             'North Carolina avenue': 300,
             'Pennsylvania avenue': 320,
             'Park place': 350,
             'Boardwalk': 400}

player_2_renta_count_dict = {'Meditieval avenue': 1,
                             'Baltic avenue': 1,
                             'Oriental avenue': 1,
                             'Vermont avenue': 1,
                             'Connecticut avenue': 1,
                             'St. Charles place': 1,
                             'States avenue': 1,
                             'Virginia avenue': 1,
                             'St. James place': 1,
                             'Tennesee avenue': 1,
                             'New York avenue': 1,
                             'Kentucky avenue': 1,
                             'Indiana avenue': 1,
                             'Illinois avenue': 1,
                             'Atlantic avenue': 1,
                             'Ventor avenue': 1,
                             'Marvin gardens': 1,
                             'Pacific avenue': 1,
                             'North Carolina avenue': 1,
                             'Pennsylvania avenue': 1,
                             'Park place': 1,
                             'Boardwalk': 1}

player_1_renta_count_dict = {'Meditieval avenue': 1,
                             'Baltic avenue': 1,
                             'Oriental avenue': 1,
                             'Vermont avenue': 1,
                             'Connecticut avenue': 1,
                             'St. Charles place': 1,
                             'States avenue': 1,
                             'Virginia avenue': 1,
                             'St. James place': 1,
                             'Tennesee avenue': 1,
                             'New York avenue': 1,
                             'Kentucky avenue': 1,
                             'Indiana avenue': 1,
                             'Illinois avenue': 1,
                             'Atlantic avenue': 1,
                             'Ventor avenue': 1,
                             'Marvin gardens': 1,
                             'Pacific avenue': 1,
                             'North Carolina avenue': 1,
                             'Pennsylvania avenue': 1,
                             'Park place': 1,
                             'Boardwalk': 1}

string_rendered_chance = font.render(' ', 1, pygame.Color('black'))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_9:
                end_screen(player_loser=player_user)
                running = False
            if event.key == pygame.K_5:
                image, tax = chance()
                get_chance(image)
                print(tax)
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
            if event.key == pygame.K_0:
                motion = switch_motion(motion)

            if motion == 1 and count_motion <= step:
                last = pygame.time.get_ticks()
                while True:
                    cooldown = 10
                    now = pygame.time.get_ticks()
                    if now - last >= cooldown:
                        last = now
                        if event.key == pygame.K_UP and hero_1.pos[0] <= 105:
                            move(hero_1, "up")
                            count_1 += 1
                            count_motion += 1
                            person_1_steps += 1
                        elif event.key == pygame.K_DOWN and hero_1.pos[0] >= 695 and hero_1.pos[1] <= 688:
                            move(hero_1, "down")
                            count_1 += 1
                            count_motion += 1
                            person_1_steps += 1
                        elif event.key == pygame.K_LEFT and hero_1.pos[1] >= 690:
                            move(hero_1, "left")
                            count_1 += 1
                            count_motion += 1
                            person_1_steps += 1
                        elif event.key == pygame.K_RIGHT and hero_1.pos[1] <= 93:
                            move(hero_1, "right")
                            count_1 += 1
                            count_motion += 1
                            person_1_steps += 1
                        break
                if person_1_steps == step:
                    person_1_steps = 0
                    if count_1 in list_of_numbers_renta:
                        cursor = db.cursor()
                        query = f""" SELECT name FROM expenses WHERE id = {count_1}"""
                        cursor.execute(query)
                        for res in cursor:
                            result = res[0]
                            print(result)
                        print(dict[result])
                        if dict[result] == 0 and player_1_purse >= cost_dict[result]:
                            buy_or_not()
                            if answer == 'yes':
                                dict[result] = 1
                                player_1_purse -= cost_dict[result]
                                if count_1 == 8:
                                    pygame.draw.circle(field_image, (0, 255, 255), (200, 696), 10)  # 8
                                elif count_1 == 1:
                                    pygame.draw.circle(field_image, (0, 255, 255), (665, 696), 10)  # 1
                                elif count_1 == 3:
                                    pygame.draw.circle(field_image, (0, 255, 255), (530, 696), 10)  # 3
                                elif count_1 == 6:
                                    pygame.draw.circle(field_image, (0, 255, 255), (339, 696), 10)  # 6
                                elif count_1 == 9:
                                    pygame.draw.circle(field_image, (0, 255, 255), (135, 696), 10)  # 9
                                elif count_1 == 21:
                                    pygame.draw.circle(field_image, (0, 255, 255), (135, 85), 10)  # 21
                                elif count_1 == 23:
                                    pygame.draw.circle(field_image, (0, 255, 255), (265, 85), 10)  # 23
                                elif count_1 == 24:
                                    pygame.draw.circle(field_image, (0, 255, 255), (339, 85), 10)  # 24
                                elif count_1 == 29:
                                    pygame.draw.circle(field_image, (0, 255, 255), (665, 85), 10)  # 29
                                elif count_1 == 27:
                                    pygame.draw.circle(field_image, (0, 255, 255), (530, 85), 10)  # 27
                                elif count_1 == 26:
                                    pygame.draw.circle(field_image, (0, 255, 255), (465, 85), 10)  # 26
                                elif count_1 == 11:
                                    pygame.draw.circle(field_image, (0, 255, 255), (89, 650), 10)  # 11
                                elif count_1 == 13:
                                    pygame.draw.circle(field_image, (0, 255, 255), (89, 520), 10)  # 13
                                elif count_1 == 14:
                                    pygame.draw.circle(field_image, (0, 255, 255), (89, 455), 10)  # 14
                                elif count_1 == 16:
                                    pygame.draw.circle(field_image, (0, 255, 255), (89, 325), 10)  # 16
                                elif count_1 == 18:
                                    pygame.draw.circle(field_image, (0, 255, 255), (89, 195), 10)  # 18
                                elif count_1 == 19:
                                    pygame.draw.circle(field_image, (0, 255, 255), (89, 130), 10)  # 19
                                elif count_1 == 31:
                                    pygame.draw.circle(field_image, (0, 255, 255), (710, 650), 10)  # 31
                                elif count_1 == 32:
                                    pygame.draw.circle(field_image, (0, 255, 255), (710, 520), 10)  # 32
                                elif count_1 == 34:
                                    pygame.draw.circle(field_image, (0, 255, 255), (710, 325), 10)  # 34
                                elif count_1 == 37:
                                    pygame.draw.circle(field_image, (0, 255, 255), (710, 195), 10)  # 37
                                elif count_1 == 39:
                                    pygame.draw.circle(field_image, (0, 255, 255), (710, 130), 10)  # 39

                        elif dict[result] == 2 and player_2_renta_count_dict[result] == 1:
                            player_2_renta_count_dict[result] += 1
                            renta = f""" SELECT renta1 FROM expenses WHERE id = {count_1}"""
                            cursor.execute(renta)
                            for res in cursor:
                                result = int(res[0])
                                print(result)
                            player_1_purse -= result
                            player_2_purse += result
                        elif dict[result] == 2 and player_2_renta_count_dict[result] == 2:
                            player_2_renta_count_dict[result] += 1
                            renta = f""" SELECT renta2 FROM expenses WHERE id = {count_1}"""
                            cursor.execute(renta)
                            for res in cursor:
                                result = int(res[0])
                                print(result)
                            player_1_purse -= result
                            player_2_purse += result
                        elif dict[result] == 2 and player_2_renta_count_dict[result] == 3:
                            renta = f""" SELECT renta3 FROM expenses WHERE id = {count_1}"""
                            cursor.execute(renta)
                            for res in cursor:
                                result = int(res[0])
                                print(result)
                            player_1_purse -= result
                            player_2_purse += result
                    elif count_1 == 7 or count_1 == 22:  # шанс
                        image, tax = chance()
                        player_1_purse -= tax
                        string_rendered_chance = font.render(f'Ваш налог: {str(tax)}', 1, pygame.Color('black'))
                    elif count_1 == 2 or count_1 == 17 or count_1 == 33 or count_1 == 4 or count_1 == 5 or count_1 == 12 \
                            or count_1 == 15 or count_1 == 25 or count_1 == 28 or count_1 == 35:  # comunity chest
                        player_1_purse -= 100
                        string_rendered_chance = font.render(f'Ваш налог: 100', 1, pygame.Color('black'))
            if motion == 2 and count_motion <= step:
                last = pygame.time.get_ticks()
                while True:
                    cooldown = 10
                    now = pygame.time.get_ticks()
                    if now - last >= cooldown:
                        last = now
                        if event.key == pygame.K_UP and hero_2.pos[0] <= 105:
                            move(hero_2, "up")
                            count_2 += 1
                            count_motion += 1
                            person_2_steps += 1
                        elif event.key == pygame.K_DOWN and hero_2.pos[0] >= 695 and hero_2.pos[1] <= 688:
                            move(hero_2, "down")
                            count_2 += 1
                            count_motion += 1
                            person_2_steps += 1
                        elif event.key == pygame.K_LEFT and hero_2.pos[1] >= 690:
                            move(hero_2, "left")
                            count_2 += 1
                            count_motion += 1
                            person_2_steps += 1
                        elif event.key == pygame.K_RIGHT and hero_1.pos[1] <= 93:
                            move(hero_2, "right")
                            count_2 += 1
                            count_motion += 1
                            person_2_steps += 1
                        break
                if person_2_steps == step:
                    person_2_steps = 0
                    if count_2 in list_of_numbers_renta:
                        cursor = db.cursor()
                        query = f""" SELECT name FROM expenses WHERE id = {count_2}"""
                        cursor.execute(query)
                        for res in cursor:
                            result = res[0]
                            print(result)
                        print(dict[result])
                        if dict[result] == 0 and player_2_purse >= cost_dict[result]:
                            buy_or_not()
                            if answer == 'yes':
                                dict[result] = 2
                                player_2_purse -= cost_dict[result]
                                if count_2 == 8:
                                    pygame.draw.circle(field_image, (255, 96, 208), (200, 696), 10)  # 8
                                elif count_2 == 1:
                                    pygame.draw.circle(field_image, (255, 96, 208), (665, 696), 10)  # 1
                                elif count_2 == 3:
                                    pygame.draw.circle(field_image, (255, 96, 208), (530, 696), 10)  # 3
                                elif count_2 == 6:
                                    pygame.draw.circle(field_image, (255, 96, 208), (339, 696), 10)  # 6
                                elif count_2 == 9:
                                    pygame.draw.circle(field_image, (255, 96, 208), (135, 696), 10)  # 9
                                elif count_2 == 21:
                                    pygame.draw.circle(field_image, (255, 96, 208), (135, 85), 10)  # 21
                                elif count_2 == 23:
                                    pygame.draw.circle(field_image, (255, 96, 208), (265, 85), 10)  # 23
                                elif count_2 == 24:
                                    pygame.draw.circle(field_image, (255, 96, 208), (339, 85), 10)  # 24
                                elif count_2 == 29:
                                    pygame.draw.circle(field_image, (255, 96, 208), (665, 85), 10)  # 29
                                elif count_2 == 27:
                                    pygame.draw.circle(field_image, (255, 96, 208), (530, 85), 10)  # 27
                                elif count_2 == 26:
                                    pygame.draw.circle(field_image, (255, 96, 208), (465, 85), 10)  # 26
                                elif count_2 == 11:
                                    pygame.draw.circle(field_image, (255, 96, 208), (89, 650), 10)  # 11
                                elif count_2 == 13:
                                    pygame.draw.circle(field_image, (255, 96, 208), (89, 520), 10)  # 13
                                elif count_2 == 14:
                                    pygame.draw.circle(field_image, (255, 96, 208), (89, 455), 10)  # 14
                                elif count_2 == 16:
                                    pygame.draw.circle(field_image, (255, 96, 208), (89, 325), 10)  # 16
                                elif count_2 == 18:
                                    pygame.draw.circle(field_image, (255, 96, 208), (89, 195), 10)  # 18
                                elif count_2 == 19:
                                    pygame.draw.circle(field_image, (255, 96, 208), (89, 130), 10)  # 19
                                elif count_2 == 31:
                                    pygame.draw.circle(field_image, (255, 96, 208), (710, 650), 10)  # 31
                                elif count_2 == 32:
                                    pygame.draw.circle(field_image, (255, 96, 208), (710, 520), 10)  # 32
                                elif count_2 == 34:
                                    pygame.draw.circle(field_image, (255, 96, 208), (710, 325), 10)  # 34
                                elif count_2 == 37:
                                    pygame.draw.circle(field_image, (255, 96, 208), (710, 195), 10)  # 37
                                elif count_2 == 39:
                                    pygame.draw.circle(field_image, (255, 96, 208), (710, 130), 10)  # 39
                        elif dict[result] == 1 and player_1_renta_count_dict[result] == 1:
                            player_1_renta_count_dict[result] += 1
                            renta = f""" SELECT renta1 FROM expenses WHERE id = {count_2}"""
                            cursor.execute(renta)
                            for res in cursor:
                                result = int(res[0])
                                print(result)
                            player_2_purse -= result
                            player_1_purse += result
                        elif dict[result] == 1 and player_1_renta_count_dict[result] == 2:
                            player_1_renta_count_dict[result] += 1
                            renta = f""" SELECT renta2 FROM expenses WHERE id = {count_2}"""
                            cursor.execute(renta)
                            for res in cursor:
                                result = int(res[0])
                                print(result)
                            player_2_purse -= result
                            player_1_purse += result
                        elif dict[result] == 1 and player_1_renta_count_dict[result] == 3:
                            renta = f""" SELECT renta3 FROM expenses WHERE id = {count_2}"""
                            cursor.execute(renta)
                            for res in cursor:
                                result = int(res[0])
                                print(result)
                            player_2_purse -= result
                            player_1_purse += result
                    elif count_2 == 7 or count_2 == 22:  # шанс
                        image, tax = chance()
                        player_1_purse -= tax
                        string_rendered_chance = font.render(f'Ваш налог: {str(tax)}', 1, pygame.Color('black'))
                    elif count_2 == 2 or count_2 == 17 or count_2 == 33 or count_2 == 4 or count_2 == 5 or count_2 == 12 \
                            or count_2 == 15 or count_2 == 25 or count_2 == 28 or count_2 == 35:  # comunity chest
                        player_2_purse -= 100
                        string_rendered_chance = font.render(f'Ваш налог: 100', 1, pygame.Color('black'))

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
            if player_1_purse < 0:
                end_screen('player 1')
            if player_2_purse < 0:
                end_screen('player 2')


    # координаты блока: 102, 97____698, 982
    string_rendered_1 = font.render(f'player 1 purse: {str(player_1_purse)}', 1, pygame.Color('black'))
    string_rendered_2 = font.render(f'player 2 purse: {str(player_2_purse)}', 1, pygame.Color('black'))

    screen.blit(field_image, (0, 0))
    screen.blit(string_rendered_chance, (450, 100))
    screen.blit(string_rendered_1, (450, 150))
    screen.blit(string_rendered_2, (450, 200))

    sprite_group.draw(screen)
    hero_group.draw(screen)
    dice_group.draw(screen)

    clock.tick(FPS)
    pygame.display.flip()

pygame.quit()
