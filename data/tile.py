import pygame
import re
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
        event_name: str = None,
    ):
        # self.char = char
        self.fg = fg  # fg of first frame
        self.bg = bg  # bg of first frame
        self.description = description
        self.dialogue = dialogue
        self.name = name
        self.is_wall = is_wall
        # self.sprite = dc.char_sprites[char]
        self.frames = [
            (char, fg, bg)
        ]
        self.frame = 0
        self.event_name = event_name

    def run_event(self, map: []):
        """
        Runs the events in the event file if there is an event file.
        """
        if not self.event_name:
            return

        print(f'running event {self.event_name}')
        with open(f'assets/events/{self.event_name}.event', 'r') as f:
            contents = f.read()

            # TODO clean up optional arguments
            regex = r'(\d+)\s(\d+)\s(\d+)\s(\d+)\s\((.+),\s(.+),\s(.+)\)\s"(.+)"\s(\'.+\')?\s?(\w+)?'
            pattern = re.compile(regex)
            matches = pattern.finditer(contents)

            for match in matches:
                map_x = int(match.group(1))
                map_y = int(match.group(2))
                board_x = int(match.group(3))
                board_y = int(match.group(4))
                char = match.group(5)
                fg = match.group(6)
                bg = match.group(7)
                text = match.group(8).upper()

                if match.group(9) != '':
                    name = match.group(9)[1:-1].upper()

                if match.group(10):
                    target_file = match.group(10)
                else:
                    target_file = None

                target = map.get_board(map_x, map_y).get_tile(board_x, board_y)

                if name and name != '-':
                    target.set(name=name)

                if text != '-':
                    if name:
                        target.set(dialogue=text)
                    else:
                        target.set(description=text)

                target.event_name = target_file
                print(f'event effects {target.name}')

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
        # char: int = None,
        fg: () = None,
        bg: () = None,
        frames: [] = None,
        description: str = None,
        dialogue: str = None,
        name: str = None,
        is_wall: bool = None,
    ):
        # self.char = char if char else self.char
        # self.sprite = dc.char_sprites[char]

        self.frames = frames if frames else self.frames
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
