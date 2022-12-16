import data.constants as dc
import pygame


class Tile:
    def __init__(
        self,
        char: str,
        color: dc.Color,
        description: str,
        name: str = None,
    ):
        self.char = char
        self.color = color
        self.description = description
        self.name = name
        self.__set_sprite(char)

    def set(self, char: str, color: dc.Color):
        self.char = char
        self.color = color
        self.__set_sprite(char)

    def __set_sprite(self, char: str):
        self.sprite = dc.spritesheet.subsurface((
            (ord(char) % dc.SPRITES_PER_ROW) * dc.TILE_WIDTH,
            (ord(char) // dc.SPRITES_PER_ROW) * dc.TILE_HEIGHT,
            dc.TILE_WIDTH,
            dc.TILE_HEIGHT,
        ))

    def __repr__(self):
        return self.char


def load_map(file) -> []:
    f = open(f'assets/map/{file}', 'r')
    lines = f.readlines()

    map = []
    for line in lines:
        line = line.replace('\n', '')
        line_arr = []
        for char in line:
            line_arr.append(
                Tile(
                    char=char,
                    color=dc.Color.RED,
                    description='',
                )
            )

        map.append(line_arr)

    return map


def print_map(map):
    for row in map:
        for tile in row:
            print(tile, end='')
        print()


def draw_map(screen: pygame.Surface, map: []):
    for iy, row in enumerate(map):
        for ix, tile in enumerate(row):
            screen.blit(tile.sprite, (
                ix * dc.TILE_WIDTH,
                iy * dc.TILE_HEIGHT
            ))
            screen.blit(dc.SURFACES[tile.color], (
                ix * dc.TILE_WIDTH,
                iy * dc.TILE_HEIGHT,
            ), special_flags=pygame.BLEND_RGB_MIN)

# TODO add save function
