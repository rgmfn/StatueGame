import pygame

import data.constants as dc
import data.popup as dp
import data.map as dm

pygame.init()

display = pygame.display.set_mode((
    dc.DISPLAY_WIDTH,
    dc.DISPLAY_HEIGHT,
))
screen = pygame.Surface((
    dc.SCREEN_WIDTH,
    dc.SCREEN_HEIGHT,
))
pygame.display.set_caption('Level Builder')

mainClock = pygame.time.Clock()

tile = dm.Tile(
    char='d',
    color=dc.Color.RED,
    description='A cute red dog',
    # name='dog',
)

color_prompt = 'Color:'
tile_prompt = 'Tile:'

dialogue: dp.Popup = dp.Popup(
    num_lines=2,
    line_width=15,
    side_margin=1,
    top_margin=1,
    line_space=1,
    does_input=True,
)

test_popup: dp.Popup = dp.Popup(
    num_lines=3,
    line_width=20,
    side_margin=1,
    top_margin=1,
    line_space=1,
)
test_popup.set(
    text=[
        'Woof woof!',
        'Textboxes are a good way to convey info.',
        'They are also very hard to program.',
    ],
    pos=pygame.Rect(0, 0, 0, 0),
    # speaker=tile,
)

popup = None

map = dm.load_map('map.txt')

tile_color = dc.Color.RED
tile_char = '@'


def get_popup_value():
    global tile_color
    global tile_char
    if popup.text == [[color_prompt]]:
        popup.input = popup.input.upper()
        if popup.input in dc.color_names:
            tile_color = dc.Color[popup.input]
    if popup.text == [[tile_prompt]]:
        if popup.input.find('num') >= 0:
            popup.input = popup.input.replace('num', '').strip()

            if not popup.input.isnumeric():
                return
            if len(popup.input) != 1:
                return

            tile_char = popup.input
        elif popup.input.isnumeric():
            tile_char = chr(int(popup.input))
        elif len(popup.input) == 1:
            tile_char = popup.input


mouse_x, mouse_y = pygame.mouse.get_pos()

ctr = 0
run = True
# TODO split keyboard and mouse input into separate methods
while run:

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            map[
                ((mouse_y // dc.SCALE) // dc.TILE_HEIGHT)
            ][
                ((mouse_x // dc.SCALE) // dc.TILE_WIDTH)
            ].set(tile_char, tile_color)

        if event.type == pygame.KEYDOWN:
            if popup and popup.does_input:
                if event.key == pygame.K_RETURN:
                    get_popup_value()
                    popup = None
                elif event.key == pygame.K_ESCAPE:
                    popup = None
                else:
                    popup.type(event.unicode)
            elif event.key == pygame.K_ESCAPE:
                run = False
            elif (popup and not popup.does_input and
                    event.key == pygame.K_SPACE):
                if not popup.next():
                    popup = None
            elif event.key == pygame.K_c:
                popup = dialogue
                popup.set(text=[color_prompt])
            elif event.key == pygame.K_t:
                popup = dialogue
                popup.set(text=[tile_prompt])
            elif event.key == pygame.K_a:
                print(tile_color)
                print(tile_char)

    screen.fill(dc.BLACK)

    dm.draw_map(screen, map)

    screen.blit(dp.char_sprites[tile_char], (
        ((mouse_x // dc.SCALE) // dc.TILE_WIDTH)*dc.TILE_WIDTH,
        ((mouse_y // dc.SCALE) // dc.TILE_HEIGHT)*dc.TILE_HEIGHT,
    ))
    screen.blit(dc.SURFACES[tile_color], (
        ((mouse_x // dc.SCALE) // dc.TILE_WIDTH)*dc.TILE_WIDTH,
        ((mouse_y // dc.SCALE) // dc.TILE_HEIGHT)*dc.TILE_HEIGHT,
    ), special_flags=pygame.BLEND_RGB_MIN)

    if popup:
        popup.display(screen)

    pygame.transform.scale(
        screen,
        (
            dc.DISPLAY_WIDTH,
            dc.DISPLAY_HEIGHT,
        ),
        display,
    )

    # print(ctr)
    # ctr += 1
    pygame.display.update()
    mainClock.tick(30)

pygame.quit()
