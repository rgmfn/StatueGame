import pygame

import data.constants as dc
import data.popup as dp
import data.map as dm
import data.tile as dt

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

tile = dt.Tile(
    char='d',
    fg=dc.Color.RED,
    description='A cute red dog',
    # name='dog',
)

fg_prompt = 'Fg Color:'
bg_prompt = 'Bg Color:'
tile_prompt = 'Tile:'
save_prompt = 'Save map to:'
load_prompt = 'Load map from:'

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

map = dm.Map()
collision_view = False

tile_fg = dc.Color.WHITE
tile_bg = dc.Color.NONE
tile_char = '@'


def get_popup_value():
    global tile_fg
    global tile_bg
    global tile_char
    global map
    if popup.text == [[fg_prompt]]:
        popup.input = popup.input.upper()
        if popup.input in dc.color_names:
            tile_fg = dc.Color[popup.input]
    elif popup.text == [[bg_prompt]]:
        popup.input = popup.input.upper()
        if popup.input in dc.color_names:
            tile_bg = dc.Color[popup.input]
    elif popup.text == [[tile_prompt]]:
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
    elif popup.text == [[save_prompt]]:
        map.save(popup.input + '.json')
    elif popup.text == [[load_prompt]]:
        map.load(popup.input + '.json')


mouse_x, mouse_y = pygame.mouse.get_pos()

ctr = 0
run = True
while run:

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0] and not collision_view:
                map.set_by_mouse(
                    mouse_x, mouse_y, tile_char, tile_fg, tile_bg
                )
            elif event.buttons[2]:
                map.set_by_mouse(
                    mouse_x, mouse_y, char=' ',
                    fg=dc.Color.NONE, bg=dc.Color.NONE,
                )
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if collision_view:
                    map.flip_wall_mouse(mouse_x, mouse_y)
                else:
                    map.set_by_mouse(
                        mouse_x, mouse_y, tile_char, tile_fg, tile_bg
                    )
            elif event.button == 2:
                map.set_by_mouse(
                    mouse_x, mouse_y, char=' ',
                    fg=dc.Color.NONE, bg=dc.Color.NONE,
                )
            elif event.button == 3:
                tile = map.get_by_mouse(mouse_x, mouse_y)
                tile_fg = tile.fg
                tile_bg = tile.bg
                tile_char = tile.char

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
            elif event.key == pygame.K_f:
                popup = dialogue
                popup.set(text=[fg_prompt])
            elif event.key == pygame.K_b:
                popup = dialogue
                popup.set(text=[bg_prompt])
            elif event.key == pygame.K_t:
                popup = dialogue
                popup.set(text=[tile_prompt])
            elif event.key == pygame.K_s:
                popup = dialogue
                popup.set(text=[save_prompt])
            elif event.key == pygame.K_l:
                popup = dialogue
                popup.set(text=[load_prompt])
            elif event.key == pygame.K_v:
                collision_view = not collision_view
            elif event.key == pygame.K_a:
                print(tile_fg)
                print(tile_bg)
            elif event.key == pygame.K_d:
                print(map.width, map.height)
            elif event.key == pygame.K_m:
                print(map)

    screen.fill(dc.BLACK)

    map.draw(screen, collision_view)

    if not collision_view:
        screen.blit(dc.SURFACES[tile_bg], (
            ((mouse_x // dc.SCALE) // dc.TILE_WIDTH)*dc.TILE_WIDTH,
            ((mouse_y // dc.SCALE) // dc.TILE_HEIGHT)*dc.TILE_HEIGHT,
        ))
        copy = dc.char_sprites[ord(tile_char)]
        copy.blit(dc.SURFACES[tile_fg], (
            0, 0,
        ), special_flags=pygame.BLEND_RGB_MIN)
        screen.blit(copy, (
            ((mouse_x // dc.SCALE) // dc.TILE_WIDTH)*dc.TILE_WIDTH,
            ((mouse_y // dc.SCALE) // dc.TILE_HEIGHT)*dc.TILE_HEIGHT,
        ))

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
