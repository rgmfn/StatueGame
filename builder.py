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

mouse_tile = dt.Tile(
    char='d',
    fg=dc.Color.RED,
    description='A cute red dog',
)

fg_prompt = 'Fg Color:'
bg_prompt = 'Bg Color:'
tile_prompt = 'Tile:'
save_prompt = 'Save map to:'
load_prompt = 'Load map from:'
name_prompt = 'Name:'

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
    line_width=15,
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

mouse_tile = dt.Tile(
    char='@',
    fg=dc.Color.WHITE,
    bg=dc.Color.NONE,
)


def get_popup_value(map, mouse_tile):
    if popup.input_prompt is None:
        # input = ''
        # for line in popup.input:
        #     input += line
        input = popup.input[0]
        for i in range(1, len(popup.input)):
            input += ' ' + popup.input[i].strip()
        mouse_tile.description = input
    elif popup.input_prompt == fg_prompt:
        input = popup.input[0].upper()
        if input in dc.color_names:
            mouse_tile.fg = dc.Color[input]
    elif popup.input_prompt == bg_prompt:
        input = popup.input[0].upper()
        if input in dc.color_names:
            mouse_tile.bg = dc.Color[input]
    elif popup.input_prompt == tile_prompt:
        input = popup.input[0]
        if input.find('num') >= 0:
            input = input.replace('num', '').strip()

            if not input.isnumeric():
                return
            if len(input) != 1:
                return

            mouse_tile.char = input
        elif input.isnumeric():
            mouse_tile.char = chr(int(input))
        elif len(input) == 1:
            mouse_tile.char = input
    elif popup.input_prompt == save_prompt:
        map.save(popup.input[0] + '.json')
    elif popup.input_prompt == load_prompt:
        map.load(popup.input[0] + '.json')
    elif popup.input_prompt == name_prompt:
        mouse_tile.name = popup.input[0]


mouse_x, mouse_y = pygame.mouse.get_pos()

run = True
while run:

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0] and not collision_view:
                map.set_by_mouse(
                    mouse_x, mouse_y, mouse_tile.copy(),
                )
            elif event.buttons[2]:
                map.set_by_mouse(
                    mouse_x, mouse_y, dt.Tile(),
                )
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if collision_view:
                    map.flip_wall_mouse(mouse_x, mouse_y)
                else:
                    map.set_by_mouse(
                        mouse_x, mouse_y, mouse_tile.copy(),
                    )
            elif event.button == 3:
                map.set_by_mouse(
                    mouse_x, mouse_y, dt.Tile(),
                )
            elif event.button == 2:
                mouse_tile = map.get_by_mouse(mouse_x, mouse_y).copy()

        if event.type == pygame.KEYDOWN:
            if popup and popup.does_input:
                if event.key == pygame.K_RETURN:
                    get_popup_value(map, mouse_tile)
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
                popup.set(input_prompt=fg_prompt)
            elif event.key == pygame.K_b:
                popup = dialogue
                popup.set(input_prompt=bg_prompt)
            elif event.key == pygame.K_t:
                popup = dialogue
                popup.set(input_prompt=tile_prompt)
            elif event.key == pygame.K_s:
                popup = dialogue
                popup.set(input_prompt=save_prompt)
            elif event.key == pygame.K_l:
                popup = dialogue
                popup.set(input_prompt=load_prompt)
            elif event.key == pygame.K_d:
                popup = dialogue
                popup.set(input_prompt=None)
            elif event.key == pygame.K_v:
                collision_view = not collision_view
            elif event.key == pygame.K_p:
                popup = test_popup
            elif event.key == pygame.K_n:
                popup = dialogue
                popup.set(input_prompt=name_prompt)
            elif event.key == pygame.K_a:
                print(mouse_tile.fg)
                print(mouse_tile.bg)

    screen.fill(dc.BLACK)

    map.draw(screen, collision_view)

    if not collision_view:
        screen.blit(dc.SURFACES[mouse_tile.bg], (
            ((mouse_x // dc.SCALE) // dc.TILE_WIDTH)*dc.TILE_WIDTH,
            ((mouse_y // dc.SCALE) // dc.TILE_HEIGHT)*dc.TILE_HEIGHT,
        ))
        copy = dc.char_sprites[ord(mouse_tile.char)].copy()
        copy.blit(dc.SURFACES[mouse_tile.fg], (
            0, 0,
        ), special_flags=pygame.BLEND_RGBA_MIN)
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

    pygame.display.update()
    mainClock.tick(30)

pygame.quit()
