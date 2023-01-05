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
        self.moving_tiles = set()
        self.tiles = self.load(file)

    def load(self, file) -> []:
        with open(f'assets/map/{file}.psci', 'r') as f:
            obj = json.load(f)
            tiles = self.__load_tiles(
                obj['frames'][0]['layers'][0]['tiles']
            )
            self.__load_animations(tiles, obj)
            self.__load_collisions(
                tiles,
                obj['frames'][0]['layers'][1]['tiles']
            )
            self.__load_descriptions(tiles, file)

            return tiles

        return None  # unreachable?

    def __load_tiles(self, tiles: []) -> []:
        new_map = []

        row = []
        for i, tile in enumerate(tiles):
            row.append(dt.Tile(
                char=tile['char'],
                fg=tile['fg']-1,  # colors in psci file are 1 indexed
                bg=tile['bg']-1,
            ))
            if i % dc.TILES_WIDE == dc.TILES_WIDE-1:
                new_map.append(row)
                row = []

        return new_map

    def __load_animations(self, tiles: [], obj: {}):
        for i in range(1, len(obj['frames'])):
            frame = obj['frames'][i]['layers'][0]['tiles']
            for j, frame_tile in enumerate(frame):
                if (
                    frame_tile['fg'] != 0 and
                    frame_tile['bg'] != 0
                ):
                    tiles[
                        j // dc.TILES_WIDE
                    ][
                        j % dc.TILES_WIDE
                    ].add_frame((
                        frame_tile['char'],
                        frame_tile['fg']-1,
                        frame_tile['bg']-1,
                    ))
                    self.moving_tiles.add((
                        j % dc.TILES_WIDE,
                        j // dc.TILES_WIDE,
                    ))

    def __load_collisions(self, tiles: [], collision_tiles: []):
        for i, tile in enumerate(collision_tiles):
            if tile['fg'] == 2 or tile['bg'] == 2:
                tiles[
                    i // dc.TILES_WIDE
                ][
                    i % dc.TILES_WIDE
                ].is_wall = True

    def __load_descriptions(self, tiles: [], file: str):
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
                            tiles[iy][ix].dialogue = text
                            tiles[iy][ix].name = name
                        else:
                            tiles[iy][ix].description = text

    # TODO split into helper methods methods
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
                    # print(coll_tile)
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

    def update_animations(self):
        """
        Updates the animations for the tiles that have animations on the
        current board.
        """
        for ix, iy in self.moving_tiles:
            self.tiles[iy][ix].next_frame()

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
