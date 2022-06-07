import pygame, sys, time
from src.setting import *
from src.level import Level
from src.overworld import Overworld
from src.titlescreen import Titlescreen
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
        self.titlescreen = Titlescreen(self.create_level, self.create_overworld)
        self.status = 'Titlescreen'

        # Images
        self.back_img = pygame.image.load('graphics/Overworld/back.png').convert_alpha()
        self.play_img = pygame.image.load('graphics/Overworld/play.png').convert_alpha()

    def create_level(self, node):
        self.level = Level(node.content, node.pos, node.next_lvl, self.create_overworld, self.recreate_level, self.create_next_level)
        self.status = 'Level'

    def recreate_level(self, pos, content, next_lvl):
        self.level = Level(content, pos, next_lvl, self.create_overworld, self.recreate_level, self.create_next_level)

    def create_next_level(self, pos, content, next_lvl):
        self.level = Level(content, pos, next_lvl, self.create_overworld, self.recreate_level, self.create_next_level)

    def create_overworld(self, pos):
        self.overworld = Overworld(pos, self.create_level, self.create_titlescreen)
        self.status = 'Overworld'

    def create_titlescreen(self):
        self.titlescreen = Titlescreen(self.create_level, self.create_overworld)
        self.status = 'Titlescreen'

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
                self.screen.blit(self.play_img, (553, 16))
            elif self.status == 'Overworld':
                self.overworld.run(dt)
                self.screen.blit(self.back_img, (16, 16))
                self.screen.blit(self.play_img, (553, 16))
            elif self.status == 'Level':
                self.level.run(dt)
            debug('FPS', int(self.clock.get_fps()), 34)

            pygame.display.update()
            self.clock.tick(fps)
