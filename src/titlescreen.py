import pygame, json
from src.overworld import Select, Node
from src.objects import Basic_Tile
from src.background import Background
from src.game_data import level_1, character


class Titlescreen:
    def __init__(self, pos, create_level, create_overworld, create_helpscreen, create_infoscreen, create_skinscreen):
        self.display_surface = pygame.display.get_surface()
        self.pos = pos
        self.title_img = pygame.image.load('graphics/Titlescreen/title.png').convert_alpha()
        self.create_level = create_level
        self.create_overworld = create_overworld
        self.create_helpscreen = create_helpscreen
        self.create_infoscreen = create_infoscreen
        self.create_skinscreen = create_skinscreen
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
        self.character_index = {'index': 0}
        try:
            with open('graphics/player/character_index.txt') as data:
                self.character_index = json.load(data)
        except:
            with open('graphics/player/character_index.txt', 'w') as data:
                json.dump(self.character_index, data)
        self.character = character[self.character_index['index']]

        # audio
        self.selected_sound = pygame.mixer.Sound('audio/selected.wav')
        self.selected_sound.set_volume(0.6)

    def load(self):
        Background(self.background_sprite)
        Select(self.pos, [self.visible_sprites, self.select_sprite], pygame.image.load('graphics/Titlescreen/select.png').convert_alpha(), 'Titlescreen')
        Basic_Tile((299, 112), [self.visible_sprites, self.play_sprite], pygame.image.load('graphics/Titlescreen/play.png').convert_alpha())
        Basic_Tile((299, 176), [self.visible_sprites, self.level_sprite], pygame.image.load('graphics/Titlescreen/level.png').convert_alpha())
        Basic_Tile((299, 240), [self.visible_sprites, self.help_sprite], pygame.image.load('graphics/Titlescreen/help.png').convert_alpha())
        Basic_Tile((299, 304), [self.visible_sprites, self.info_sprite], pygame.image.load('graphics/Titlescreen/info.png').convert_alpha())

    def input(self):
        keys = pygame.key.get_pressed()
        select = self.select_sprite.sprite
        play = self.play_sprite.sprite
        level = self.level_sprite.sprite
        help = self.help_sprite.sprite
        info = self.info_sprite.sprite
        if keys[pygame.K_SPACE]:
            if select.rect.colliderect(play.rect):
                self.selected_sound.play()
                node = Node(level_1['pos'], level_1['content'], level_1['next_lvl'], self.node_sprite)
                self.create_level(node, self.character)
            elif select.rect.colliderect(level):
                self.selected_sound.play()
                self.create_overworld((144, 32), self.character)
            elif select.rect.colliderect(help):
                self.selected_sound.play()
                self.create_helpscreen()
            elif select.rect.colliderect(info):
                self.selected_sound.play()
                self.create_infoscreen()
        elif keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            self.selected_sound.play()
            self.create_skinscreen(self.character_index['index'])

    def run(self, dt):
        self.input()
        self.background_sprite.update(dt)
        self.background_sprite.draw(self.display_surface)
        self.display_surface.blit(self.title_img, (88, 64))
        self.select_sprite.update()
        self.visible_sprites.draw(self.display_surface)
