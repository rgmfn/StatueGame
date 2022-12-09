import pygame

pygame.init()

SCALE = ?
# tile width, tile height
TW = ?
TH = ?

# window width, window height
WW = 400
WH = 400

display = pygame.display.set_mode((WW, WH))
pygame.display.set_caption('Sudoku')

mainClock = pygame.time.Clock()

test_img = pygame.image.load('assets/test.png').convert_alpha()

test_color = (255, 0, 0)
test_surf = pygame.Surface((20, 20))
test_surf.set_alpha(255)
test_surf.fill(test_color)

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

    display.blit(test_img, (0, 0))
    display.blit(test_surf, (0, 0), special_flags=pygame.BLEND_MIN)
    pygame.display.update()
    mainClock.tick(30)

pygame.quit()
