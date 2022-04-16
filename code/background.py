from email.mime import image
import pygame
from random import choice
from support import import_folder


class Background(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        images = import_folder('../graphics/Background')
        image = choice(images)
        surface1 = image
        surface2 = image
        height = surface1.get_height()
        
        self.image = pygame.Surface((surface1.get_width(), surface1.get_height() * 2))
        self.image.blit(surface1, (0, 0))
        self.image.blit(surface2, (0, height))

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def move(self, dt):
        self.pos.y -= 13 * dt
        if self.rect.centery <= 0:
            self.pos.y = 0
        self.rect.y = round(self.pos.y)

    def update(self, dt):
        self.move(dt)