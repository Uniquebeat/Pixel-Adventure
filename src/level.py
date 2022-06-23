
import pygame
from pytmx.util_pygame import load_pygame
from src.setting import *
from src.support import import_csv_layout
from src.objects import *
from src.player import Player
from src.effect import Collect_effect, Player_effect, Arrow_effect
from src.background import Background
from src.debug import debug
from src.game_data import *


class Level:
    def __init__(self, character, content, pos, next_lvl, create_overworld, recreate_level, create_next_level):
        self.display_surface = pygame.display.get_surface()
        self.character = character
        self.create_overworld = create_overworld
        self.recreate_level = recreate_level
        self.create_next_level = create_next_level
        self.pos = pos
        self.player_pos = None
        self.next_lvl = next_lvl
        self.game_state = 'Start'
        self.content = content
        self.level_data = load_pygame(self.content)
        self.visible = False
        self.pressed = False

        # set the sprite group
        self.background_sprite = pygame.sprite.GroupSingle()
        self.chain_sprites = pygame.sprite.Group()
        self.obstacle_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()
        self.entity_sprites = pygame.sprite.Group()
        self.collectable_sprites = pygame.sprite.Group()
        self.effect_sprites = pygame.sprite.Group()
        self.damageable_sprites = pygame.sprite.Group()
        self.saw_sprites = pygame.sprite.Group()
        self.bounce_platforms = pygame.sprite.Group()
        self.oneway_sprites = pygame.sprite.Group()
        self.rockhead_sprites = pygame.sprite.Group()
        self.spikehead_sprites = pygame.sprite.Group()
        self.arrow_sprites = pygame.sprite.Group()
        self.falling_sprites = pygame.sprite.Group()
        self.fire_sprites = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.hitbox_sprites = pygame.sprite.Group()
        self.spikeball_sprites = pygame.sprite.Group()
        
        # audio
        self.enter_sound = pygame.mixer.Sound('audio/enter.wav')
        self.enter_sound.set_volume(0.6)
        self.hurt_sound = pygame.mixer.Sound('audio/hurt.wav')
        self.hurt_sound.set_volume(0.6)
        self.dead_sound = pygame.mixer.Sound('audio/dead.wav')
        self.dead_sound.set_volume(0.6)
        self.bounce_sound = pygame.mixer.Sound('audio/bounce.wav')
        self.bounce_sound.set_volume(0.6)
        self.back_sound = pygame.mixer.Sound('audio/selected.wav')
        self.back_sound.set_volume(0.6)

        # setup level
        self.timer_index = 0
        self.timer_speed = 0.14
        self.setup_layout()
        self.setup_Enter()


    def get_hitbox_visible(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_v]:
            for sprite in self.hitbox_sprites:
                pygame.draw.rect(self.display_surface, 'red', sprite.hitbox, 1)
        elif keys[pygame.K_BACKSPACE]:
            if not self.pressed:
                self.pressed = True
                self.back_sound.play()
                self.create_overworld(self.pos, self.character)
        elif self.pressed:
            self.pressed = False

    def setup_Enter(self):
        self.enter_sound.play()
        Player_effect(self.player_pos, 'Enter', [self.effect_sprites], self.create_player)

    def setup_layout(self):
        Background([self.background_sprite])
        for layer in self.level_data.layers:
            if hasattr(layer, 'data'):
                for x, y, surface in layer.tiles():
                    pos = (x*16, y*16)

                    # TILES---------------------------------#
                    if layer.name in ('StaticTiles'):
                        Basic_Tile(pos, [self.visible_sprites, self.obstacle_sprites, self.hitbox_sprites], surface)
                    if layer.name in ('OnewayTiles'):
                        OneWay_Tile(pos, [self.visible_sprites, self.oneway_sprites, self.hitbox_sprites], surface)
                    if layer.name in ('BlockTiles'):
                        Basic_Tile(pos, [self.block_sprites])
                    if layer.name in ('Chain'):
                        Basic_Tile((pos[0], pos[1]), [self.chain_sprites], surface)

                    # Spikes
                    if layer.name in ('SpikeTilesBottom'):
                        Spike_Tile((pos[0], pos[1]), 'bottom', [self.visible_sprites, self.entity_sprites, self.damageable_sprites, self.hitbox_sprites], surface)
                    if layer.name in ('SpikeTilesTop'):
                        Spike_Tile((pos[0], pos[1]), 'top', [self.visible_sprites, self.entity_sprites, self.damageable_sprites, self.hitbox_sprites], surface)
                    if layer.name in ('SpikeTilesRight'):
                        Spike_Tile((pos[0], pos[1]), 'right', [self.visible_sprites, self.entity_sprites, self.damageable_sprites, self.hitbox_sprites], surface)
                    if layer.name in ('SpikeTilesLeft'):
                        Spike_Tile((pos[0], pos[1]), 'left', [self.visible_sprites, self.entity_sprites, self.damageable_sprites, self.hitbox_sprites], surface)
                    
        for obj in self.level_data.objects:
            if obj.name in ('Player'):
                self.player_pos = (obj.x+16, obj.y+16)
            if obj.name in ('Fruits'):
                CollectableFruit((obj.x, obj.y), [self.visible_sprites, self.entity_sprites, self.collectable_sprites, self.hitbox_sprites], obj.type)
            if obj.name in ('Traps'):
                if obj.type in ('Arrow'):
                    Arrow((obj.x, obj.y), [self.visible_sprites, self.entity_sprites, self.arrow_sprites, self.hitbox_sprites])
                if obj.type in ('Bounce'):
                    BouncePlatform((obj.x, obj.y), [self.visible_sprites, self.entity_sprites, self.bounce_platforms, self.hitbox_sprites])
                if obj.type in ('Falling'):
                    FallingPlatform((obj.x, obj.y), [self.visible_sprites, self.entity_sprites, self.falling_sprites, self.obstacle_sprites, self.hitbox_sprites])
                if obj.type in ('Fire'):
                    FirePlatform((obj.x, obj.y), [self.entity_sprites, self.fire_sprites, self.obstacle_sprites, self.hitbox_sprites], self.create_fire)
            if obj.name in ('RockHead'):
                RockHead((obj.x, obj.y), obj.type, [self.visible_sprites, self.rockhead_sprites, self.hitbox_sprites], self.obstacle_sprites)
            if obj.name in ('SpikeHead'):
                SpikeHead((obj.x, obj.y), obj.type, [self.visible_sprites, self.damageable_sprites, self.spikehead_sprites,self.hitbox_sprites], self.obstacle_sprites)
            if obj.name in ('Saw'):
                Saw((obj.x, obj.y), obj.type, [self.saw_sprites, self.damageable_sprites, self.hitbox_sprites], self.block_sprites)
            if obj.name in ('Center-C'):
                if obj.type == '64':
                    radius = 64
                elif obj.type == '48':
                    radius = 48
                elif obj.type == '32':
                    radius = 32
                SpikeCenter((obj.x, obj.y), radius, 'C', [self.visible_sprites, self.entity_sprites, self.obstacle_sprites], self.create_ball, self.create_chain)
            if obj.name in ('Center-A'):
                if obj.type == '64':
                    radius = 64
                elif obj.type == '48':
                    radius = 48
                elif obj.type == '32':
                    radius = 32
                SpikeCenter((obj.x, obj.y), radius, 'A', [self.visible_sprites, self.entity_sprites, self.obstacle_sprites], self.create_ball, self.create_chain)

    def create_player(self):
        Player(self.player_pos, self.character, [self.player, self.hitbox_sprites], self.obstacle_sprites, self.oneway_sprites, self.rockhead_sprites, self.create_dead_effect)

    def create_dead_effect(self):
        player = self.player.sprite
        self.dead_sound.play()
        Player_effect(player.rect.center, 'Dead', [self.effect_sprites], self.create_player)

    def create_fire(self, pos):
        Fire((pos[0]+3, pos[1]+3), [self.damageable_sprites, self.entity_sprites, self.hitbox_sprites])
    
    def create_chain(self, center, radius, type):
        Chain(center, radius, type, [self.spikeball_sprites])

    def create_ball(self, center, radius, type):
        SpikeBall(center, radius, type, [self.spikeball_sprites, self.damageable_sprites, self.hitbox_sprites])

    def check_collect(self):
        if self.collectable_sprites:
            player = self.player.sprite
            for sprite in self.collectable_sprites.sprites():
                if sprite.hitbox.colliderect(player.hitbox):
                    sprite.collect_sound.play()
                    Collect_effect(sprite.rect.topleft, [self.effect_sprites])
                    sprite.remove()
                    sprite.kill()

    def check_damage(self):
        if self.damageable_sprites:
            player = self.player.sprite
            for sprite in self.damageable_sprites.sprites():
                if player.hitbox.colliderect(sprite.hitbox):
                    player.status = 'Hurt'

    def check_bounce(self):
        if self.bounce_platforms:
            player = self.player.sprite
            for sprite in self.bounce_platforms.sprites():
                if player.hitbox.colliderect(sprite.hitbox):
                    sprite.status = 'Hit'
                    self.bounce_sound.play()
                    player.direction.y = -3.8
                    player.double_jump = True

    def check_arrow(self):
        if self.arrow_sprites:
            player = self.player.sprite
            for sprite in self.arrow_sprites.sprites():
                if player.hitbox.colliderect(sprite.hitbox):
                    self.enter_sound.play()
                    Arrow_effect(sprite.rect.topleft, [self.visible_sprites, self.effect_sprites])
                    player.direction.y = -3
                    player.double_jump = True
                    sprite.kill()

    def check_falling(self):
        if self.falling_sprites:
            player = self.player.sprite
            for sprite in self.falling_sprites.sprites():
                if player.hitbox.colliderect(sprite.landbox):
                    sprite.status = 'Off'
                    player.double_jump = True

    def check_fire(self):
        if self.fire_sprites:
            player = self.player.sprite
            for sprite in self.fire_sprites.sprites():
                if player.hitbox.colliderect(sprite.landbox) and sprite.status == 'Off':
                    sprite.status = 'Hit'

    def check_game_stage(self):
        player = self.player.sprite
        if player.alive == False:
            self.game_state = 'Dead'
        sprites = self.collectable_sprites.sprites()
        if len(sprites) == 0:
            self.game_state = 'Won'

    def enter_timer(self):
        self.timer_index += self.timer_speed
        if self.timer_index >= 7:
            self.game_state = 'Running'

    def dead_timer(self):
        self.timer_index += self.timer_speed
        if self.timer_index >= 23:
            self.display_surface.fill('black')
            self.game_state = 'Revive'

    def exit_timer(self):
        self.timer_index += self.timer_speed
        if self.timer_index >= 16:
            self.display_surface.fill('black')
            self.game_state = 'Next'

    def run(self, dt):

        # Background
        self.background_sprite.draw(self.display_surface)
        self.chain_sprites.draw(self.display_surface)

        # UPDATE METHOD
        # Background
        self.background_sprite.update(dt)
        # Effects
        self.effect_sprites.update()
        # Entity
        self.entity_sprites.update(dt)
        self.spikeball_sprites.update(dt)

        # DRAW METHOD
        self.saw_sprites.draw(self.display_surface)
        self.visible_sprites.draw(self.display_surface)

        # Player
        if self.game_state == 'Running' or self.game_state == 'Won':
            self.player.update(dt)
            self.player.draw(self.display_surface)

        # Fire
        self.fire_sprites.draw(self.display_surface)
        # Effect
        self.effect_sprites.draw(self.display_surface)
        # Spikeball
        self.spikeball_sprites.draw(self.display_surface)

        # Checks
        self.get_hitbox_visible()
        if self.game_state == 'Start':
            self.enter_timer()
        elif self.game_state == 'Running':
            self.check_collect()
            self.check_damage()
            self.check_bounce()
            self.check_arrow()
            self.check_falling()
            self.check_game_stage()
            self.check_fire()
            self.rockhead_sprites.update(dt)
            self.spikehead_sprites.update(dt)
            self.saw_sprites.update(dt)
            player = self.player.sprite
            debug('player_status', player.status, 26)
        elif self.game_state == 'Won':
            self.exit_timer()
        elif self.game_state == 'Dead':
            self.dead_timer()
        elif self.game_state == 'Revive':
            self.recreate_level(self.character, self.pos, self.content, self.next_lvl)
        elif self.game_state == 'Next':
            if self.next_lvl <= len(levels):
                level = levels[self.next_lvl-1]
                self.create_next_level(self.character, level['pos'], level['content'], level['next_lvl'])
            else:
                self.create_overworld(self.pos, self.character)

        debug('Level', self.level_data)
        debug('game_state', self.game_state, 18)
