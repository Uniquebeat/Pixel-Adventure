import pygame, sys, time
from src.setting import *
from src.level import Level
from src.overworld import Overworld
from src.debug import debug
from src.game_data import *


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((scaled_width, scaled_height), pygame.SCALED)
        pygame.display.set_caption('Pixel_Adventure_1')
        self.clock = pygame.time.Clock()
        self.overworld = Overworld((144, 32), self.create_level)
        self.status = 'Overworld'

    def create_level(self, node):
        self.level = Level(node.content, node.pos, node.next_lvl, self.create_overworld, self.recreate_level, self.create_next_level)
        self.status = 'Level'

    def recreate_level(self, pos, content, next_lvl):
        self.level = Level(content, pos, next_lvl, self.create_overworld, self.recreate_level, self.create_next_level)

    def create_next_level(self, pos, content, next_lvl):
        self.level = Level(content, pos, next_lvl, self.create_overworld, self.recreate_level, self.create_next_level)

    def create_overworld(self, pos):
        self.overworld = Overworld(pos, self.create_level)
        self.status = 'Overworld'

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
            if self.status == 'Overworld':
                self.overworld.run(dt)
            elif self.status == 'Level':
                self.level.run(dt)
            debug('FPS', int(self.clock.get_fps()), 34)

            pygame.display.update()
            self.clock.tick(fps)
