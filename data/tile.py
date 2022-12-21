import pygame
import data.constants as dc


class Tile:
    def __init__(
        self,
        char: str = ' ',
        fg: dc.Color = dc.Color.NONE,
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
        self.sprite = dc.char_sprites[ord(char)]

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
            'name': self.name,
            'description': self.description,
        }

    def flip_wall(self):
        self.is_wall = not self.is_wall

    def copy(self):
        return Tile(
            char=self.char,
            fg=self.fg,
            bg=self.bg,
            description=self.description,
            name=self.name,
            is_wall=self.is_wall,
        )

    def draw(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        collision_view: bool = False,
    ):
        fg = self.bg if collision_view and self.is_wall else self.fg
        bg = self.fg if collision_view and self.is_wall else self.bg
        screen.blit(dc.SURFACES[bg], (
            x * dc.TILE_WIDTH,
            y * dc.TILE_HEIGHT,
        ))
        copy = self.sprite.copy()
        copy.blit(dc.SURFACES[fg], (
            0, 0,
        ), special_flags=pygame.BLEND_RGBA_MIN)
        screen.blit(copy, (
            x * dc.TILE_WIDTH,
            y * dc.TILE_HEIGHT,
        ))

    def __repr__(self):
        return self.char
