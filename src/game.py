import pygame, sys, time, json
from src.setting import *
from src.level import Level
from src.overworld import Overworld
from src.titlescreen import Titlescreen
from src.helpscreen import Helpscreen
from src.infoscreen import Infoscreen
from src.skinscreen import Skinscreen
from src.debug import debug
from src.game_data import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(32)
        self.screen = pygame.display.set_mode((scaled_width, scaled_height), pygame.SCALED)
        pygame.display.set_caption('Pixel_Adventure_1')
        pygame.display.set_icon(pygame.image.load('icon.png').convert_alpha())
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()
        self.titlescreen = Titlescreen((299,112) ,self.create_level, self.create_overworld, self.create_helpscreen, self.create_infoscreen, self.create_skinscreen)
        self.status = 'Titlescreen'

        # Images
        self.back_img = pygame.image.load('graphics/Overworld/back.png').convert_alpha()
        self.play_img = pygame.image.load('graphics/Overworld/play.png').convert_alpha()
        self.exit_img = pygame.image.load('graphics/Overworld/exit.png').convert_alpha()
        self.fullscreen_img = pygame.image.load('graphics/Overworld/fullscreen.png').convert_alpha()
        self.shirt_img = pygame.image.load('graphics/Overworld/shirt.png').convert_alpha()

        # data


    def create_level(self, node, character):
        self.level = Level(character, node.content, node.pos, node.next_lvl, self.create_overworld, self.recreate_level, self.create_next_level)
        self.status = 'Level'

    def recreate_level(self, character, pos, content, next_lvl):
        self.level = Level(character, content, pos, next_lvl, self.create_overworld, self.recreate_level, self.create_next_level)

    def create_next_level(self, character, pos, content, next_lvl):
        self.level = Level(character, content, pos, next_lvl, self.create_overworld, self.recreate_level, self.create_next_level)

    def create_overworld(self, pos, character):
        self.overworld = Overworld(character, pos, self.create_level, self.create_titlescreen)
        self.status = 'Overworld'

    def create_helpscreen(self):
        self.helpscreen = Helpscreen(self.create_titlescreen)
        self.status = 'Helpscreen'

    def create_infoscreen(self):
        self.infoscreen = Infoscreen(self.create_titlescreen)
        self.status = 'Infoscreen'

    def create_titlescreen(self, pos):
        self.titlescreen = Titlescreen(pos, self.create_level, self.create_overworld, self.create_helpscreen, self.create_infoscreen, self.create_skinscreen)
        self.status = 'Titlescreen'

    def create_skinscreen(self, index):
        self.skinscreen = Skinscreen(index, self.create_titlescreen)
        self.status = 'Skinscreen'

    def run(self):
        prev_time = time.time()
        while True:
            dt = time.time() - prev_time
            prev_time = time.time()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                       pygame.quit()
                       sys.exit()
                    if event.key == pygame.K_F11:
                        pygame.display.toggle_fullscreen()

            self.screen.fill((33, 31, 48))
            if self.status == 'Titlescreen':
                self.titlescreen.run(dt)
                self.screen.blit(self.exit_img, (16, 16))
                self.screen.blit(self.play_img, (553, 16))
                self.screen.blit(self.shirt_img, (16, 312))
                self.screen.blit(self.fullscreen_img, (553, 312))
            elif self.status == 'Helpscreen':
                self.helpscreen.run(dt)
                self.screen.blit(self.back_img, (16, 16))
            elif self.status == 'Infoscreen':
                self.infoscreen.run(dt)
                self.screen.blit(self.back_img, (16, 16))
            elif self.status == 'Skinscreen':
                self.skinscreen.run(dt)
                self.screen.blit(self.play_img, (553, 16))
                self.screen.blit(self.back_img, (16, 16))
                self.screen.blit(self.fullscreen_img, (553, 312))
            elif self.status == 'Overworld':
                self.overworld.run(dt)
                self.screen.blit(self.back_img, (16, 16))
                self.screen.blit(self.play_img, (553, 16))
            elif self.status == 'Level':
                self.level.run(dt)
            debug('FPS', int(self.clock.get_fps()), 34)

            pygame.display.update()
            self.clock.tick(fps)
