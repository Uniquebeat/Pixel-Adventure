import pygame
from setting import *
from support import import_csv_layout
from tile import Basic_Tile, CollectableFruit, Saw, FallingPlatform
from player import Player
from effect import Collect_effect, Player_effect
from debug import debug


class Level:
    def __init__(self, surface):
        self.display_surface = surface
        self.game_state = 'Start'
        self.level = 'test_room'

        # set the sprite group
        self.obstacle_sprites = pygame.sprite.Group()
        self.collectable_sprites = pygame.sprite.Group()
        self.effect_sprites = pygame.sprite.Group()
        self.damageable_sprites = pygame.sprite.Group()
        self.falling_sprites = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        # setup level
        self.timer_index = 0
        self.timer_speed = 0.28
        self.setup_Enter()
        self.setup_layout()
        self.background_surface = pygame.image.load(f'../levels/{self.level}/layout.png').convert_alpha()

    def setup_Enter(self):
        Player_effect((64, 230), 'Enter', [self.effect_sprites], self.create_player)

    def setup_layout(self):
        #FallingPlatform((230, 260), [self.falling_sprites, self.obstacle_sprites], self.player.sprite)
        layouts = {
            'obstacle_block': import_csv_layout(f'../levels/{self.level}/csv/{self.level}_StaticTiles.csv'),
            'CollectableFruit': import_csv_layout(f'../levels/{self.level}/csv/{self.level}_CollectableFruits.csv'),
            'DamageableSprites' : import_csv_layout(f'../levels/{self.level}/csv/{self.level}_DamageableSprites.csv'),
        }

        for style, layout in layouts.items():
            for row_index, row in enumerate(layout):
                for col_index, cell in enumerate(row):
                    if cell != '-1':
                        x = col_index * tile_size
                        y = row_index * tile_size
                        if style == 'obstacle_block':
                            Basic_Tile((x, y), [self.obstacle_sprites])
                        if style == 'CollectableFruit':
                            if cell == '0':
                                CollectableFruit((x, y), [self.collectable_sprites], 'Apple')
                            elif cell == '1':
                                CollectableFruit((x, y), [self.collectable_sprites], 'Cherry')
                        if style == 'DamageableSprites':
                            if cell == '0':
                                image = pygame.image.load('../graphics/Traps/spike.png')
                                Basic_Tile((x, y+9), [self.damageable_sprites], image)
                            if cell == '1':
                                Saw((x + 15, y), [self.damageable_sprites])

    def create_player(self):
        Player((64, 230), [self.player], self.obstacle_sprites, self.create_dead_effect)

    def create_dead_effect(self):
        player = self.player.sprite
        Player_effect(player.rect.center, 'Dead', [self.effect_sprites], self.create_player)

    def check_collect(self):
        player = self.player.sprite
        for sprite in self.collectable_sprites.sprites():
            if sprite.hitbox.colliderect(player.hitbox):
                Collect_effect(sprite.rect.topleft, [self.effect_sprites])
                sprite.kill()

    def check_damage(self):
        player = self.player.sprite
        for sprite in self.damageable_sprites.sprites():
            if player.hitbox.colliderect(sprite.hitbox):
                player.status = 'Hurt'

    def check_game_stage(self):
        player = self.player.sprite
        if player.alive == False:
            self.game_state = 'End'

    def enter_timer(self):
        self.timer_index += self.timer_speed
        if self.timer_index >= 14:
            self.game_state = 'Running'

    def run(self, dt):

        # Background
        self.display_surface.blit(self.background_surface, (0, 0))
        debug('Level', self.level, self.display_surface)
        debug('game_state', self.game_state, self.display_surface, 20)

        # Fruits
        self.collectable_sprites.update(dt)
        self.collectable_sprites.draw(self.display_surface)

        # Falling
        if self.game_state == 'Running':
            self.falling_sprites.update(dt)
            self.falling_sprites.draw(self.display_surface)

        # Player
        if self.game_state == 'Running':
            self.player.update(dt)
            self.player.draw(self.display_surface)

        # Spike
        self.damageable_sprites.update(dt)
        self.damageable_sprites.draw(self.display_surface)

        # Effects
        self.effect_sprites.update()
        self.effect_sprites.draw(self.display_surface)

        # Checks
        if self.game_state == 'Start':
            self.enter_timer()
        elif self.game_state == 'Running':
            self.check_collect()
            self.check_damage()
            self.check_game_stage()
            player = self.player.sprite
            debug('player_status', player.status, self.display_surface, 30)
