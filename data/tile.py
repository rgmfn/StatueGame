import data.constants as dc


class Tile:
    def __init__(
        self,
        char: str,
        fg: dc.Color,
        bg: dc.Color = dc.Color.NONE,
        description: str = None,
        name: str = None,
        is_wall: bool = False,
    ):
        self.char = char
        self.fg = fg
        self.bg = bg
        self.description = description
        self.name = name
        self.is_wall = is_wall
        self.__set_sprite(char)

    def set(self, char: str, fg: dc.Color, bg: dc.Color):
        self.char = char
        self.fg = fg
        self.bg = bg
        self.__set_sprite(char)

    def to_object(self):
        return {
            'char': self.char,
            'fg': self.fg.name,
            'bg': self.bg.name,
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
        self.sprite.set_colorkey(dc.BLACK)

    def __repr__(self):
        return self.char
