import data.constants as dc
import data.map as dm
import pygame

char_sprites = [
    dc.spritesheet.subsurface((
        (i % dc.SPRITES_PER_ROW) * dc.TILE_WIDTH,
        (i // dc.SPRITES_PER_ROW) * dc.TILE_HEIGHT,
        dc.TILE_WIDTH,
        dc.TILE_HEIGHT,
    )) for i in range(0, 256)
]
TOP_LEFT = char_sprites[218]
TOP_RIGHT = char_sprites[191]
BOTTOM_LEFT = char_sprites[192]
BOTTOM_RIGHT = char_sprites[217]
SIDE = char_sprites[179]
TOP = char_sprites[196]


class Popup:
    def __init__(
        self,
        num_lines: int,
        line_width: int,
        side_margin: int,
        top_margin: int,
        does_input: bool = False,
        line_space: int = 1,  # the space between lines (0 or 1)
    ):
        self.num_lines: int = num_lines
        self.line_width: int = line_width
        self.does_input: str = does_input
        self.input = ''
        self.line_space: int = line_space

        self.side_margin: int = side_margin
        self.top_margin: int = top_margin

        self.text: [str] = None
        self.box_num: int = 0
        self.x: int = None
        self.y: int = None
        self.w: int = None
        self.h: int = None
        self.speaker: dm.Tile = None

        self.box_width: int = self.side_margin*2 + self.line_width
        self.box_height: int = (
            self.top_margin*2 + self.num_lines*(self.line_space+1) -
            self.line_space
        )

        self.is_set = False

    def set(
            self,
            text: [str],
            pos: pygame.Rect = pygame.Rect(0, 0, 0, 0,),
            speaker: dm.Tile = None,
    ):
        self.is_set = True
        self.text = text
        self.box_num = 0
        self.input = ''
        self.x = pos.x
        self.y = pos.y
        self.w = pos.w
        self.h = pos.h
        self.speaker = speaker

        self.parse_text()

    def next(self):
        """
        Returns True if there is still more text.
        """
        self.box_num += 1
        return self.box_num == len(self.text)

    def type(self, unicode: str):
        if not self.does_input:
            return

        if unicode == '\x08':
            self.input = self.input[:-1] if len(self.input) > 1 else ''
        elif len(self.input)+1 <= self.line_width:
            self.input += unicode

        # print(self.input)

    def parse_text(self):
        parsed_text = []

        for phrase in self.text:
            box = []
            words = phrase.split(' ')
            line = ''
            space_left = self.line_width

            while len(words) > 0:
                word = words.pop(0)

                # if space_left >= len(word):
                #     line += word
                #     space_left -= len(word)
                # else:
                #     box.append(line)
                #     line = word
                #     space_left = self.line_width - len(word)

                # if space_left >= 1:
                #     line += ' '
                #     space_left -= 1
                # else:
                #     box.append(line)
                #     line = ''
                #     space_left = self.line_width

                if space_left == self.line_width:
                    line += word
                    space_left -= len(word)
                elif space_left < len(word)+1:
                    box.append(line)
                    line = word
                    space_left = self.line_width - len(word)
                else:
                    line += f' {word}'
                    space_left -= len(word)+1

                if len(box) == self.num_lines:
                    parsed_text.append(box)
                    box = []

            box.append(line)
            parsed_text.append(box)

        self.text = parsed_text

        # print(self.text)

    def display_top(self, screen: pygame.Surface):
        screen.blit(TOP_LEFT, (
            self.x*dc.TILE_WIDTH,
            self.y*dc.TILE_HEIGHT,
        ))

        for ix in range(self.box_width):
            if self.speaker and ix < len(self.speaker.name):
                for c in self.speaker.name:
                    pass
                    # screen.blit(alphabet_sprites()

                    # )
            else:
                screen.blit(TOP, (
                    (self.x+ix+1)*dc.TILE_WIDTH,  # +1 bc not top left
                    self.y*dc.TILE_HEIGHT,
                ))

        screen.blit(TOP_RIGHT, (
            (self.x+self.box_width+1)*dc.TILE_WIDTH,
            self.y*dc.TILE_HEIGHT,
        ))

    def display_bottom(self, screen: pygame.Surface):
        screen.blit(BOTTOM_LEFT, (
            self.x*dc.TILE_WIDTH,
            (self.y+self.box_height+1)*dc.TILE_HEIGHT,
        ))

        for ix in range(self.box_width):
            if (self.box_num < len(self.text)-1 and
                    self.box_width-5 < ix < self.box_width-1):
                screen.blit(char_sprites['.'], (
                    (self.x+ix+1)*dc.TILE_WIDTH,  # +1 bc not top left
                    (self.y+self.box_height+1)*dc.TILE_HEIGHT,
                ))
            else:
                screen.blit(TOP, (
                    (self.x+ix+1)*dc.TILE_WIDTH,  # +1 bc not top left
                    (self.y+self.box_height+1)*dc.TILE_HEIGHT,
                ))

        screen.blit(BOTTOM_RIGHT, (
            (self.x+self.box_width+1)*dc.TILE_WIDTH,
            (self.y+self.box_height+1)*dc.TILE_HEIGHT,
        ))

    def display_sides(self, screen: pygame.Surface):
        for iy in range(self.box_height):
            # left side
            screen.blit(SIDE, (
                self.x*dc.TILE_WIDTH,
                (self.y+iy+1)*dc.TILE_HEIGHT,
            ))
            # right side
            screen.blit(SIDE, (
                (self.x+self.box_width+1)*dc.TILE_WIDTH,
                (self.y+iy+1)*dc.TILE_HEIGHT,
            ))

    def display_text(self, screen: pygame.Surface):
        box = self.text[self.box_num]
        for iy, line in enumerate(box):
            for ix, char in enumerate(line):
                if char != ' ':
                    screen.blit(char_sprites[ord(char)], (
                        (self.x+self.side_margin+ix+1)*dc.TILE_WIDTH,
                        (self.y+self.top_margin+1 +
                            iy*(self.line_space+1))*dc.TILE_HEIGHT)
                    )

    def display_input(self, screen: pygame.Surface):
        assert self.num_lines >= 2  # needs 2 lines for input
        box = self.text[0]
        line = box[0]
        for ix, char in enumerate(line):
            if char != ' ':
                screen.blit(char_sprites[ord(char)], (
                    (self.x+self.side_margin+ix+1)*dc.TILE_WIDTH,
                    (self.y+self.top_margin+1)*dc.TILE_HEIGHT)
                )
        ix = 0
        for char in self.input:
            if char != ' ':
                screen.blit(char_sprites[ord(char)], (
                    (self.x+self.side_margin+ix+1)*dc.TILE_WIDTH,
                    (self.y+self.top_margin+1 +
                        self.line_space+1)*dc.TILE_HEIGHT)
                )
            ix += 1
        if ix < self.line_width:
            screen.blit(char_sprites[ord('_')], (
                (self.x+self.side_margin+ix+1)*dc.TILE_WIDTH,
                (self.y+self.top_margin+1 +
                    self.line_space+1)*dc.TILE_HEIGHT)
            )

    def display(self, screen: pygame.Surface):
        if not self.is_set:
            print('Error: popup not set')
            return

        # TODO render scaled black sheet below popup

        self.display_top(screen)
        self.display_bottom(screen)
        self.display_sides(screen)

        if self.does_input:
            self.display_input(screen)
        else:
            self.display_text(screen)
