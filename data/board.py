import data.constants as dc
import data.tile as dt
import pygame
import json


class Board:
    def __init__(
        self,
    ):
        self.width = dc.TILES_WIDE
        self.height = dc.TILES_TALL
        self.map = self.create_empty(self.width, self.height)

    def load(self, file):
        with open(f'assets/map/{file}', 'r') as f:

            obj = json.loads(f.readline())
            # print(obj)

            new_map = []
            for line in obj['map']:
                new_line = []
                for tile in line:
                    new_line.append(dt.Tile(
                        char=tile['char'],
                        fg=dc.Color[tile['fg']],
                        bg=dc.Color[tile['bg']],
                        is_wall=tile['is_wall'],
                        name=tile['name'],
                        description=tile['description'],
                    ))
                new_map.append(new_line)

            self.map = new_map

    def save(self, file: str):
        with open(f'assets/map/{file}', 'w') as f:
            new_map = []
            for line in self.map:
                new_line = []
                for tile in line:
                    new_line.append(tile.to_object())
                new_map.append(new_line)

            obj = {'map': new_map, 'descriptions': []}

            f.write(json.dumps(obj))
            # print(json.dumps(obj, indent=4))

    def create_empty(self, width: int, height: int) -> []:
        map = []
        for _ in range(height):
            line_arr = []
            for _ in range(width):
                line_arr.append(dt.Tile())

            map.append(line_arr)

        return map

    def print_colors(self):
        for row in self.map:
            for tile in row:
                print(tile.fg, end=',')
            print()

    def __repr__(self):
        str = ''
        for row in self.map:
            for tile in row:
                str += tile
            str += '\n'

        return str

    def draw(self, screen: pygame.Surface, collision_view: bool = False):
        for iy, row in enumerate(self.map):
            for ix, tile in enumerate(row):
                tile.draw(screen, ix, iy, collision_view)

    def set_by_mouse(self, mouse_x: int, mouse_y: int, tile: dt.Tile,):
        map_x = (mouse_x // dc.SCALE) // dc.TILE_WIDTH
        map_y = (mouse_y // dc.SCALE) // dc.TILE_HEIGHT
        if map_x < self.width and map_y < self.height:
            self.map[map_y][map_x] = tile

    def get_by_mouse(self, mouse_x: int, mouse_y: int):
        map_x = (mouse_x // dc.SCALE) // dc.TILE_WIDTH
        map_y = (mouse_y // dc.SCALE) // dc.TILE_HEIGHT
        if map_x < self.width and map_y < self.height:
            return self.map[map_y][map_x]
        else:
            return None

    def flip_wall_mouse(self, mouse_x: int, mouse_y: int):
        tile = self.get_by_mouse(mouse_x, mouse_y)
        if tile:
            tile.flip_wall()

    def is_walkable(self, x: int, y: int):
        return (0 <= x < dc.TILES_WIDE and 0 <= y < dc.TILES_TALL and
                (not self.map[y][x].is_wall))

    def is_talkable(self, x: int, y: int):
        return (0 <= x < dc.TILES_WIDE and 0 <= y < dc.TILES_TALL and
                (self.map[y][x].name is not None))
