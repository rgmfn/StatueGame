import data.constants as dc
import data.tile as dt
import pygame
import json
import re


class Board:
    def __init__(
        self,
        file: str,
    ):
        self.width = dc.TILES_WIDE
        self.height = dc.TILES_TALL
        self.tiles = self.load_playscii(file)

    def load_playscii(self, file):
        new_map = []
        with open(f'assets/map/{file}.psci', 'r') as f:
            obj = json.load(f)

            map = obj['frames'][0]['layers'][0]['tiles']
            coll_layer = obj['frames'][0]['layers'][1]['tiles']
            for iy in range(dc.TILES_TALL):
                new_line = []
                for ix in range(dc.TILES_WIDE):
                    tile = map[iy*dc.TILES_WIDE+ix]
                    coll_tile = coll_layer[iy*dc.TILES_WIDE+ix]
                    print(coll_tile)
                    new_line.append(dt.Tile(
                        char=tile['char'],
                        fg=tile['fg']-1,
                        bg=tile['bg']-1,
                        is_wall=(coll_tile['bg'] == 2),  # white bg
                    ))
                new_map.append(new_line)

        with open(f'assets/map/{file}.txt', 'r') as f:
            contents = f.read()

            regex = r'(\d+)(-?\d*)\s+(\d+)(-?\d*)\s+"(.+)"\s?(\'.+\')?'
            pattern = re.compile(regex)
            matches = pattern.finditer(contents)

            for match in matches:
                x_start = match.group(1)
                x_end = match.group(2)[1:]
                y_start = match.group(3)
                y_end = match.group(4)[1:]
                text = match.group(5).upper()
                name = match.group(6)

                name = name[1:-1].upper() if name else None

                if (
                    not x_start.isnumeric() or
                    not y_start.isnumeric() or
                    (x_end != '' and
                        not x_end.isnumeric()) or
                    (y_end != '' and
                        not y_end.isnumeric())
                ):
                    continue

                if x_end == '':
                    x_end = x_start
                if y_end == '':
                    y_end = y_start

                for iy in range(int(y_start), int(y_end)+1):
                    for ix in range(int(x_start), int(x_end)+1):
                        if name:
                            new_map[iy][ix].dialogue = text
                            new_map[iy][ix].name = name
                        else:
                            new_map[iy][ix].description = text

        return new_map

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

            self.tiles = new_map

    def save(self, file: str):
        with open(f'assets/map/{file}', 'w') as f:
            new_map = []
            for line in self.tiles:
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
        for row in self.tiles:
            for tile in row:
                print(tile.fg, end=',')
            print()

    def __repr__(self):
        str = ''
        for row in self.tiles:
            for tile in row:
                str += tile
            str += '\n'

        return str

    def draw(self, screen: pygame.Surface, collision_view: bool = False):
        if self.tiles is None:
            print(self.tiles)
            return

        for iy, row in enumerate(self.tiles):
            for ix, tile in enumerate(row):
                tile.draw(screen, ix, iy, collision_view)

    def set_by_mouse(self, mouse_x: int, mouse_y: int, tile: dt.Tile,):
        map_x = (mouse_x // dc.SCALE) // dc.TILE_WIDTH
        map_y = (mouse_y // dc.SCALE) // dc.TILE_HEIGHT
        if map_x < self.width and map_y < self.height:
            self.tiles[map_y][map_x] = tile

    def get_by_mouse(self, mouse_x: int, mouse_y: int):
        map_x = (mouse_x // dc.SCALE) // dc.TILE_WIDTH
        map_y = (mouse_y // dc.SCALE) // dc.TILE_HEIGHT
        if map_x < self.width and map_y < self.height:
            return self.tiles[map_y][map_x]
        else:
            return None

    def flip_wall_mouse(self, mouse_x: int, mouse_y: int):
        tile = self.get_by_mouse(mouse_x, mouse_y)
        if tile:
            tile.flip_wall()

    def is_walkable(self, x: int, y: int):
        return (self.tiles and
                0 <= x < dc.TILES_WIDE and 0 <= y < dc.TILES_TALL and
                (not self.tiles[y][x].is_wall))

    def is_talkable(self, x: int, y: int):
        return (self.tiles and
                0 <= x < dc.TILES_WIDE and 0 <= y < dc.TILES_TALL and
                (self.tiles[y][x].name is not None) and
                (self.tiles[y][x].dialogue is not None))

    def amount_offscreen(self, x: int, y: int):
        return (x // self.width, y // self.height)

    def get_tile(self, x: int, y: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        else:
            return None
