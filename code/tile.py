import pygame
from setting import tile_size
from support import import_folder


class Basic_Tile(pygame.sprite.Sprite):
    def __init__(self, pos, group, surface=pygame.Surface((tile_size, tile_size))):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

class OneWay_Tile(pygame.sprite.Sprite):
    def __init__(self, pos, group, surface=pygame.Surface((16, 1))):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, 16, 1)

class CollectableFruit(pygame.sprite.Sprite):
    def __init__(self, pos, group, type):
        super().__init__(group)
        self.image = pygame.image.load('../graphics/fruits/'+type+'/a.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-16))
        self.hitbox = self.rect.inflate(-9, -9)
        self.type = type

        # animation
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 18

    def import_assets(self):
        self.animations = {
                'Apple' : [], 'Cherry': []
        }
        path = '../graphics/fruits/'
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        animations = self.animations[self.type]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(animations):
            self.frame_index = 0
        self.image = animations[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class Saw(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('../graphics/Traps/Saw/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos[0]-19, pos[1]-19))
        self.hitbox = self.rect.inflate(-1, -1)

        # animation
        self.frames = import_folder('../graphics/Traps/Saw')
        self.frame_index = 0
        self.animation_speed = 18

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class FallingPlatform(pygame.sprite.Sprite):
    def __init__(self, pos, group, player):
        super().__init__(group)
        self.image = pygame.image.load('../graphics/Traps/FallingPlatform/Off/0.png').convert_alpha()
        self.player = player
        self.rect = self.image.get_rect(topleft=pos)
        self.grounded = False

        # animation
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 18
        self.status = 'On'

    def import_assets(self):
        self.animations = {
                'On' : [], 'Off': []
        }
        path = '../graphics/Traps/FallingPlatform/'
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        animations = self.animations[self.status]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(animations):
            self.frame_index = 0
        self.image = animations[int(self.frame_index)]

    def apply_gravity(self):
        self.rect.y += 3

    def check(self):
        if self.grounded == True:
            self.apply_gravity()

    def update(self, dt):
        self.animate(dt)
        self.check()


class BouncePlatform(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('../graphics/Traps/BouncePlatform/Idle/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-2, -18)

        # animations 
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 18
        self.status = 'Idle'

    def import_assets(self):
        self.animations = {
                'Idle' : [], 'Hit' : []
                }
        path = '../graphics/Traps/BouncePlatform'
        for animation in self.animations.keys():
            fullpath = path + '/' + animation
            self.animations[animation] = import_folder(fullpath)

    def animate(self, dt):
        animations = self.animations[self.status]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(animations) and self.status == 'Idle':
            self.frame_index = 0
        elif self.frame_index >= len(animations) and self.status == 'Hit':
            self.frame_index = 0
            self.status = 'Idle'
        self.image = animations[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)
