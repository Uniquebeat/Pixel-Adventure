import pygame


class Background(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        surface1 = pygame.image.load('../graphics/test/background.png').convert_alpha()
        surface2 = pygame.image.load('../graphics/test/background.png').convert_alpha()
        height = surface1.get_height()
        
        self.image = pygame.Surface((surface1.get_width(), surface1.get_height() * 2))
        self.image.blit(surface1, (0, 0))
        self.image.blit(surface2, (0, height))

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def move(self, dt):
        self.pos.y -= 20 * dt
        if self.rect.centery <= 0:
            self.pos.y = 0
        self.rect.y = round(self.pos.y)

    def update(self, dt):
        self.move(dt)