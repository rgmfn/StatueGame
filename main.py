import pygame

import data.constants as dc
import data.popup as dp
import data.board as db

pygame.init()

display = pygame.display.set_mode((
    dc.DISPLAY_WIDTH,
    dc.DISPLAY_HEIGHT,
))
screen = pygame.Surface((
    dc.SCREEN_WIDTH,
    dc.SCREEN_HEIGHT,
))
pygame.display.set_caption('Statue Meditation')

mainClock = pygame.time.Clock()

player = {
    'x': 0,
    'y': 0,
    'sprite': dc.SURFACES[0].copy(),
}
_player_color = 5
_player_sprite = dc.char_sprites[13*dc.SPRITES_PER_ROW+1].copy()
# _player_sprite = dc.get_text_sprite('@').copy()
_player_sprite.blit(dc.SURFACES[_player_color], (
    0, 0
), special_flags=pygame.BLEND_RGB_MIN)
player['sprite'].blit(_player_sprite, (0, 0))

cursor = {
    'x': 0,
    'y': 0,
    'jump_x': 4,  # how many spaces to jump around by
    'jump_y': 3,  # how many spaces to jump around by
    'sprite': dc.char_sprites[3*dc.SPRITES_PER_ROW+21].copy(),
}


# TODO? make character/entity class for player and cursor
def display_cursor(screen, cursor):
    screen.blit(dc.SURFACES[0], (
        cursor['x']*dc.TILE_WIDTH,
        cursor['y']*dc.TILE_HEIGHT,
    ))
    copy = cursor['sprite'].copy()
    color = None
    if board.map[cursor['y']][cursor['x']].name:  # can speak to
        color = 2  # red
    elif board.map[cursor['y']][cursor['x']].description:  # description of
        color = 8  # orange
    else:  # normal cursor
        color = 7  # yellow

    copy.blit(dc.SURFACES[color], (
        0, 0,
    ), special_flags=pygame.BLEND_RGB_MIN)
    screen.blit(copy, (
        cursor['x']*dc.TILE_WIDTH,
        cursor['y']*dc.TILE_HEIGHT,
    ))


view_mode = False


def move_player(event):
    global popup
    delta_x = 0
    delta_y = 0
    if event.key in UP_KEYS:
        delta_y -= 1
    elif event.key in DOWN_KEYS:
        delta_y += 1
    elif event.key in LEFT_KEYS:
        delta_x -= 1
    elif event.key in RIGHT_KEYS:
        delta_x += 1
    else:
        return

    if event.mod == 1:  # shift
        while board.is_walkable(x=player['x']+delta_x, y=player['y']+delta_y):
            player['x'] += delta_x
            player['y'] += delta_y
    else:
        if board.is_walkable(x=player['x']+delta_x, y=player['y']+delta_y):
            player['x'] += delta_x
            player['y'] += delta_y
        elif board.is_talkable(x=player['x']+delta_x, y=player['y']+delta_y):
            tile = board.map[player['y']+delta_y][player['x']+delta_x]
            popup = dialogue
            popup.set(text=[tile.description], speaker=tile)


def move_cursor(event):
    global popup
    delta_x = 0
    delta_y = 0
    if event.key in UP_KEYS:
        delta_y -= 1
    elif event.key in DOWN_KEYS:
        delta_y += 1
    if event.key in LEFT_KEYS:
        delta_x -= 1
    elif event.key in RIGHT_KEYS:
        delta_x += 1
    elif event.key in ACTION_KEYS:
        tile = board.map[cursor['y']][cursor['x']]
        if tile.description is not None:
            popup = dialogue
            popup.set(text=[tile.description], speaker=tile)

    if event.mod == 1:  # shift
        delta_x *= cursor['jump_x']
        delta_y *= cursor['jump_y']

    cursor['x'] += delta_x
    cursor['y'] += delta_y


UP_KEYS = [pygame.K_UP, pygame.K_i]
DOWN_KEYS = [pygame.K_DOWN, pygame.K_k]
LEFT_KEYS = [pygame.K_LEFT, pygame.K_j]
RIGHT_KEYS = [pygame.K_RIGHT, pygame.K_l]
VIEW_KEYS = [pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_x]
ACTION_KEYS = [pygame.K_SPACE, pygame.K_RETURN]
QUIT_KEYS = [pygame.K_ESCAPE]

# TODO make map class with multiple boards
# TODO system for collisions
# TODO make event prototype
# TODO make event system
# TODO make cursor use bg below it (not yellow)
board = db.Board('tree')

# test_color = (255, 0, 0)
# test_surf = pygame.Surface((dc.TILE_WIDTH, dc.TILE_HEIGHT))
# test_surf.set_alpha(100)
# test_surf.fill(test_color)

dialogue: dp.Popup = dp.Popup(
    num_lines=2,
    line_width=15,
    side_margin=1,
    top_margin=1,
    line_space=1,
)
popup = None

run = True
while run:

    # keys = pygame.key.get_pressed()
    # needed if I need key combos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key in QUIT_KEYS and popup:
                popup = None
            elif event.key == pygame.K_ESCAPE:
                run = False
            elif event.key in VIEW_KEYS:
                view_mode = not view_mode
                if view_mode:
                    cursor['x'] = player['x']
                    cursor['y'] = player['y']
            elif (event.key in ACTION_KEYS and
                    popup and not popup.does_input):
                if not popup.next():
                    popup = None
            elif event.key == pygame.K_d:
                print(player['x'], player['y'])
            elif not popup and view_mode:
                move_cursor(event)
            elif not popup:
                move_player(event)

    screen.fill(dc.COLORS[0])

    board.draw(screen)

    screen.blit(player['sprite'], (
        player['x']*dc.TILE_WIDTH,
        player['y']*dc.TILE_HEIGHT
    ))

    if view_mode:
        display_cursor(screen, cursor)

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
