import pygame, math
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
    def __init__(self, pos, type, group, surface=pygame.Surface((tile_size, tile_size))):
        super().__init__(group)
        self.image = surface
        self.rect = self.image.get_rect(topleft=pos)
        if type == 'bottom':
            self.hitbox = pygame.Rect(self.rect.x+3, self.rect.y+11, 10, 4)
        elif type == 'top':
            self.hitbox = pygame.Rect(self.rect.x+3, self.rect.y+1, 10, 4)
        elif type == 'right':
            self.hitbox = pygame.Rect(self.rect.x+1, self.rect.y+3, 4, 10)
        elif type == 'left':
            self.hitbox = pygame.Rect(self.rect.x+11, self.rect.y+3, 4, 10)

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
        self.collect_sound = pygame.mixer.Sound('audio/collect.wav')
        self.collect_sound.set_volume(0.6)

    def import_assets(self):
        self.animations = {
                'Apple' : [], 'Cherry': [], 'Melon': [], 'Pineapple': [], 'Strawberry':[]
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
    def __init__(self, pos, type, groups, blocktiles):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/Traps/Saw/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(self.rect.x+3, self.rect.y+3, 32, 32)
        self.pos = pygame.math.Vector2(self.hitbox.topleft)
        self.blocktiles = blocktiles
        self.type = type
        self.stop = False
        self.stop_time = None
        self.cooldown_time = 510
        self.state = 'Move'

        # Movement
        if self.type == 'H':
            self.direction = pygame.math.Vector2(1, 0)
        elif self.type == 'V':
            self.direction = pygame.math.Vector2(0, 1)
        elif self.type == 'C':
            self.direction = pygame.math.Vector2(1, 0)
        elif self.type == 'A':
            self.direction = pygame.math.Vector2(-1, 0)
        elif self.type == 'Z':
            self.direction = pygame.math.Vector2(0, 0)
        self.speed = 110

        # Animation
        self.frames = import_folder('graphics/Traps/Saw')
        self.frame_index = 0
        self.animation_speed = 18

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def horizontal(self):
        for sprite in self.blocktiles:
            if self.hitbox.colliderect(sprite.hitbox):
                self.stop = True
                self.stop_time = pygame.time.get_ticks()
                if self.direction.x > 0:
                    self.hitbox.right = sprite.hitbox.left
                    self.pos.x = self.hitbox.x
                    self.direction.x = -1
                elif self.direction.x < 0:
                    self.hitbox.left = sprite.hitbox.right
                    self.pos.x = self.hitbox.x
                    self.direction.x = 1

    def vertical(self):
        for sprite in self.blocktiles:
            if self.hitbox.colliderect(sprite.hitbox):
                self.stop = True
                self.stop_time = pygame.time.get_ticks()
                if self.direction.y > 0:
                    self.hitbox.bottom = sprite.hitbox.top
                    self.pos.y = self.hitbox.y
                    self.direction.y = -1
                elif self.direction.y < 0:
                    self.hitbox.top = sprite.hitbox.bottom
                    self.pos.y = self.hitbox.y
                    self.direction.y = 1

    def clock(self, change):
        for sprite in self.blocktiles:
            if self.hitbox.colliderect(sprite.hitbox):
                self.stop = True
                self.stop_time = pygame.time.get_ticks()
                if self.direction.x > 0:
                    self.hitbox.right = sprite.hitbox.left
                    self.pos.x = self.hitbox.x
                    self.direction.x = 0 * change
                    self.direction.y = 1 * change
                elif self.direction.y > 0:
                    self.hitbox.bottom = sprite.hitbox.top
                    self.pos.y = self.hitbox.y
                    self.direction.x = -1 * change
                    self.direction.y = 0 * change
                elif self.direction.x < 0:
                    self.hitbox.left = sprite.hitbox.right
                    self.pos.x = self.hitbox.x
                    self.direction.x = 0 * change
                    self.direction.y = -1 * change
                elif self.direction.y < 0:
                    self.hitbox.top = sprite.hitbox.bottom
                    self.pos.y = self.hitbox.y
                    self.direction.x = 1 * change
                    self.direction.y = 0 * change

    def move(self, dt):
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.x = round(self.pos.x)
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.y = round(self.pos.y)
        self.rect.x = self.hitbox.x - 3
        self.rect.y = self.hitbox.y - 3

    def cooldown(self):
        current = pygame.time.get_ticks()
        if self.stop == True:
            if current - self.stop_time >= self.cooldown_time:
                self.stop = False

    def check_type(self):
        if self.type == 'H':
            self.horizontal()
        elif self.type == 'V':
            self.vertical()
        elif self.type == 'C':
            self.clock(1)
        elif self.type == 'A':
            self.clock(-1)

    def update(self, dt):
        self.check_type()
        if self.stop == False:
            self.move(dt)
        self.animate(dt)
        self.cooldown()


class FallingPlatform(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('graphics/Traps/FallingPlatform/Off/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.Rect(self.rect.x+1, self.rect.y+4, 30, 1)
        self.landbox = pygame.Rect(self.rect.x+5, self.rect.y+2, 22, 1)
        self.old_hitbox = self.hitbox.copy()
        self.direction = pygame.math.Vector2(0, 0)
        self.pos = pygame.math.Vector2(self.hitbox.topleft)
        self.gravity = 6

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
        self.direction.y += self.gravity * dt
        if self.direction.y >= 6.3:
            self.direction.y = 6.3
        self.pos.y += self.direction.y
        self.hitbox.y = round(self.pos.y)
        self.rect.x = self.hitbox.x - 1
        self.rect.y = self.hitbox.y - 4

    def update(self, dt):
        self.old_hitbox = self.hitbox.copy()
        self.animate(dt)
        if self.status == 'Off':
            self.apply_gravity(dt)

class BouncePlatform(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(group)
        self.image = pygame.image.load('graphics/Traps/BouncePlatform/Idle/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.Rect(self.rect.x + 2, self.rect.y + 17, 23, 9)

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
        self.hitbox = pygame.Rect(self.rect.x + 5, self.rect.y + 5, 32, 32)
        self.pos = pygame.math.Vector2(self.hitbox.topleft)
        self.obstacle_sprites = obstacle_sprites
        self.type = type
        self.stop = False
        self.stop_time = None
        self.cooldown_time = 390
        self.state = 'Move'

        # Movement
        if self.type == 'H':
            self.direction = pygame.math.Vector2(1, 0)
        elif self.type == 'V':
            self.direction = pygame.math.Vector2(0, 1)
        elif self.type == 'C':
            self.direction = pygame.math.Vector2(1, 0)
        elif self.type == 'A':
            self.direction = pygame.math.Vector2(-1, 0)
        self.speed = 200

        # Animation
        self.import_assets()
        self.status = 'Idle'
        self.frame_index = 0
        self.animation_speed = 18

        # Audio
        self.hitsound = pygame.mixer.Sound('audio/headhit.wav')
        self.hitsound.set_volume(0.8)

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
                self.hitsound.play()
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
                self.hitsound.play()
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
                self.hitsound.play()
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
        self.rect.x = self.hitbox.x - 5
        self.rect.y = self.hitbox.y - 5

    def cooldown(self):
        current = pygame.time.get_ticks()
        if self.stop == True:
            if current - self.stop_time >= self.cooldown_time:
                self.stop = False

    def check_type(self):
        if self.type == 'H':
            self.horizontal()
        elif self.type == 'V':
            self.vertical()
        elif self.type == 'C':
            self.clock(1)
        elif self.type == 'A':
            self.clock(-1)

    def update(self, dt):
        self.old_hitbox = self.hitbox.copy()
        self.check_type()
        if self.stop == False:
            self.move(dt)
        self.animate(dt)
        self.cooldown()


class SpikeHead(pygame.sprite.Sprite):
    def __init__(self, pos, type, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/Traps/SpikeHead/Idle/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = pygame.Rect(self.rect.x + 7, self.rect.y + 6, 41, 41)
        self.pos = pygame.math.Vector2(self.hitbox.topleft)
        self.obstacle_sprites = obstacle_sprites
        self.type = type
        self.stop = False
        self.stop_time = None
        self.cooldown_time = 380
        self.state = 'Move'

        # Movement
        if self.type == 'H':
            self.direction = pygame.math.Vector2(1, 0)
        elif self.type == 'V':
            self.direction = pygame.math.Vector2(0, 1)
        elif self.type == 'C':
            self.direction = pygame.math.Vector2(1, 0)
        elif self.type == 'A':
            self.direction = pygame.math.Vector2(-1, 0)
        self.speed = 200

        # Animation
        self.import_assets()
        self.status = 'Idle'
        self.frame_index = 0
        self.animation_speed = 18

        # Audio
        self.hitsound = pygame.mixer.Sound('audio/headhit.wav')
        self.hitsound.set_volume(0.8)

    def import_assets(self):
        self.animations = {
            'Idle':[], 'RightHit':[], 'LeftHit':[], 'UpHit':[], 'DownHit':[]
        }
        path = 'graphics/Traps/SpikeHead'
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
                self.hitsound.play()
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
                self.hitsound.play()
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
                self.hitsound.play()
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
        self.rect.x = self.hitbox.x - 7
        self.rect.y = self.hitbox.y - 6

    def cooldown(self):
        current = pygame.time.get_ticks()
        if self.stop == True:
            if current - self.stop_time >= self.cooldown_time:
                self.stop = False

    def check_type(self):
        if self.type == 'H':
            self.horizontal()
        elif self.type == 'V':
            self.vertical()
        elif self.type == 'C':
            self.clock(1)
        elif self.type == 'A':
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


class FirePlatform(pygame.sprite.Sprite):
    def __init__(self, pos, groups, create_fire):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/Traps/Fire/Off/0.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = pygame.Rect(self.rect.x, self.rect.y+16, 16, 16)
        self.old_hitbox = self.hitbox.copy()
        self.landbox = pygame.Rect(self.rect.x+4, self.rect.y+14, 8, 4)
        self.create_fire = create_fire

        # Animatino
        self.import_assets()
        self.status = 'Off'
        self.frame_index = 0
        self.animation_speed = 12
        self.turn = 0

    def import_assets(self):
        self.animations = {
            'Off':[], 'On':[], 'Hit':[]
        }
        path = 'graphics/Traps/Fire'
        for animation in self.animations.keys():
            full_path = path + '/' + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        animations = self.animations[self.status]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(animations) and self.status == 'Off':
            self.frame_index = 0
        elif self.frame_index >= len(animations) and self.status == 'Hit':
            self.frame_index = 0
            self.status = 'On'
            self.create_fire(self.rect.topleft)
        elif self.frame_index >= len(animations) and self.status == 'On':
            self.frame_index = 0
            self.turn += 1
            if self.turn > 2:
                self.status = 'Off'
        self.image = animations[int(self.frame_index)]

    def update(self, dt):
        self.old_hitbox = self.hitbox.copy()
        if self.status == 'Off':
            self.turn = 0
        self.animate(dt)


class Fire(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((10, 13))
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect
        self.index = 0
        self.speed = 12
        self.fire_sound = pygame.mixer.Sound('audio/fire.wav')
        self.fire_sound.set_volume(0.6)
        self.fire_sound.play()

    def update(self, dt):
        self.index += self.speed * dt
        if self.index >= 7:
            self.kill()


class SpikeBall(pygame.sprite.Sprite):
    def __init__(self, center, radius, type, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/Traps/SpikeBall/spikeball.png').convert_alpha()
        self.type = type
        self.radius = radius
        self.center = pygame.math.Vector2(center, center)
        self.rect = self.image.get_rect(topleft=(self.radius, self.radius))
        self.hitbox = pygame.Rect(self.rect.x+5, self.rect.y+5, 17, 17)
        self.angle = 0

    def move(self, dt):
        self.hitbox.x = self.radius * math.cos(self.angle) + self.center.x
        self.hitbox.y = self.radius * math.sin(self.angle) + self.center.y
        if self.type == 'C':
            self.angle += 2 * dt
        elif self.type == 'A':
            self.angle -= 2 * dt
        self.rect.x = self.hitbox.x - 5
        self.rect.y = self.hitbox.y - 5

    def update(self, dt):
        self.move(dt)


class Chain(pygame.sprite.Sprite):
    def __init__(self, center, radius, type, groups):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/Traps/SpikeBall/Chain.png').convert_alpha()
        self.type = type
        self.radius = radius
        self.center = pygame.math.Vector2(center, center)
        self.rect = self.image.get_rect(topleft=(self.radius, self.radius))
        self.hitbox = self.rect
        self.angle = 0

    def move(self, dt):
        self.hitbox.x = self.radius * math.cos(self.angle) + self.center.x + 4
        self.hitbox.y = self.radius * math.sin(self.angle) + self.center.y + 4
        if self.type == 'C':
            self.angle += 2 * dt
        elif self.type == 'A':
            self.angle -= 2 * dt
        self.rect.topleft =self.hitbox.topleft

    def update(self, dt):
        self.move(dt)


class SpikeCenter(pygame.sprite.Sprite):
    def __init__(self, pos, radius, type, groups, create_ball, create_chain):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/Traps/SpikeBall/center.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox= self.rect
        self.old_hitbox = self.hitbox.copy()
        self.radius = radius
        self.type = type
        self.create_ball = create_ball
        self.create_chain = create_chain
        self.setup()

    def setup(self):
        radius = self.radius
        while radius > 0:
            radius -= 8
            self.create_chain(self.rect.topleft, radius, self.type)
        self.create_ball(self.rect.topleft, self.radius, self.type)
