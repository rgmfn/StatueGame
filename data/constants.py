import pygame
from enum import Enum

SCALE = 4
TILE_WIDTH = 8
TILE_HEIGHT = 12

TILES_WIDE = 10
TILES_TALL = 10

SCREEN_WIDTH = TILE_WIDTH * TILES_WIDE
SCREEN_HEIGHT = TILE_HEIGHT * TILES_TALL

DISPLAY_WIDTH = SCREEN_WIDTH * SCALE
DISPLAY_HEIGHT = SCREEN_HEIGHT * SCALE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

Color = Enum('Color', ['WHT', 'RED', 'BLU', 'GRN'])

SURFACES = {
    Color.WHT: pygame.Surface((
        TILE_WIDTH,
        TILE_HEIGHT,
    )),
    Color.RED: pygame.Surface((
        TILE_WIDTH,
        TILE_HEIGHT,
    )),
    Color.BLU: pygame.Surface((
        TILE_WIDTH,
        TILE_HEIGHT,
    )),
    Color.GRN: pygame.Surface((
        TILE_WIDTH,
        TILE_HEIGHT,
    )),
}

SURFACES[Color.WHT].fill(WHITE)
SURFACES[Color.RED].fill(RED)
SURFACES[Color.BLU].fill(BLUE)
SURFACES[Color.GRN].fill(GREEN)
