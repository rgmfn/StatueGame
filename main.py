import pygame

pygame.init()

SCALE = 4
TILE_WIDTH = 8
TILE_HEIGHT = 12

TILES_WIDE = 10
TILES_TALL = 10

SCREEN_WIDTH = TILE_WIDTH * TILES_WIDE
SCREEN_HEIGHT = TILE_HEIGHT * TILES_TALL

DISPLAY_WIDTH = SCREEN_WIDTH * SCALE
DISPLAY_HEIGHT = SCREEN_HEIGHT * SCALE

display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Statue Meditation')

mainClock = pygame.time.Clock()

spritesheet = pygame.image.load('assets/spritesheet.png')

# test_color = (255, 0, 0)
# test_surf = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
# test_surf.set_alpha(255)
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

    screen.blit(spritesheet, (0, 0))

    pygame.transform.scale(screen, (DISPLAY_WIDTH, DISPLAY_HEIGHT), display)

    pygame.display.update()
    mainClock.tick(30)

pygame.quit()
