import pygame
from src.support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, tiles, oneway_tiles, create_dead_effect):
        super().__init__(group)
        self.image = pygame.image.load('graphics/player/Idle/a.png').convert_alpha()
        self.rect = self.image.get_rect(center=(pos[0]-3, pos[1]-7))
        self.hitbox = self.rect.inflate(-15, 0)
        self.tiles = tiles
        self.oneway_tiles = oneway_tiles
        self.pressed = False
        self.alive = True

        # Movement
        self.pos = pygame.math.Vector2(self.rect.center)
        self.direction = pygame.math.Vector2()
        self.speed = 86
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

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            if self.on_ground:
                    self.jump()
                    self.jump_sound.play()
            if not self.pressed:
                self.jumping = True
                self.pressed = True
                if (self.on_right or self.on_left) and self.wall_jumped == False:
                    self.wall_jump()
                    self.jump_sound.play()
                elif not self.on_ground and self.double_jump:
                    self.jump()
                    self.jump_sound.play()
                    self.double_jump = False
        elif self.pressed:
            self.pressed = False
            self.jumping = False

    def static_collision(self, direction):
        if direction == 'horizontal':
            for tile in self.tiles:
                if tile.rect.colliderect(self.hitbox):
                    if self.direction.x > -1:
                        self.hitbox.right = tile.rect.left
                        self.pos.x = self.hitbox.x
                        self.on_right = True
                        self.current_x = self.hitbox.right
                    elif self.direction.x < 1:
                        self.hitbox.left = tile.rect.right
                        self.pos.x =self.hitbox.x
                        self.on_left = True
                        self.current_x = self.hitbox.left
            if self.on_left and (self.hitbox.left < self.current_x or self.direction.x >= 0):
                self.on_left = False
            elif self.on_right and (self.hitbox.right > self.current_x or self.direction.x <= 0):
                self.on_right = False
        if direction == 'vertical':
            for tile in self.tiles:
                if tile.rect.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = tile.rect.top
                        self.direction.y = 0
                        self.pos.y = self.hitbox.y
                        self.on_ground = True
                        self.double_jump = True
                    elif self.direction.y < 0:
                        self.hitbox.top = tile.rect.bottom
                        self.pos.y = self.hitbox.y
                        self.direction.y = 0
            if self.on_ground and self.direction.y < 0 or self.direction.y > 0.6:
                self.on_ground = False

    def oneway_collision_test(self):
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

    def move(self, dt):
        if self.status != 'Hurt':
            self.pos.x += self.direction.x * self.speed * dt
            self.hitbox.x = round(self.pos.x)
            self.static_collision('horizontal')
            self.apply_gravity(dt)
            self.static_collision('vertical')
            self.oneway_collision_test()
        self.rect.center = self.hitbox.center

    def apply_gravity(self, dt):
        self.direction.y += self.gravity * dt
        if self.direction.y >= 7:
            self.direction.y = 7
        self.pos.y += self.direction.y
        self.hitbox.y = round(self.pos.y)

    def jump(self):
        self.direction.y = self.jumpforce

    def wall_jump(self):
        self.direction.x *= -8
        self.direction.y = self.jumpforce
        self.wall_jumped = True

    def update(self, dt):
        self.get_input(dt)
        self.get_status()
        self.animate(dt)
        self.move(dt)
