import pygame
from background import Background
from support import import_folder
from game_data import levels


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, content, groups, surface):
        super().__init__(groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.content = content


class Select(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('../graphics/Overworld/select.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.pressed = False

        # movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            if not self.pressed:
                self.pressed = True
                self.rect.x += 64
        elif keys[pygame.K_a]:
            if not self.pressed:
                self.pressed = True
                self.rect.x -= 64
        elif keys[pygame.K_w]:
            if not self.pressed:
                self.pressed = True
                self.rect.y -= 64
        elif keys[pygame.K_s]:
            if not self.pressed:
                self.pressed = True
                self.rect.y += 64
        elif self.pressed:
            self.pressed = False

    def reset(self):
        if self.rect.x < 144:
            self.rect.x = 464
        elif self.rect.x > 464:
            self.rect.x = 144
        elif self.rect.y < 32:
            self.rect.y = 288
        elif self.rect.y > 288:
            self.rect.y = 32

    def update(self):
        self.get_input()
        self.reset()


class Overworld:
    def __init__(self, create_level):
        self.display_surface = pygame.display.get_surface()
        self.create_level = create_level
        self.background_sprite = pygame.sprite.GroupSingle()
        self.node_sprites = pygame.sprite.Group()
        self.select_sprite = pygame.sprite.GroupSingle()
        self.setup()

    def setup(self):
        Background([self.background_sprite])
        Select((144, 32), [self.select_sprite])
        graphics = import_folder('../graphics/Overworld/levels')
        for node_data in levels.values():
            surface = graphics[node_data['number']]
            Node(node_data['pos'], node_data['content'], [self.node_sprites], surface)

    def input(self):
        keys = pygame.key.get_pressed()
        select = self.select_sprite.sprite
        for node in self.node_sprites.sprites():
            if keys[pygame.K_SPACE] and node.rect.colliderect(select.rect):
                self.create_level(node.content)

    def run(self, dt):
        self.input()
        self.background_sprite.update(dt)
        self.background_sprite.draw(self.display_surface)
        self.select_sprite.update()
        self.select_sprite.draw(self.display_surface)
        self.node_sprites.draw(self.display_surface)
