import data.constants as dc
import pygame
import json


class Tile:
    def __init__(
        self,
        char: str,
        color: dc.Color,
        description: str = None,
        name: str = None,
        is_wall: bool = False,
    ):
        self.char = char
        self.color = color
        self.description = description
        self.name = name
        self.is_wall = is_wall
        self.__set_sprite(char)

    def set(self, char: str, color: dc.Color):
        self.char = char
        self.color = color
        self.__set_sprite(char)

    def to_object(self):
        return {
            'char': self.char,
            'color': self.color.name,
            'is_wall': self.is_wall,
        }

    def flip_wall(self):
        self.is_wall = not self.is_wall

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
    with open(f'assets/map/{file}', 'r') as f:

        obj = json.loads(f.readline())
        # print(obj)

        new_map = []
        for line in obj['map']:
            new_line = []
            for tile in line:
                new_line.append(Tile(
                    char=tile['char'],
                    color=dc.Color[tile['color']],
                    is_wall=tile['is_wall']
                ))
            new_map.append(new_line)

        return new_map


def save_map(map: [], file: str):
    with open(f'assets/map/{file}', 'w') as f:
        new_map = []
        for line in map:
            new_line = []
            for tile in line:
                new_line.append(tile.to_object())
            new_map.append(new_line)

        obj = {'map': new_map, 'descriptions': []}

        f.write(json.dumps(obj))


def empty_map(width: int, height: int):
    map = []
    for _ in range(height):
        line_arr = []
        for _ in range(width):
            line_arr.append(
                Tile(
                    char=' ',
                    color=dc.Color.WHITE,
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


def draw_map(screen: pygame.Surface, map: [], collision_view: bool = False):
    for iy, row in enumerate(map):
        for ix, tile in enumerate(row):
            screen.blit(tile.sprite, (
                ix * dc.TILE_WIDTH,
                iy * dc.TILE_HEIGHT
            ))
            if collision_view and tile.is_wall:
                screen.blit(dc.SURFACES[tile.color], (
                    ix * dc.TILE_WIDTH,
                    iy * dc.TILE_HEIGHT,
                ), special_flags=pygame.BLEND_RGB_MAX)
            else:
                screen.blit(dc.SURFACES[tile.color], (
                    ix * dc.TILE_WIDTH,
                    iy * dc.TILE_HEIGHT,
                ), special_flags=pygame.BLEND_RGB_MIN)


"""
TODO
 change class
 make santa wishlist
 make amazon wishlist
 decide what to get family
"""
