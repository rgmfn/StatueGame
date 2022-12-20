import pygame
from enum import Enum

spritesheet = pygame.image.load('assets/spritesheet.png')
SPRITES_PER_ROW = 16

SCALE = 3
TILE_WIDTH = 8
TILE_HEIGHT = 12

TILES_WIDE = 20
TILES_TALL = 10

SCREEN_WIDTH = TILE_WIDTH * TILES_WIDE
SCREEN_HEIGHT = TILE_HEIGHT * TILES_TALL

DISPLAY_WIDTH = SCREEN_WIDTH * SCALE
DISPLAY_HEIGHT = SCREEN_HEIGHT * SCALE

PUREBLACK = (0, 0, 0)
RED = (160, 20, 10)
ORANGE = (220, 50, 20)
YELLOW = (230, 170, 30)
GREEN = (80, 135, 20)
LGREEN = (125, 185, 55)
CYAN = (25, 140, 140)
LCYAN = (60, 205, 190)
BLUE = (45, 90, 160)
LBLUE = (105, 135, 225)
PINK = (190, 110, 185)
PURPLE = (135, 60, 130)
BROWN = (150, 75, 55)
BLACK = (21, 19, 15)
GRAY = (116, 110, 113)
LGRAY = (178, 175, 172)
WHITE = (232, 227, 232)

color_names = [
    'BLACK',
    'BLUE',
    'GREEN',
    'CYAN',
    'RED',
    'PURPLE',
    'BROWN',
    'LGRAY',
    'GRAY',
    'LBLUE',
    'LGREEN',
    'LCYAN',
    'ORANGE',
    'PINK',
    'YELLOW',
    'WHITE',
    'NONE',
]
color_list = [
    BLACK,
    BLUE,
    GREEN,
    CYAN,
    RED,
    PURPLE,
    BROWN,
    LGRAY,
    GRAY,
    LBLUE,
    LGREEN,
    LCYAN,
    ORANGE,
    PINK,
    YELLOW,
    WHITE,
]
Color = Enum('Color', color_names)

base_surface = pygame.Surface((
    TILE_WIDTH,
    TILE_HEIGHT,
))
SURFACES = {Color[color]: base_surface.copy() for color in color_names}

for name, color in zip(color_names, color_list):
    SURFACES[Color[name]].fill(color)

char_sprites = [
    spritesheet.subsurface((
        (i % SPRITES_PER_ROW) * TILE_WIDTH,
        (i // SPRITES_PER_ROW) * TILE_HEIGHT,
        TILE_WIDTH,
        TILE_HEIGHT,
    )) for i in range(0, 256)
]
for sprite in char_sprites:
    sprite.set_colorkey(PUREBLACK)
