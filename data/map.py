import data.constants as dc


def load_map(file, spritesheet, sprites_per_row=16) -> []:
    f = open(f'assets/map/{file}', 'r')
    lines = f.readlines()

    map = []
    for line in lines:
        line = line.replace('\n', '')
        line_arr = []
        for char in line:
            line_arr.append({
                'char': char,
                'color': dc.Color.RED,
                'description': '',
                'sprite': spritesheet.subsurface((
                    (ord(char) % sprites_per_row) * dc.TILE_WIDTH,
                    (ord(char) // sprites_per_row) * dc.TILE_HEIGHT,
                    dc.TILE_WIDTH,
                    dc.TILE_HEIGHT,
                )),
            })

        map.append(line_arr)

    return map


def print_map(map):
    for row in map:
        for tile in row:
            print(tile['char'], end='')
        print()
