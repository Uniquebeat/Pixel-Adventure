from re import L
import pygame
from src.overworld import Select, Node
from src.objects import Basic_Tile
from src.background import Background
from src.game_data import level_1


class Titlescreen:
    def __init__(self, create_level, create_overworld):
        self.display_surface = pygame.display.get_surface()
        self.title_img = pygame.image.load('graphics/Titlescreen/title.png').convert_alpha()
        self.create_level = create_level
        self.create_overworld = create_overworld
        #sprites
        self.play_sprite = pygame.sprite.GroupSingle()
        self.level_sprite = pygame.sprite.GroupSingle()
        self.help_sprite = pygame.sprite.GroupSingle()
        self.info_sprite = pygame.sprite.GroupSingle()
        self.visible_sprites = pygame.sprite.Group()
        self.background_sprite = pygame.sprite.GroupSingle()
        self.select_sprite = pygame.sprite.GroupSingle()
        self.node_sprite = pygame.sprite.GroupSingle()
        self.load()

        # audio
        self.selected_sound = pygame.mixer.Sound('audio/selected.wav')
        self.selected_sound.set_volume(0.6)

    def load(self):
        Background([self.background_sprite])
        Select((299, 112), [self.visible_sprites, self.select_sprite], pygame.image.load('graphics/Titlescreen/select.png').convert_alpha(), 'Titlescreen')
        Basic_Tile((299, 112), [self.visible_sprites, self.play_sprite], pygame.image.load('graphics/Titlescreen/play.png').convert_alpha())
        Basic_Tile((299, 176), [self.visible_sprites, self.level_sprite], pygame.image.load('graphics/Titlescreen/level.png').convert_alpha())
        Basic_Tile((299, 240), [self.visible_sprites, self.help_sprite], pygame.image.load('graphics/Titlescreen/help.png').convert_alpha())
        Basic_Tile((299, 304), [self.visible_sprites, self.info_sprite], pygame.image.load('graphics/Titlescreen/info.png').convert_alpha())

    def input(self):
        keys = pygame.key.get_pressed()
        select = self.select_sprite.sprite
        play = self.play_sprite.sprite
        level = self.level_sprite.sprite
        if keys[pygame.K_SPACE]:
            if select.rect.colliderect(play.rect):
                self.selected_sound.play()
                node = Node(level_1['pos'], level_1['content'], level_1['next_lvl'], self.node_sprite)
                self.create_level(node)
            elif select.rect.colliderect(level):
                self.selected_sound.play()
                self.create_overworld((144, 32))

    def run(self, dt):
        self.input()
        self.background_sprite.update(dt)
        self.background_sprite.draw(self.display_surface)
        self.display_surface.blit(self.title_img, (88, 64))
        self.select_sprite.update()
        self.visible_sprites.draw(self.display_surface)
