import pygame
from pytmx.util_pygame import load_pygame
from setting import *
from support import import_csv_layout
from tile import Basic_Tile, CollectableFruit, Saw, FallingPlatform, BouncePlatform, OneWay_Tile
from player import Player
from effect import Collect_effect, Player_effect
from background import Background
from debug import debug


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.game_state = 'Start'
        self.level_data = load_pygame('../levels/0.tmx')
        self.visible = False

        # set the sprite group
        self.background_sprite = pygame.sprite.GroupSingle()
        self.obstacle_sprites = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()
        self.collectable_sprites = pygame.sprite.Group()
        self.effect_sprites = pygame.sprite.Group()
        self.damageable_sprites = pygame.sprite.Group()
        self.bounce_platforms = pygame.sprite.Group()
        self.oneway_sprites = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.hitbox_sprites = pygame.sprite.Group()

        # setup level
        self.timer_index = 0
        self.timer_speed = 0.14
        self.setup_Enter()
        self.setup_layout()

    def get_hitbox_visible(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_v]:
            for sprite in self.hitbox_sprites:
                pygame.draw.rect(self.display_surface, 'red', sprite.hitbox, 1)

    def setup_Enter(self):
        Player_effect((64, 230), 'Enter', [self.effect_sprites, self.visible_sprites], self.create_player)

    def setup_layout(self):
        Background([self.background_sprite])
        for layer in self.level_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, surface in layer.tiles():
                    pos = (x*16, y*16)
                    if layer.name in ('StaticTiles'):
                        Basic_Tile(pos, [self.visible_sprites, self.obstacle_sprites, self.hitbox_sprites], surface)
                    if layer.name in ('OnewayTiles'):
                        OneWay_Tile(pos, [self.visible_sprites, self.oneway_sprites, self.hitbox_sprites], surface)
        
    def create_player(self):
        Player((64, 230), [self.player, self.hitbox_sprites], self.obstacle_sprites, self.oneway_sprites, self.create_dead_effect)

    def create_dead_effect(self):
        player = self.player.sprite
        Player_effect(player.rect.center, 'Dead', [self.effect_sprites, self.visible_sprites], self.create_player)

    def check_collect(self):
        player = self.player.sprite
        for sprite in self.collectable_sprites.sprites():
            if sprite.hitbox.colliderect(player.hitbox):
                Collect_effect(sprite.rect.topleft, [self.effect_sprites, self.visible_sprites])
                sprite.kill()

    def check_damage(self):
        player = self.player.sprite
        for sprite in self.damageable_sprites.sprites():
            if player.hitbox.colliderect(sprite.hitbox):
                player.status = 'Hurt'

    def check_bounce(self):
        player = self.player.sprite
        for sprite in self.bounce_platforms.sprites():
            if player.hitbox.colliderect(sprite.hitbox):
                sprite.status = 'Hit'
                player.direction.y = -3.5
                player.double_jump = True

    def check_game_stage(self):
        player = self.player.sprite
        if player.alive == False:
            self.game_state = 'End'

    def enter_timer(self):
        self.timer_index += self.timer_speed
        if self.timer_index >= 7:
            self.game_state = 'Running'

    def run(self, dt):

        # Background
        self.background_sprite.draw(self.display_surface)

        # UPDATE METHOD
        # Background
        self.background_sprite.update(dt)
        # Fruits
        self.collectable_sprites.update(dt)
        # Spike
        self.damageable_sprites.update(dt)
        # Effects
        self.effect_sprites.update()
        # BouncePlatforms
        self.bounce_platforms.update(dt)

        # DRAW METHOD
        self.visible_sprites.draw(self.display_surface)

        # Player
        if self.game_state == 'Running':
            self.player.update(dt)
            self.player.draw(self.display_surface)

        # Checks
        self.get_hitbox_visible()
        if self.game_state == 'Start':
            self.enter_timer()
        elif self.game_state == 'Running':
            self.check_collect()
            self.check_damage()
            self.check_bounce()
            self.check_game_stage()
            player = self.player.sprite
            debug('player_status', player.status, 26)

        debug('Level', self.level_data)
        debug('game_state', self.game_state, 18)
