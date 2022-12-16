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
    'x': 3 * dc.TILE_WIDTH,
    'y': 3 * dc.TILE_WIDTH,
    'sprite': dc.spritesheet.subsurface((
                dc.TILE_WIDTH,
                0,
                dc.TILE_WIDTH,
                dc.TILE_HEIGHT
            )),
    'color': dc.Color.GRN,
}

UP_KEYS = [pygame.K_UP, pygame.K_i]
DOWN_KEYS = [pygame.K_DOWN, pygame.K_k]
LEFT_KEYS = [pygame.K_LEFT, pygame.K_j]
RIGHT_KEYS = [pygame.K_RIGHT, pygame.K_l]

map = dm.load_map('map.txt')
# dm.print_map(map)

# test_color = (255, 0, 0)
# test_surf = pygame.Surface((dc.TILE_WIDTH, dc.TILE_HEIGHT))
# test_surf.set_alpha(100)
# test_surf.fill(test_color)

ctr = 0
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
            if event.key in UP_KEYS:
                player['y'] -= dc.TILE_HEIGHT
            elif event.key in DOWN_KEYS:
                player['y'] += dc.TILE_HEIGHT
            if event.key in LEFT_KEYS:
                player['x'] -= dc.TILE_WIDTH
            elif event.key in RIGHT_KEYS:
                player['x'] += dc.TILE_WIDTH

    screen.fill(dc.BLACK)

    dm.draw_map(screen, map)

    screen.blit(player['sprite'], (player['x'], player['y']))
    screen.blit(
        dc.SURFACES[dc.Color.GRN],
        (player['x'], player['y']),
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

    print(ctr)
    ctr += 1
    pygame.display.update()
    mainClock.tick(30)

pygame.quit()
