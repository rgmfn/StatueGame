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

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (133, 142, 209)
RED = (185, 11, 11)  # TODO too close to pink, not red enough
ORANGE = (255, 174, 66)  # TODO too close to yellow
YELLOW = (212, 175, 55)
GREEN = (37, 142, 112)
BLUE = (52, 142, 199)
PURPLE = (126, 78, 172)
PINK = (220, 55, 83)

color_names = [
    'WHITE', 'GRAY', 'RED', 'ORANGE', 'YELLOW', 'GREEN',
    'BLUE', 'PURPLE', 'PINK', 'BLACK', 'NONE'
]
color_list = [
    WHITE, GRAY, RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, PINK, BLACK
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
    sprite.set_colorkey(BLACK)
