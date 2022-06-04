from operator import truediv
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
    def __init__(self, content, pos, next_lvl, create_overworld, recreate_level, create_next_level):
        self.display_surface = pygame.display.get_surface()
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
        self.sounded = False

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
        self.player = pygame.sprite.GroupSingle()
        self.hitbox_sprites = pygame.sprite.Group()
        
        # audio
        self.enter_sound = pygame.mixer.Sound('audio/enter.wav')
        self.enter_sound.set_volume(0.4)
        self.collect_sound = pygame.mixer.Sound('audio/collect.wav')
        self.collect_sound.set_volume(0.4)
        self.hurt_sound = pygame.mixer.Sound('audio/hurt.wav')
        self.hurt_sound.set_volume(0.4)
        self.dead_sound = pygame.mixer.Sound('audio/dead.wav')
        self.dead_sound.set_volume(0.4)
        self.bounce_sound = pygame.mixer.Sound('audio/bounce.wav')
        self.bounce_sound.set_volume(0.4)
        self.back_sound = pygame.mixer.Sound('audio/selected.wav')
        self.back_sound.set_volume(0.4)

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
            self.back_sound.play()
            self.create_overworld(self.pos)

    def setup_Enter(self):
        self.enter_sound.play()
        Player_effect(self.player_pos, 'Enter', [self.effect_sprites, self.visible_sprites], self.create_player)

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
                        Basic_Tile((pos[0]-8, pos[1]+8), [self.chain_sprites], surface)

                    # PLAYER--------------------------------#
                    if layer.name in ('Player'):
                        self.player_pos = pos

                    # OBJECTS-------------------------------#

                    # Spikes
                    if layer.name in ('SpikeTilesBottom'):
                        Spike_Tile((pos[0], pos[1]), 'bottom', [self.visible_sprites, self.entity_sprites, self.damageable_sprites, self.hitbox_sprites], surface)
                    if layer.name in ('SpikeTilesTop'):
                        Spike_Tile((pos[0], pos[1]), 'top', [self.visible_sprites, self.entity_sprites, self.damageable_sprites, self.hitbox_sprites], surface)
                    if layer.name in ('SpikeTilesRight'):
                        Spike_Tile((pos[0], pos[1]), 'right', [self.visible_sprites, self.entity_sprites, self.damageable_sprites, self.hitbox_sprites], surface)
                    if layer.name in ('SpikeTilesLeft'):
                        Spike_Tile((pos[0], pos[1]), 'left', [self.visible_sprites, self.entity_sprites, self.damageable_sprites, self.hitbox_sprites], surface)

                    # Arrow
                    if layer.name in ('ArrowTiles'):
                        Arrow(pos, [self.visible_sprites, self.entity_sprites, self.arrow_sprites, self.hitbox_sprites])
                    
                    # Bounce
                    if layer.name in ('BounceTiles'):
                        BouncePlatform((pos[0]-6, pos[1]-12), [self.visible_sprites, self.entity_sprites, self.bounce_platforms, self.hitbox_sprites])
                    
                    # Rockhead
                    if layer.name in ('RockHead-H'):
                        RockHead((pos[0]-5, pos[1]-21), 'Horizontal', [self.visible_sprites, self.rockhead_sprites, self.hitbox_sprites], self.obstacle_sprites)
                    if layer.name in ('RockHead-V'):
                        RockHead((pos[0]-5, pos[1]-21), 'Vertical', [self.visible_sprites, self.rockhead_sprites, self.hitbox_sprites], self.obstacle_sprites)
                    if layer.name in ('RockHead-C'):
                        RockHead((pos[0]-5, pos[1]-21), 'Clock', [self.visible_sprites, self.rockhead_sprites, self.hitbox_sprites], self.obstacle_sprites)
                    if layer.name in ('RockHead-A'):
                        RockHead((pos[0]-5, pos[1]-21), 'AntiClock', [self.visible_sprites, self.rockhead_sprites], self.obstacle_sprites)

                    # Spikehead
                    if layer.name in ('SpikeHead-H'):
                        SpikeHead((pos[0]-11, pos[1]-26), 'Horizontal', [self.visible_sprites, self.damageable_sprites, self.spikehead_sprites, self.hitbox_sprites], self.obstacle_sprites)
                    if layer.name in ('SpikeHead-V'):
                        SpikeHead((pos[0]-11, pos[1]-26), 'Vertical', [self.visible_sprites, self.damageable_sprites, self.spikehead_sprites, self.hitbox_sprites], self.obstacle_sprites)
                    if layer.name in ('SpikeHead-C'):
                        SpikeHead((pos[0]-11, pos[1]-26), 'Clock', [self.visible_sprites, self.damageable_sprites, self.spikehead_sprites, self.hitbox_sprites], self.obstacle_sprites)
                    if layer.name in ('SpikeHead-A'):
                        SpikeHead((pos[0]-11, pos[1]-26), 'AntiClock', [self.visible_sprites, self.damageable_sprites, self.spikehead_sprites, self.hitbox_sprites], self.obstacle_sprites)

                    # Saw
                    if layer.name in ('Saw-Zero'):
                        Saw((pos[0]-3, pos[1]-3), 'Zero', [self.saw_sprites, self.damageable_sprites, self.hitbox_sprites], self.block_sprites)
                    if layer.name in ('Saw-H'):
                        Saw((pos[0]-3, pos[1]-3), 'Horizontal', [self.saw_sprites, self.damageable_sprites, self.hitbox_sprites], self.block_sprites)
                    if layer.name in ('Saw-V'):
                        Saw((pos[0]-3, pos[1]-3), 'Vertical', [self.saw_sprites, self.damageable_sprites, self.hitbox_sprites], self.block_sprites)
                    if layer.name in ('Saw-Clock'):
                        Saw((pos[0]-3, pos[1]-3), 'Clock', [self.saw_sprites, self.damageable_sprites, self.hitbox_sprites], self.block_sprites)
                    if layer.name in ('Saw-AntiClock'):
                        Saw((pos[0]-3, pos[1]-3), 'AntiClock', [self.saw_sprites, self.damageable_sprites, self.hitbox_sprites], self.block_sprites)
                    
                    # FRUITS--------------------------------#
                    if layer.name in ('AppleTiles'):
                        CollectableFruit((pos[0], pos[1]-16), [self.visible_sprites, self.entity_sprites, self.collectable_sprites, self.hitbox_sprites], 'Apple')
                    if layer.name in ('CherryTiles'):
                        CollectableFruit((pos[0], pos[1]-16), [self.visible_sprites, self.entity_sprites, self.collectable_sprites, self.hitbox_sprites], 'Cherry')
                    if layer.name in ('MelonTiles'):
                        CollectableFruit((pos[0], pos[1]-16), [self.visible_sprites, self.entity_sprites, self.collectable_sprites, self.hitbox_sprites], 'Melon')
                    if layer.name in ('PineappleTiles'):
                        CollectableFruit((pos[0], pos[1]-16), [self.visible_sprites, self.entity_sprites, self.collectable_sprites, self.hitbox_sprites], 'Pineapple')
                    if layer.name in ('StrawberryTiles'):
                        CollectableFruit((pos[0], pos[1]-16), [self.visible_sprites, self.entity_sprites, self.collectable_sprites, self.hitbox_sprites], 'Strawberry')
        
    def create_player(self):
        Player(self.player_pos, [self.player, self.hitbox_sprites], self.obstacle_sprites, self.oneway_sprites, self.rockhead_sprites, self.create_dead_effect)

    def create_dead_effect(self):
        player = self.player.sprite
        self.dead_sound.play()
        Player_effect(player.rect.center, 'Dead', [self.effect_sprites, self.visible_sprites], self.create_player)

    def check_collect(self):
        player = self.player.sprite
        for sprite in self.collectable_sprites.sprites():
            if sprite.hitbox.colliderect(player.hitbox):
                self.collect_sound.play()
                Collect_effect(sprite.rect.topleft, [self.effect_sprites, self.visible_sprites])
                sprite.remove()
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
                self.bounce_sound.play()
                player.direction.y = -3.8
                player.double_jump = True

    def check_arrow(self):
        player = self.player.sprite
        for sprite in self.arrow_sprites.sprites():
            if player.hitbox.colliderect(sprite.hitbox):
                self.enter_sound.play()
                Arrow_effect(sprite.rect.topleft, [self.visible_sprites, self.effect_sprites])
                player.direction.y = -3
                player.double_jump = True
                sprite.kill()

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

        # DRAW METHOD
        self.saw_sprites.draw(self.display_surface)
        self.visible_sprites.draw(self.display_surface)

        # Player
        if self.game_state == 'Running' or self.game_state == 'Won':
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
            self.check_arrow()
            self.check_game_stage()
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
            self.recreate_level(self.pos, self.content, self.next_lvl)
        elif self.game_state == 'Next':
            if self.next_lvl <= len(levels):
                level = levels[self.next_lvl-1]
                self.create_next_level(level['pos'], level['content'], level['next_lvl'])
            else:
                self.create_overworld(self.pos)

        debug('Level', self.level_data)
        debug('game_state', self.game_state, 18)
