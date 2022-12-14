import data.constants as dc
import data.tile as dt
import pygame

TOP_LEFT = dc.char_sprites[16*dc.SPRITES_PER_ROW+18]
TOP_RIGHT = dc.char_sprites[16*dc.SPRITES_PER_ROW+19]
BOTTOM_LEFT = dc.char_sprites[17*dc.SPRITES_PER_ROW+18]
BOTTOM_RIGHT = dc.char_sprites[17*dc.SPRITES_PER_ROW+19]
LEFT_SIDE = dc.char_sprites[16*dc.SPRITES_PER_ROW+16]
RIGHT_SIDE = dc.char_sprites[16*dc.SPRITES_PER_ROW+17]
TOP = dc.char_sprites[17*dc.SPRITES_PER_ROW+16]
BOTTOM = dc.char_sprites[17*dc.SPRITES_PER_ROW+17]


class Popup:
    def __init__(
        self,
        num_lines: int,
        line_width: int,
        side_margin: int,
        top_margin: int,
        does_input: bool = False,
        line_space: int = 1,  # the space between lines (0 or 1)
        show_name: bool = False,
    ):
        self.num_lines: int = num_lines
        self.line_width: int = line_width
        self.does_input: str = does_input
        self.input = ['']
        self.input_prompt = None
        self.line_space: int = line_space
        self.input_line = 0

        self.side_margin: int = side_margin
        self.top_margin: int = top_margin

        self.text: [str] = None
        self.box_num: int = 0
        self.x: int = None
        self.y: int = None
        self.w: int = None
        self.h: int = None
        self.speaker: dt.Tile = None
        self.show_name: bool = show_name

        self.box_width: int = self.side_margin*2 + self.line_width
        self.box_height: int = (
            self.top_margin*2 + self.num_lines*(self.line_space+1) -
            self.line_space
        )

        self.black_sheet = pygame.Surface((
            (self.box_width+2)*dc.TILE_WIDTH,
            (self.box_height+2)*dc.TILE_HEIGHT,
        ))
        pygame.transform.scale(
            dc.SURFACES[0],
            (
                (self.box_width+2)*dc.TILE_WIDTH,
                (self.box_height+2)*dc.TILE_HEIGHT,
            ),
            self.black_sheet,
        )

        self.is_set = False

    def set(
            self,
            input_prompt: str = None,
            text: [str] = None,
            pos: pygame.Rect = pygame.Rect(0, 0, 0, 0,),
            speaker: dt.Tile = None,
            show_name: bool = False,
    ):
        self.is_set = True
        self.text = text
        self.box_num = 0
        self.input = ['']
        self.x = pos.x
        self.y = pos.y
        self.w = pos.w
        self.h = pos.h
        self.speaker = speaker if speaker and speaker.name else None
        self.input_prompt = input_prompt
        self.input_line = 0
        self.show_name = show_name

        self.__parse_text()

    def next(self):
        """
        Returns True if there is still more text.
        """
        self.box_num += 1
        return self.box_num < len(self.text)

    def type(self, unicode: str):
        if not self.does_input:
            return

        if unicode == '\x09':
            self.input.append('')
            self.input_line += 1
        elif unicode == '\x7f' and self.input_line > 0:
            self.input.pop(-1)
            self.input_line -= 1
        elif unicode == '\x08':
            if len(self.input[self.input_line]) > 0:  # 3
                self.input[self.input_line] = self.input[self.input_line][:-1]
            elif self.input_line > 0:  # 2
                self.input.pop(-1)
                self.input_line -= 1
                self.input[self.input_line] = self.input[self.input_line][:-1]
        else:
            if len(self.input[self.input_line]) < self.line_width:  # 4
                self.input[self.input_line] += unicode
            else:  # 5
                self.input.append('')
                self.input_line += 1
                self.input[self.input_line] += unicode

        # print(self.input)

    # TODO? just make it store an array of strings not an array of arrays
    def __parse_text(self):
        parsed_text = []

        if self.text is None:
            return

        for phrase in self.text:
            box = []
            words = phrase.split(' ')
            line = ''
            space_left = self.line_width

            while len(words) > 0:
                word = words.pop(0)

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

    def __display_top(self, screen: pygame.Surface):
        screen.blit(TOP_LEFT, (
            self.x*dc.TILE_WIDTH,
            self.y*dc.TILE_HEIGHT,
        ))

        for ix in range(self.box_width):
            if (self.speaker and self.show_name and ix < len(self.speaker.name)):
                screen.blit(dc.get_text_sprite(self.speaker.name[ix]), (
                    (self.x+ix+1)*dc.TILE_WIDTH,  # +1 bc not top left
                    self.y*dc.TILE_HEIGHT,
                ))
                screen.blit(dc.SURFACES[self.speaker.fg], (
                    (self.x+ix+1)*dc.TILE_WIDTH,  # +1 bc not top left
                    self.y*dc.TILE_HEIGHT,
                ), special_flags=pygame.BLEND_RGB_MIN)
            else:
                screen.blit(TOP, (
                    (self.x+ix+1)*dc.TILE_WIDTH,  # +1 bc not top left
                    self.y*dc.TILE_HEIGHT,
                ))

        screen.blit(TOP_RIGHT, (
            (self.x+self.box_width+1)*dc.TILE_WIDTH,
            self.y*dc.TILE_HEIGHT,
        ))

    def __display_bottom(self, screen: pygame.Surface):
        screen.blit(BOTTOM_LEFT, (
            self.x*dc.TILE_WIDTH,
            (self.y+self.box_height+1)*dc.TILE_HEIGHT,
        ))

        for ix in range(self.box_width):
            if (self.text and self.box_num < len(self.text)-1 and
                    self.box_width-5 < ix < self.box_width-1):
                screen.blit(dc.get_text_sprite('.'), (
                    (self.x+ix+1)*dc.TILE_WIDTH,  # +1 bc not top left
                    (self.y+self.box_height+1)*dc.TILE_HEIGHT,
                ))
            else:
                screen.blit(BOTTOM, (
                    (self.x+ix+1)*dc.TILE_WIDTH,  # +1 bc not top left
                    (self.y+self.box_height+1)*dc.TILE_HEIGHT,
                ))

        screen.blit(BOTTOM_RIGHT, (
            (self.x+self.box_width+1)*dc.TILE_WIDTH,
            (self.y+self.box_height+1)*dc.TILE_HEIGHT,
        ))

    def __display_sides(self, screen: pygame.Surface):
        for iy in range(self.box_height):
            # left side
            screen.blit(LEFT_SIDE, (
                self.x*dc.TILE_WIDTH,
                (self.y+iy+1)*dc.TILE_HEIGHT,
            ))
            # right side
            screen.blit(RIGHT_SIDE, (
                (self.x+self.box_width+1)*dc.TILE_WIDTH,
                (self.y+iy+1)*dc.TILE_HEIGHT,
            ))

    def __display_text(self, screen: pygame.Surface):
        box = self.text[self.box_num]
        for iy, line in enumerate(box):
            for ix, char in enumerate(line):
                if char != ' ':
                    screen.blit(dc.get_text_sprite(char), (
                        (self.x+self.side_margin+ix+1)*dc.TILE_WIDTH,
                        (self.y+self.top_margin+1 +
                            iy*(self.line_space+1))*dc.TILE_HEIGHT)
                    )

    def __display_input(self, screen: pygame.Surface):
        assert self.num_lines >= 2  # needs 2 lines for input
        if self.input_prompt:
            for ix, char in enumerate(self.input_prompt):
                if char != ' ':
                    screen.blit(dc.get_text_sprite(char), (
                        (self.x+self.side_margin+ix+1)*dc.TILE_WIDTH,
                        (self.y+self.top_margin+1)*dc.TILE_HEIGHT)
                    )
        for iy, line in enumerate(self.input):
            ix = 0
            for char in line:
                if char != ' ':
                    screen.blit(dc.get_text_sprite(char), (
                        (self.x+self.side_margin+ix+1)*dc.TILE_WIDTH,
                        (self.y+self.top_margin+1 +
                            (iy+int(self.input_prompt is not None)) *
                            (self.line_space+1))*dc.TILE_HEIGHT)
                    )
                ix += 1
        if ix < self.line_width:
            screen.blit(dc.get_text_sprite('_'), (
                (self.x+self.side_margin+ix+1)*dc.TILE_WIDTH,
                (self.y+self.top_margin+1 +
                    (iy+int(self.input_prompt is not None)) *
                    (self.line_space+1))*dc.TILE_HEIGHT)
            )

    def display(self, screen: pygame.Surface):
        if not self.is_set:
            print('Error: popup not set')
            return

        screen.blit(self.black_sheet, (
            self.x*dc.TILE_WIDTH,
            self.y*dc.TILE_HEIGHT,
        ))

        self.__display_top(screen)
        self.__display_bottom(screen)
        self.__display_sides(screen)

        if self.does_input:
            self.__display_input(screen)
        else:
            self.__display_text(screen)
