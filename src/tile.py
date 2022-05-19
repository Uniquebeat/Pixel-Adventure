from pickle import FALSE
import pygame
from src.setting import tile_size
from src.support import import_folder


class Basic_Tile(pygame.sprite.Sprite):
    def __init__(self, pos, group, surface=pygame.Surface((tile_size, tile_size))):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect

class OneWay_Tile(pygame.sprite.Sprite):
    def __init__(self, pos, group, surface):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, 16, 1)

class CollectableFruit(pygame.sprite.Sprite):
    def __init__(self, pos, group, type):
        super().__init__(group)
        self.image = pygame.image.load('graphics/fruits/'+type+'/a.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
        self.hitbox = self.rect.inflate(-11, -11)
        self.type = type

        # animation
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 18

    def import_assets(self):
        self.animations = {
                'Apple' : [], 'Cherry': []
        }
        path = 'graphics/fruits/'
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
        self.image = pygame.image.load('graphics/Traps/Saw/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(pos[0]-19, pos[1]-19))
        self.hitbox = self.rect.inflate(-1, -1)

        # animation
        self.frames = import_folder('graphics/Traps/Saw')
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
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('graphics/Traps/FallingPlatform/Off/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y, 16, 1)

        # animation
        self.import_assets()
        self.frame_index = 0
        self.animation_speed = 18
        self.status = 'On'

    def import_assets(self):
        self.animations = {
                'On' : [], 'Off': []
        }
        path = 'graphics/Traps/FallingPlatform/'
        for animation in self.animations.keys():
            full_path = path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        animations = self.animations[self.status]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(animations):
            self.frame_index = 0
        self.image = animations[int(self.frame_index)]

    def apply_gravity(self, dt):
        self.rect.y += 6 * dt

    def update(self, dt):
        self.animate(dt)


class BouncePlatform(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('graphics/Traps/BouncePlatform/Idle/0.png').convert_alpha()
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
        path = 'graphics/Traps/BouncePlatform'
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


class RockHead(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/Traps/RockHead/Idle/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect
        self.obstacle_sprites = obstacle_sprites
        self.pos = pygame.math.Vector2(self.hitbox.topleft)

        # Movement
        self.direction = pygame.math.Vector2(1, 0)
        self.speed = 180

        # Animation
        self.import_assets()
        self.status = 'Idle'
        self.frame_index = 0
        self.animation_speed = 16

    def import_assets(self):
        self.animations = {
            'Idle':[], 'RightHit':[], 'LeftHit':[]
        }
        path = 'graphics/Traps/Rockhead'
        for animation in self.animations.keys():
            fullpath = path + '/' + animation
            self.animations[animation] = import_folder(fullpath)


    def animate(self, dt):
        animations = self.animations[self.status]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(animations) and self.status == 'Idle':
            self.frame_index = 0
        elif self.frame_index >= len(animations) and self.status != 'Idle':
            self.status = 'Idle'
            self.frame_index = 3
        self.image = animations[int(self.frame_index)]

    def check_collide(self):
        for sprite in self.obstacle_sprites:
            if self.hitbox.colliderect(sprite.hitbox):
                if self.direction.x > 0:
                    self.status = 'RightHit'
                    self.hitbox.right = sprite.hitbox.left
                    self.pos.x = self.hitbox.x
                    self.direction.x = -1
                elif self.direction.x < 0:
                    self.status = 'LeftHit'
                    self.hitbox.left = sprite.hitbox.right
                    self.pos.x = self.hitbox.x
                    self.direction.x = 1

    def move(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.x = round(self.pos.x)
        self.rect.topleft = self.hitbox.topleft

    def update(self, dt):
        self.check_collide()
        self.move(dt)
        self.animate(dt)
