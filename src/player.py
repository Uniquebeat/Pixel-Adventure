from pickle import TRUE
import pygame
from src.support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, tiles, oneway_tiles, rockhead_sprites, create_dead_effect):
        super().__init__(group)
        self.image = pygame.image.load('graphics/player/Idle/a.png').convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.hitbox = pygame.Rect(self.rect.x+8, self.rect.y+7, 17, 25)
        self.old_hitbox = self.hitbox.copy()
        self.tiles = tiles
        self.oneway_tiles = oneway_tiles
        self.rockhead_sprites = rockhead_sprites
        self.pressed = False
        self.alive = True

        # Movement
        self.pos = pygame.math.Vector2(self.hitbox.topleft)
        self.direction = pygame.math.Vector2()
        self.speed = 118
        self.gravity = 6
        self.jumpforce = -2.5
        self.current_x = 0
        self.friction = 1
        self.on_ground = False
        self.facing_right = True
        self.on_right = False
        self.on_left = False
        self.jumping = False
        self.wall_jumped = False
        self.double_jump = True

        # Animation
        self.frame_index = 0
        self.animation_speed = 18
        self.status = 'Idle'
        self.import_character_assets()

        # Effect
        self.create_dead_effect = create_dead_effect

        # Audio
        self.jump_sound = pygame.mixer.Sound('audio/jump.wav')
        self.jump_sound.set_volume(0.6)


    def import_character_assets(self):
        self.animations = {
                'Idle': [], 'Run': [], 'Jump': [], 'Fall': [], 'On_wall': [], 'DoubleJump': [], 'Hurt':[]
        }
        character_path = 'graphics/player/'
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def animate(self, dt):
        animation = self.animations[self.status]
        if self.alive == True:
            self.frame_index += self.animation_speed * dt
            
        if self.frame_index >= len(animation):
            self.frame_index = 0
        elif self.frame_index >= 6 and self.status == 'Hurt':
            self.create_dead_effect()
            self.alive = False

        image = animation[int(self.frame_index)]

        if self.facing_right:
            self.image = image
        else:
            flip_image = pygame.transform.flip(image, True, False)
            self.image = flip_image

    def get_status(self):
        if self.status != 'Hurt':
            if self.on_left or self.on_right:
                self.double_jump = True
                if not self.jumping:
                    self.status = 'On_wall'
                    self.direction.y = 0.14
                if self.jumping:
                    self.status = 'Jump'
            elif self.status == 'Hurt':
                self.direction = pygame.math.Vector2(0, 0)
            else:
                self.wall_jumped = False
                if self.direction.y > 1:
                     self.status = 'Fall'
                elif self.direction.y < 0 and self.double_jump == True:
                     self.status = 'Jump'
                elif self.direction.y < 0 and self.double_jump == False:
                     self.status = 'DoubleJump'
                else:
                    if self.direction.x == 0:
                        self.status = 'Idle'
                    elif self.direction.x != 0:
                        self.status = 'Run'

    def get_input(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
            if self.on_ground:
                    self.jump()
            if not self.pressed:
                self.jumping = True
                self.pressed = True
                if (self.on_right or self.on_left) and self.wall_jumped == False:
                    self.wall_jump()
                elif not self.on_ground and self.double_jump:
                    self.jump()
                    self.double_jump = False
        elif self.pressed:
            self.pressed = False
            self.jumping = False

    def static_collision(self, direction):
        if direction == 'horizontal':
            for tile in self.tiles:
                if tile.hitbox.colliderect(self.hitbox):
                    if self.hitbox.right >= tile.hitbox.left and self.old_hitbox.right <= tile.old_hitbox.left:
                        self.hitbox.right = tile.hitbox.left
                        self.pos.x = self.hitbox.x
                        self.on_right = True
                        self.current_x = self.hitbox.right
                    elif self.hitbox.left <= tile.hitbox.right and self.old_hitbox.left >= tile.old_hitbox.right:
                        self.hitbox.left = tile.hitbox.right
                        self.pos.x = self.hitbox.x
                        self.on_left = True
                        self.current_x = self.hitbox.left

            if self.on_left and (self.hitbox.left < self.current_x or self.direction.x >= 0):
                self.on_left = False
            elif self.on_right and (self.hitbox.right > self.current_x or self.direction.x <= 0):
                self.on_right = False

        if direction == 'vertical':
            for tile in self.tiles:
                if tile.hitbox.colliderect(self.hitbox):
                    if self.hitbox.bottom >= tile.hitbox.top and self.old_hitbox.bottom <= tile.old_hitbox.top:
                        self.hitbox.bottom = tile.hitbox.top
                        self.pos.y = self.hitbox.y
                        self.direction.y = 0
                        self.on_ground = True
                        self.double_jump = True
                    elif self.hitbox.top <= tile.hitbox.bottom and self.old_hitbox.top >= tile.old_hitbox.bottom:
                        self.hitbox.top = tile.hitbox.bottom
                        self.pos.y = self.hitbox.y
                        self.direction.y = 0

            if self.on_ground and self.direction.y < 0 or self.direction.y > 0.6:
                self.on_ground = False

    def oneway_collision(self):
        for sprite in self.oneway_tiles:
            diff = self.hitbox.y - sprite.hitbox.y
            if abs(diff) >= 20:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.direction.y = 0
                        self.pos.y = self.hitbox.y
                        self.on_ground = True
                        self.double_jump = True

    def rockhead_collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.rockhead_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.hitbox.right >= sprite.hitbox.left and self.old_hitbox.right <= sprite.old_hitbox.left:
                        self.hitbox.right = sprite.hitbox.left
                        self.pos.x = self.hitbox.x
                        self.on_right = True
                        self.current_x = self.hitbox.right
                    elif self.hitbox.left <= sprite.hitbox.right and self.old_hitbox.left >= sprite.old_hitbox.right:
                        self.hitbox.left = sprite.hitbox.right
                        self.pos.x = self.hitbox.x
                        self.on_left = True
                        self.current_x = self.hitbox.left

            if self.on_left and (self.hitbox.left < self.current_x or self.direction.x >= 0):
                self.on_left = False
            elif self.on_right and (self.hitbox.right > self.current_x or self.direction.x <= 0):
                self.on_right = False

        if direction == 'vertical':
            for sprite in self.rockhead_sprites.sprites():
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.hitbox.bottom >= sprite.hitbox.top and self.old_hitbox.bottom <= sprite.old_hitbox.top:
                        self.hitbox.bottom = sprite.hitbox.top
                        self.pos.y = self.hitbox.y
                        self.on_ground = True
                        self.double_jump = True
                        self.direction.y = 0
                    elif self.hitbox.top <= sprite.hitbox.bottom and self.old_hitbox.top >= sprite.old_hitbox.bottom:
                        self.hitbox.top = sprite.hitbox.bottom
                        self.pos.y = self.hitbox.y
                        self.direction.y = 0

            if self.on_ground and self.direction.y < 0 or self.direction.y > 0.6:
                self.on_ground = False

    def move(self, dt):
        if self.status != 'Hurt':
            self.pos.x += self.direction.x * self.speed * dt
            self.hitbox.x = round(self.pos.x)
            self.static_collision('horizontal')
            self.rockhead_collision('horizontal')
            self.apply_gravity(dt)
            self.static_collision('vertical')
            self.rockhead_collision('vertical')
            self.oneway_collision()
            self.rect.x = self.hitbox.x - 8
            self.rect.y = self.hitbox.y - 7

    def apply_gravity(self, dt):
        self.direction.y += self.gravity * dt
        if self.direction.y >= 6.3:
            self.direction.y = 6.3
        self.pos.y += self.direction.y
        self.hitbox.y = round(self.pos.y)

    def jump(self):
        self.direction.y = self.jumpforce
        if self.status != 'Hurt':
            self.jump_sound.play()

    def wall_jump(self):
        self.direction.x *= -8
        self.direction.y = self.jumpforce
        self.jump_sound.play()
        self.wall_jumped = True

    def inwall_damage(self):
        for sprite in self.tiles:
            if self.hitbox.colliderect(sprite.hitbox):
                self.status = 'Hurt'

    def update(self, dt):
        self.old_hitbox = self.hitbox.copy()
        self.get_input(dt)
        self.get_status()
        self.animate(dt)
        self.move(dt)
        self.inwall_damage()
