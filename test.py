import pygame
import sys
import os
import random
from math import floor
import time
FPS = 50
# размеры окна:
x, y = 800, 500
size = width, height = x, y
clock = pygame.time.Clock()
toch = []
kol_mobov = 0
on = 0
kol_m = 3


def terminate():
    pygame.quit()
    sys.exit()


# Загрузка изображений
def load_image(name, colorkey=None):
    fullname = name
    image = pygame.image.load(fullname).convert()
    # colorkey цвет заднего фона
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


# Загрузка уровня
def load_level(filename):
    filename = filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('W')
    return list(map(lambda x: x.ljust(max_width, 'W'), level_map))


# Заставка
def start_screen():
    intro_text = []

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
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
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


# Генерация уровня
def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                # Дорога
                Tile('road', x, y)
            elif level[y][x] == '@':
                # Человек
                Tile('road', x, y)
                x1 = x
                y1 = y
            else:
                # Пустота
                Tile('black', x, y)
    player = Player(x1, y1)
    # вернем игрока, а также размер поля в клетках
    return player, x, y


# Блоки
class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type != 'black':
            super().__init__(tiles_group, all_sprites)
        else:
            super().__init__(tiles_group, all_sprites, blocker)
        self.image = tile_images[tile_type]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(tile_width * pos_x,
                                               tile_height * pos_y)
        self.type1 = tile_type


# Игрок
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.mask = pygame.mask.from_surface(player_image)
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15,
                                               tile_height * pos_y + 5)
        self.nx = tile_width * pos_x + 15
        self.ny = tile_height * pos_y + 5
        self.x = tile_width * pos_x + 15
        self.y = tile_height * pos_y + 5
        self.zd = 5
        self.ub = 0

# Камера
class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy


    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)

# Основная функция
def run():
    global toch, kol_mobov, on
    # Генерация уровня
    level = load_level('one.txt')
    player, level_x, level_y = generate_level(level)
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    all_sprites.draw(screen)
    pygame.display.flip()
    running = True
    d = 0
    p = 0
    op1 = []
    inr = 0
    shagat = 0
    shag1 = 1
    while running:
        screen.fill((0,0,0))
        # Управление
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                on = 1
            if event.type == pygame.KEYUP:
                if op1.count(event.key) != 0:
                    op1.remove(event.key)
            if event.type == pygame.KEYDOWN:
                op1.append(event.key)
        # Нажатые команды игроком
        for op in op1:
            if op in [100, 97, 119, 115] and inr == 0:
                shagat += 1
                if shagat % 50 == 0:
                    d = (d + 1) % 2
                shag = shag1
                if op == 100:
                    player.rect.x += shag
                    player.x += shag
                    p = 0
                    os = 0
                    for sprite in blocker:
                        if pygame.sprite.collide_mask(sprite, player):
                            os = 1
                    if os == 1:
                        player.rect.x -= shag
                        player.x -= shag
                elif op == 97:
                    p = 2
                    os = 0
                    player.rect.x -= shag
                    player.x -= shag
                    for sprite in blocker:
                        if pygame.sprite.collide_mask(sprite, player):
                            os = 1
                    if os == 1:
                        player.rect.x += shag
                        player.x += shag
                elif op == 119:
                    os = 0
                    player.rect.y -= shag
                    player.y -= shag
                    for sprite in blocker:
                        if pygame.sprite.collide_mask(sprite, player):
                            os = 1
                    if os == 1:
                        player.rect.y += shag
                        player.y += shag
                elif op == 115:
                    os = 0
                    player.rect.y += shag
                    player.y += shag
                    for sprite in blocker:
                        if pygame.sprite.collide_mask(sprite, player):
                            os = 1
                    if os == 1:
                        player.rect.y -= shag
                        player.y -= shag
                camera.update(player)
                # обновляем положение всех спрайтов
                online = 0
                for sprite in all_sprites:
                    camera.apply(sprite)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()


# инициализация Pygame:
pygame.init()

# screen — холст, на котором нужно рисовать:
screen = pygame.display.set_mode(size)

# формирование кадра:
# команды рисования на холсте
# ...

tile_images = {
    # Дорога
    'road': load_image('grass.png'),
    # Пустота
    'black': load_image('box.png'),
}
# Игрок
player_image = load_image('mar.png', -1)

# Размер блока
tile_width = tile_height = 50

start_screen()
player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
mobs_group = pygame.sprite.Group()
blocker = pygame.sprite.Group()
camera = Camera()
run()
# завершение работы:
pygame.quit()
