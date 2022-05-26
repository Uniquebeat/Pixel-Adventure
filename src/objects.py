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
        self.old_hitbox = self.hitbox.copy()

    def update(self, dt):
        self.old_hitbox = self.hitbox.copy()

class Spike_Tile(pygame.sprite.Sprite):
    def __init__(self, pos, group, surface=pygame.Surface((tile_size, tile_size))):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(-4, -2)

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
                'Apple' : [], 'Cherry': [], 'Melon': [], 'Pineapple': []
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
    def __init__(self, pos, type, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/Traps/RockHead/Idle/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.hitbox = pygame.Rect(self.pos.x + 5, self.pos.y + 5, 32, 32)
        self.obstacle_sprites = obstacle_sprites
        self.type = type
        self.stop = False
        self.stop_time = None
        self.cooldown_time = 390
        self.state = 'Move'

        # Movement
        if self.type == 'Horizontal':
            self.direction = pygame.math.Vector2(1, 0)
        elif self.type == 'Vertical':
            self.direction = pygame.math.Vector2(0, 1)
        elif self.type == 'Clock':
            self.direction = pygame.math.Vector2(1, 0)
        elif self.type == 'AntiClock':
            self.direction = pygame.math.Vector2(-1, 0)
        self.speed = 180

        # Animation
        self.import_assets()
        self.status = 'Idle'
        self.frame_index = 0
        self.animation_speed = 18

    def import_assets(self):
        self.animations = {
            'Idle':[], 'RightHit':[], 'LeftHit':[], 'UpHit':[], 'DownHit':[]
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

    def horizontal(self):
        for sprite in self.obstacle_sprites:
            if self.hitbox.colliderect(sprite.hitbox):
                self.stop = True
                self.stop_time = pygame.time.get_ticks()
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

    def vertical(self):
        for sprite in self.obstacle_sprites:
            if self.hitbox.colliderect(sprite.hitbox):
                self.stop = True
                self.stop_time = pygame.time.get_ticks()
                if self.direction.y > 0:
                    self.status = 'DownHit'
                    self.hitbox.bottom = sprite.hitbox.top
                    self.pos.y = self.hitbox.y
                    self.direction.y = -1
                elif self.direction.y < 0:
                    self.status = 'UpHit'
                    self.hitbox.top = sprite.hitbox.bottom
                    self.pos.y = self.hitbox.y
                    self.direction.y = 1

    def clock(self, change):
        for sprite in self.obstacle_sprites:
            if self.hitbox.colliderect(sprite.hitbox):
                self.stop = True
                self.stop_time = pygame.time.get_ticks()
                if self.direction.x > 0:
                    self.status = 'RightHit'
                    self.hitbox.right = sprite.hitbox.left
                    self.pos.x = self.hitbox.x
                    self.direction.x = 0 * change
                    self.direction.y = 1 * change
                elif self.direction.y > 0:
                    self.status = 'DownHit'
                    self.hitbox.bottom = sprite.hitbox.top
                    self.pos.y = self.hitbox.y
                    self.direction.x = -1 * change
                    self.direction.y = 0 * change
                elif self.direction.x < 0:
                    self.status = 'LeftHit'
                    self.hitbox.left = sprite.hitbox.right
                    self.pos.x = self.hitbox.x
                    self.direction.x = 0 * change
                    self.direction.y = -1 * change
                elif self.direction.y < 0:
                    self.status = 'UpHit'
                    self.hitbox.top = sprite.hitbox.bottom
                    self.pos.y = self.hitbox.y
                    self.direction.x = 1 * change
                    self.direction.y = 0 * change

    def move(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.x = round(self.pos.x)
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.y = round(self.pos.y)
        self.rect.center = self.hitbox.center

    def cooldown(self):
        current = pygame.time.get_ticks()
        if self.stop == True:
            if current - self.stop_time >= self.cooldown_time:
                self.stop = False

    def check_type(self):
        self.old_hitbox = self.hitbox.copy()
        if self.type == 'Horizontal':
            self.horizontal()
        elif self.type == 'Vertical':
            self.vertical()
        elif self.type == 'Clock':
            self.clock(1)
        elif self.type == 'AntiClock':
            self.clock(-1)

    def update(self, dt):
        self.old_hitbox = self.hitbox.copy()
        self.check_type()
        if self.stop == False:
            self.move(dt)
        self.animate(dt)
        self.cooldown()


class Arrow(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/Traps/Arrow/Idle/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = (pos[0]-2, pos[1]-2))
        self.hitbox = self.rect.inflate(-2, -2)

        # animation
        self.frames = import_folder('graphics/Traps/Arrow/Idle')
        self.frame_index = 0
        self.animation_speed = 14

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)
