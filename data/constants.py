import pygame

spritesheet = pygame.image.load('assets/MRMOTEXT EX.png')
SPRITES_PER_ROW = 32

TILE_WIDTH = 8
TILE_HEIGHT = 8

SCALE = 4

TILES_WIDE = 20
TILES_TALL = 15

SCREEN_WIDTH = TILE_WIDTH * TILES_WIDE
SCREEN_HEIGHT = TILE_HEIGHT * TILES_TALL

DISPLAY_WIDTH = SCREEN_WIDTH * SCALE
DISPLAY_HEIGHT = SCREEN_HEIGHT * SCALE

FPS = 30

PUREBLACK = (0, 0, 0)

COLORS = []
palette_img = pygame.image.load('assets/c64_pepto.png')
for i in range(palette_img.get_width()//19):
    COLORS.append(palette_img.get_at((i*19, 0)))  # colors in png 19x19

base_surface = pygame.Surface((
    TILE_WIDTH,
    TILE_HEIGHT,
))
SURFACES = []
for color in COLORS:
    surf = base_surface.copy()
    surf.fill(color)
    SURFACES.append(surf)

char_sprites = [
    spritesheet.subsurface((
        (i % SPRITES_PER_ROW) * TILE_WIDTH,
        (i // SPRITES_PER_ROW) * TILE_HEIGHT,
        TILE_WIDTH,
        TILE_HEIGHT,
    )) for i in range(0, 1024)
]
for sprite in char_sprites:
    sprite.set_colorkey(PUREBLACK)


def get_text_sprite(char: str) -> pygame.Surface:
    if char == ' ':
        return char_sprites[0]
    else:
        return char_sprites[27*SPRITES_PER_ROW+1-33+ord(char)]
