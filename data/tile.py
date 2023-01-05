import pygame
import data.constants as dc


class Tile:
    def __init__(
        self,
        char: int,
        fg: () = None,
        bg: () = None,
        description: str = None,
        dialogue: str = None,
        name: str = None,
        is_wall: bool = False,
    ):
        # self.char = char
        # self.fg = fg
        # self.bg = bg
        self.description = description
        self.dialogue = dialogue
        self.name = name
        self.is_wall = is_wall
        # self.sprite = dc.char_sprites[char]
        self.frames = [
            (char, fg, bg)
        ]
        self.frame = 0

    def add_frame(self, frame: ()):
        assert len(frame) == 3
        assert type(frame[0]) is int
        assert type(frame[1]) is int
        assert type(frame[2]) is int
        self.frames.append(frame)

    def get_last_frame(self):
        return self.frames[-1]

    def set(
        self,
        char: int = None,
        fg: () = None,
        bg: () = None,
        description: str = None,
        dialogue: str = None,
        name: str = None,
        is_wall: bool = None,
    ):
        self.char = char if char else self.char
        self.sprite = dc.char_sprites[char]

        self.fg = fg if fg else self.fg
        self.bg = bg if bg else self.bg
        self.description = description if description else self.description
        self.dialogue = dialogue if dialogue else self.dialogue
        self.name = name if name else self.name
        self.is_wall = is_wall if is_wall else self.is_wall

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
        char, fg, bg = self.frames[self.frame]
        screen.blit(dc.SURFACES[bg], (
            x * dc.TILE_WIDTH,
            y * dc.TILE_HEIGHT,
        ))
        copy = dc.char_sprites[char].copy()
        copy.blit(dc.SURFACES[fg], (
            0, 0,
        ), special_flags=pygame.BLEND_RGBA_MIN)
        screen.blit(copy, (
            x * dc.TILE_WIDTH,
            y * dc.TILE_HEIGHT,
        ))

    def next_frame(self):
        self.frame = (self.frame + 1) % len(self.frames)

    def __repr__(self):
        return f'{self.frames[0][0]}'
