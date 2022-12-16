import pygame

import data.constants as dc
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
pygame.display.set_caption('Statue Meditation')

mainClock = pygame.time.Clock()

player = {
    'x': 3,
    'y': 3,
    'sprite': dc.spritesheet.subsurface((
                dc.TILE_WIDTH,
                0,
                dc.TILE_WIDTH,
                dc.TILE_HEIGHT
            )),
    'color': dc.Color.GREEN
}


def move_player(event):
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

    if not map[player['y']+delta_y][player['x']+delta_x].is_wall:
        player['x'] += delta_x
        player['y'] += delta_y


UP_KEYS = [pygame.K_UP, pygame.K_i]
DOWN_KEYS = [pygame.K_DOWN, pygame.K_k]
LEFT_KEYS = [pygame.K_LEFT, pygame.K_j]
RIGHT_KEYS = [pygame.K_RIGHT, pygame.K_l]

map = dm.load_map('test.json')
# map = dm.empty_map(dc.TILES_WIDE, dc.TILES_TALL)
# dm.print_map(map)

# test_color = (255, 0, 0)
# test_surf = pygame.Surface((dc.TILE_WIDTH, dc.TILE_HEIGHT))
# test_surf.set_alpha(100)
# test_surf.fill(test_color)

run = True
while run:

    # keys = pygame.key.get_pressed()
    # needed if I need key combos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            else:
                move_player(event)

    screen.fill(dc.BLACK)

    dm.draw_map(screen, map)

    screen.blit(player['sprite'], (
        player['x']*dc.TILE_WIDTH,
        player['y']*dc.TILE_HEIGHT
    ))
    screen.blit(
        dc.SURFACES[player['color']],
        (player['x']*dc.TILE_WIDTH, player['y']*dc.TILE_HEIGHT),
        special_flags=pygame.BLEND_RGB_MIN
    )

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
