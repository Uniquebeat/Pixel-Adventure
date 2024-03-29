import pygame

pygame.init()

font = pygame.font.Font('graphics/font/slkscr.ttf', 9)


def debug(Text, info, y=10, x=0):
    text = str(Text)
    display_surface = pygame.display.get_surface()
    debug_surface = font.render(f'{text} : {str(info)}', True, 'white')
    debug_rect = debug_surface.get_rect(topleft=(x, y))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_x]:
        pygame.draw.rect(display_surface, 'black', debug_rect)
        display_surface.blit(debug_surface, debug_rect)
